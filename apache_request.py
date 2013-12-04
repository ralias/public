#!/usr/bin/python
import urllib2, re, sys, argparse, os, string
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse

parser=argparse.ArgumentParser(
description='Get Request/second from Apache server-status module.',
epilog="Try it again.")
parser.add_argument('url', type=str, help='Apache server-status source server.')
parser.set_defaults(feature=False)
args=parser.parse_args()
#print(args)
#print args.extend

class Status (object):
    _url = None

    def __init__ (self, url):
        self._url = url

    def fetch (self):
        return urllib2.urlopen(self._url).read()

    def parse (self):
        html = self.fetch()
        soup = BeautifulSoup(html)
        status = {}
        status['server_info'] = [i.string.strip() for i in soup.findAll('dt')]
        status['requests'] = []
        requests = soup.find('table').findAll('tr')
        keys = [i.string for i in requests.pop(0)]
        for tr in requests:
            req = {}
            for n, td in enumerate(tr):
                req[keys[n]] = td.string
            status['requests'].append(req)
        return status



status = Status(args.url)
data = status.parse()
#print "SERVER INFORMATION"
#print "=================="
for v in data['server_info']:
        if 'requests/sec' in v:
                result=re.split(' ',v)
                print str(result[1])+" "+str(result[0])+"|"+str(result[1])+"= "+str(result[0])

#print "REQUESTS BY VHOST"
#print "================="
#entries = [i['VHost'] for i in data['requests']]
#requests = sorted([(entries.count(i), i) for i in list(set(entries))], reverse=True)
#print "\n".join(["%d: %s"%(a,b) for a,b in requests])
sys.exit(0)
