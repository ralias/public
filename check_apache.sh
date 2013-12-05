#!/bin/bash
usage(){
        echo "Usage: $0 server -c -w [-e]"
        exit 1
}

[[ $# -eq 0 ]] && usage

TEMP_FILE=/tmp/$$.apache_vhosts
unset http_proxy
ExitStatus=0
Status="OK"

links -dump http://$1/server-status > $TEMP_FILE
[[ $? -ne 0 ]] && exit 2

WorkersLines=`cat $TEMP_FILE |sed -n "/idle workers/,/Scoreboard/p" |head -n-2 |tail -n+3 |wc -l`
TotalWorkers=$((`cat $TEMP_FILE |sed -n "/idle workers/,/Scoreboard/p" |head -n-2 |tail -n+3 |wc -c` - $(($WorkersLines * 2))))
RunningWorkers=`cat $TEMP_FILE |grep [0-9]-[0-9] |awk '{print $4}' |egrep -v  "\." |egrep -v "\_" |wc -l`
WaitingForConnection=`cat $TEMP_FILE |grep [0-9]-[0-9] |awk '{print $4}'|grep "\_" |wc -l`
StartingUp=`cat $TEMP_FILE |grep [0-9]-[0-9] |awk '{print $4}'|grep "S" |wc -l`
ReadingRequest=`cat $TEMP_FILE |grep [0-9]-[0-9] |awk '{print $4}'|grep "R" |wc -l`
SendingReply=`cat $TEMP_FILE |grep [0-9]-[0-9] |awk '{print $4}'|grep "W" |wc -l`
Keepalive=`cat $TEMP_FILE |grep [0-9]-[0-9] |awk '{print $4}'|grep "K" |wc -l`
DNSLookup=`cat $TEMP_FILE |grep [0-9]-[0-9] |awk '{print $4}'|grep "D" |wc -l`
ClosingConnection=`cat $TEMP_FILE |grep [0-9]-[0-9] |awk '{print $4}'|grep "C" |wc -l`
Logging=`cat $TEMP_FILE |grep [0-9]-[0-9] |awk '{print $4}'|grep "L" |wc -l`
GracefullyFinishing=`cat $TEMP_FILE |grep [0-9]-[0-9] |awk '{print $4}'|grep "G" |wc -l`
IdleCleanupOfWorker=`cat $TEMP_FILE |grep [0-9]-[0-9] |awk '{print $4}'|grep "I" |wc -l`
OpenSlotWithNoCurrentProcess=`cat $TEMP_FILE |grep [0-9]-[0-9] |awk '{print $4}'|grep "." |wc -l`
IdleWorkers=$(($TotalWorkers - $RunningWorkers))

PercentInUse=`echo "(100*$RunningWorkers)/$TotalWorkers" |bc -l`
PercentFree=`echo "100-$PercentInUse" |bc -l`
PercentInUseNoDec=`printf "%.0f" "$PercentInUse"`
PercentFreeNoDec=`printf "%.0f" "$PercentFree"`

if [ ! -z $2 ] && [ ! -z $3 ] && [ $2 -le $3 ]; then
        echo "Warning threshold is greater than the Critical threshold."
        exit 1
fi
if [[ $PercentInUseNoDec -ge $2 ]]; then
        Status="CRITICAL"
        ExitStatus=2
fi
if [[ $PercentInUseNoDec -ge $3 ]] && [[ $ExitStatus -eq 0 ]]; then
        Status="WARNING"
        ExitStatus=1
fi

if [ "$4" = "-e" ]; then
        printf "%s - %.2f%% in use, %.2f%% free. |Total Workers=%d; Waiting for Connection=%d; Starting up=%d; Reading Request=%d; Sending Reply=%d; Keepalive=%d; DNS Lookup=%d; Closing Connection=%d; Logging=%d; Gracefylly finishing=%d; Idle Cleanup of Worker=%d; Open Slot with no current Process=%d\n" "$Status" "$PercentInUse" "$PercentFree" "$TotalWorkers" "$WaitingForConnection" "$StartingUp" "$ReadingRequest" "$SendingReply" "$Keepalive" "$DNSLookup" "$ClosingConnection" "$Logging" "$GracefullyFinishing" "$IdleCleanupOfWorker" "$OpenSlotWithNoCurrentProcess"
        \rm -rf $TEMP_FILE
        exit $ExitStatus
fi
printf "%s - %.2f%% in use, %.2f%% free. |Total Workers=%d; Running Workers=%d; Idle Workers=%d\n" "$Status" "$PercentInUse" "$PercentFree" "$TotalWorkers" "$RunningWorkers" "$IdleWorkers"
\rm -rf $TEMP_FILE
exit $ExitStatus
