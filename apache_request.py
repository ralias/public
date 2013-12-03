#!/usr/bin/python
import urllib2, re, sys, argparse, os
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse

parser=argparse.ArgumentParser(
description='Get status and performance information from Apache server-status module.',
epilog="Try it again.")
parser.add_argument('url', type=str, help='Apache server-status source server.')
parser.set_defaults(feature=False)
args=parser.parse_args()
#print(args)
#print args.extend
ExitStatus = 0

URL=args.url
os.environ['http_proxy'] = ''
html = urllib2.urlopen(URL) 
html.soup = BeautifulSoup(html.read())
data = html.soup.pre
print "|Total Workers="+str(TotalWorkers)+"; Running Workers="+str(RunningWorkers)+"; Idle Workers="+str(IdleWorkers)
sys.exit(ExitStatus)
