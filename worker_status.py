#!/usr/bin/python
import urllib2, re, sys, argparse, os
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse

parser=argparse.ArgumentParser(
description='Get status and performance information from Apache server-status module.',
epilog="Try it again.")
parser.add_argument('url', type=str, help='Apache server-status source server.')
parser.add_argument('-c', type=int, choices=range(0,100), help= 'Critical Threshold.')
parser.add_argument('-w', type=int, choices=range(0,100), help='Warning Threshold.')
parser.add_argument('-e', dest='extend', action='store_true', help='Extended status information.')
parser.set_defaults(feature=False)
args=parser.parse_args()
#print(args)
#print args.extend
ExitStatus = 0
Status = 'OK'

if (args.c is not None and args.w is not None) and (args.w >= args.c):
        print "Warning threshold is greater than the Critical threshold."
        sys.exit(1)
URL=args.url
os.environ['http_proxy'] = ''
html = urllib2.urlopen(URL) 
html.soup = BeautifulSoup(html.read())
#print title
data = html.soup.pre

#Scoreboard Key:
#"_" Waiting for Connection
#"S" Starting up
#"R" Reading Request
#"W" Sending Reply
#"K" Keepalive (read)
#"D" DNS Lookup
#"C" Closing connection
#"L" Logging
#"G" Gracefully finishing
#"I" Idle cleanup of worker
#"." Open slot with no current process

#print data.string
#print len(data.string)
#print len(data.string.lstrip(' '))
WFC = data.string.count('_')
OSWNCP = data.string.count('.')
SU = data.string.count('S')
RR = data.string.count('R')
SR = data.string.count('W')
KR = data.string.count('K')
DL = data.string.count('D')
CC = data.string.count('C')
L = data.string.count('L')
GF = data.string.count('G')
ICOW = data.string.count('I')
TotalWorkers = WFC + OSWNCP + SU + RR + SR + KR + DL + CC + L + GF + ICOW
IdleWorkers = OSWNCP + WFC
RunningWorkers = SU + RR + SR + KR + DL + CC + L + GF + ICOW

PercentInUse = (100 * RunningWorkers) / TotalWorkers
PercentFree = 100-PercentInUse

if (args.c is not None) and (PercentInUse >= args.c):
        Status = "CRITICAL"
        ExitStatus = 2
if (args.w is not None) and (PercentInUse >= args.w) and (Status == "OK"):
        Status = "WARNING"
        ExitStatus = 1

print Status+" "+str(PercentInUse)+"% in use,", str(PercentFree)+"% free.",

if (args.extend == True ):
        print "|Total Workers="+str(TotalWorkers)+\
        "; Waiting for Connection="+str(WFC)+\
        "; Open Slot with no current Process="+str(OSWNCP)+\
        "; Starting up="+str(SU)+\
        "; Reading Request="+str(RR)+\
        "; Sending Reply="+str(SR)+\
        "; Keepalive="+str(KR)+\
        "; DNS Lookup="+str(DL)+\
        "; Closing Connection="+str(CC)+\
        "; Logging="+str(L)+\
        "; Gracefylly finishing="+str(GF)+\
        "; Open Slot with no current process="+str(ICOW)
else:
        print "|Total Workers="+str(TotalWorkers)+"; Running Workers="+str(RunningWorkers)+"; Idle Workers="+str(IdleWorkers)

sys.exit(ExitStatus)
