#!/usr/bin/python
'''Scraping a website using mechanize(A headless browsing library) and BeautifulSoup(A library for parsing HTML)'''
from bs4 import BeautifulSoup
import urllib2
import time
import sys
import socket
import cookielib
import mechanize
import re

start_time = time.time()

#Open files
rfile = open("input_words.csv","r").read().splitlines()
wfile = open("translations.csv","w")
sepComma = ","
newline = "\n"
counter = 0
wflag = 0


#Browser instance
browser = mechanize.Browser()

#Set proxy
#browser.set_proxies({"http":"120.203.168.89:8123"})
#browser.set_proxies({"http":"183.87.54.46:8080"})

#Cookie Jar
cookiejar_inst = cookielib.LWPCookieJar()
browser.set_cookiejar(cookiejar_inst)

#Browser options
browser.set_handle_gzip(True)
browser.set_handle_referer(True)

browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'), ('Accept-Encoding','gzip,deflate,sdch'), ('Accept-Language', 'en-US,en;q=0.8'), ('Connection', 'keep-alive'), ('Host', 'www.englishnepalidictionary.com'), ('Origin', 'http://dictionary.tamilcube.com'), ('Referer','http://www.englishnepalidictionary.com')]

retry = 0
for eng_val in rfile:
      if eng_val.startswith("'"):
            print "found unclean word", eng_val
            continue
      retry = 0
      wflag = 0
      counter += 1
      while True:
            try:
                  input_eng_val = eng_val.split(',')[1]
#                  print input_eng_val
                  browser.open('http://www.englishnepalidictionary.com/?q={qparam}'.format(qparam = input_eng_val))
            except:
                  etype, value, tb = sys.exc_info()
                  response = "%s" % value.message
                  print etype,response,tb
                  if retry < 3:
                        retry += 1
                        time.sleep(10)
                  else:
                        raise
            else:
                  soup = BeautifulSoup(browser.response().read())
                  h3 = soup.find('h3')
                  count = 0
                  val = h3.contents[0].split(',')
                  print input_eng_val
                  if val[0].startswith(input_eng_val):
                        counter = counter + 1
                        for values in val:
                              if count == 0:
                                    temp =  values.split('-')
                              else:
                                    temp.append(values)
                              count = count + 1
                        final_line = ','.join(temp).encode('utf-8')
                        final_line = final_line.replace(newline,',')
                        final_line = final_line.replace(', ',',')
                        print final_line
                        wfile.write(final_line+newline)
            break
wfile.close()
rfile.close()

print counter,"word(s) processed"
print time.time() - start_time, "seconds"
print "Successfully created dictionary."
