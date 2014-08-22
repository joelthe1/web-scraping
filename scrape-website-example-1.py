#!/usr/bin/python
'''Scrape a website using urllib2 (A library for pinging URLs) and BeautifulSoup (A library for parsing HTML)'''
from bs4 import BeautifulSoup
import urllib2
import time
import sys
import socket

start_time = time.time()

#Open files
rfile = open("input.csv","r").read().splitlines()
wfile = open("translations.csv","w")
sepComma = ","
newline = "\n"
counter = 0
tcounter = 0

#Start processing
for pEword in rfile:
      retry = 0
#      print pEword
      while True:
         try:
            counter += 1
            tcounter += 1
            url = "http://www.example.com/"

            print url
            req = urllib2.Request(url)
            req.add_header("Connection", "keep-alive")
            req.add_header("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0")
            #   req.add_header("Accept-Encoding", "gzip")
            req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
#            req.add_header("Cache-Control", "no-cache")
            req.add_header("Accept-Language", "en-US,en;q=0.8")
            req.add_header("Host", "filesdownloader.com")
#            req.add_header("If-Modified-Since", "Thu, 30 Jan 2014 17:24:29 GMT")
#            req.add_header("Cache-Control", "max-age=0")
#            req.add_header("If-Modified-Since", "Fri, 31 Jan 2014 21:52:35 GMT")
            req.add_header("Cookie", "s=6a11e5h6sald4faibrkcp5bm85; __unam=7639673-143e40de47e-4218148d-4; __utma=127728666.207454719.1391100551.1391208734.1391434591.6; __utmb=127728666.2.10.1391434591; __utmc=127728666; __utmz=127728666.1391197253.2.2.utmcsr=prx.centrump2p.com|utmccn=(referral)|utmcmd=referral|utmcct=/english/")
            page = urllib2.urlopen(req,timeout=4)
         except urllib2.HTTPError, e:
            if retry > 2:
               raise e
            print e.code
            retry += 1
            time.sleep(10)
         except urllib2.URLError, e:
            if retry > 2:
               raise e
            print e.args
            retry += 1
            time.sleep(10)
         except socket.timeout as e:
            if retry > 2:
               raise e
            print "Request timed out!"
            retry += 1
            time.sleep(10)
         except:
            etype, value, tb = sys.exc_info()
            response = "%s" % value.message
            print etype,response,tb
            raise
         else:
            soup = BeautifulSoup(page.read())
            orderedlists = soup.find_all("ol", class_="eirol")
            wfile.write(pEword);wfile.write(sepComma)
            #Looping <li> tags
            for thelist in orderedlists:
               for listitems in thelist:
                  pHword = listitems.next_element.next_sibling.string.encode('utf-8')
                  print pHword
                  wfile.write(pHword);wfile.write(sepComma);
#            print pHword
            wfile.write(newline)
#            if counter > 2:
#               time.sleep(3)
#               counter = 0
            if tcounter/1000 in range(15) and tcounter%1000 == 0:
               print "{words} words completed".format(words = tcounter)
#            if tcounter%300 == 0:
#               print "Waiting for 10 mins"
#               time.sleep(600)
            break

wfile.close()
print time.time() - start_time, "seconds"
print "Successfully created dictionary."
