#!/usr/bin/python
'''Scrape a website using mechanize (A library to do headless browsing), BeautifulSoup (A library to parse HTML files), threading and Queue (for Threading)'''
from bs4 import BeautifulSoup
import urllib2
import time
import sys
import socket
import cookielib
import mechanize
import re
import threading
import Queue

in_queue = Queue.Queue()
#out_queue = Queue.Queue()

class ThreadedUrlRead(threading.Thread):
    """Threaded reading of URLs"""
    def __init__(self, in_queue):
        threading.Thread.__init__(self)
        self.in_queue = in_queue
#        self.out_queue = out_queue
        #Browser instance
        self.browser = mechanize.Browser()

        #Set proxy
        #browser.set_proxies({"http":"120.203.168.89:8123"})
        #browser.set_proxies({"http":"183.87.54.46:8080"})

        #Cookie Jar
        self.cookiejar_inst = cookielib.LWPCookieJar()
        self.browser.set_cookiejar(self.cookiejar_inst)

        #Browser options
        self.browser.set_handle_gzip(True)
        self.browser.set_handle_referer(True)

        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'), ('Accept-Language', 'en-US,en;q=0.8'), ('Cache-Control', 'max-age=0'), ('Connection', 'keep-alive'), ('Host', 'dictionary.example.com'), ('Origin', 'http://dictionary.parent.example.com')]
    
    def run(self):
        counter = 0
        sepComma = ","
        newline = "\n"
        while True:
            #read words from in_queue
            eng_val = self.in_queue.get()

            if eng_val is None:
                print "done for now"
                break
            
            if eng_val.startswith("'"):
                print "Unsanitized word %s found" % eng_val
                continue
            
            retry = 0
            wflag = 0
            counter += 1
            while True:
                try:
                    self.browser.open('http://www.example.com')
                    self.browser.select_form(nr=0)
                    self.browser.form["name"] = eng_val
                    self.browser.submit() 
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
                    soup = BeautifulSoup(self.browser.response().read())
                    tds = soup.find_all("td", style=re.compile("padding:4px"))
                    regex = re.compile("^{eWord} :".format(eWord = eng_val), re.I)
                    regex2 = re.compile("^{eWord} \(".format(eWord = eng_val), re.I)
                    regex3 = re.compile("^{eWord} ;".format(eWord = eng_val), re.I)
                    regex4 = re.compile("^{eWord} [:;] [a-zA-Z]+".format(eWord = eng_val), re.I)
                    for td in tds:
                        trans_val = td.string.encode("utf-8").strip()
                        if (regex.match(trans_val) is not None or regex2.match(trans_val) is not None or regex3.match(trans_val) is not None) and regex4.match(trans_val) is None:
                            trans_val = trans_val.replace(":", ",", 1)
                            trans_val = trans_val.replace(";", ",")
                            trans_val = trans_val.replace(" , ", ",")
#                            wfile.write(trans_val); wfile.write(newline)
                            print trans_val
                            wflag = 1
                    if wflag == 0:
#                            wfile.write(eng_val);wfile.write(sepComma); wfile.wrpite(newline)
                        print eng_val,sepComma
                    self.in_queue.task_done()
                    break

start_time = time.time()

def main():
    #spawn pool of threads passing them the queue instance
    for i in range(5):
        t = ThreadedUrlRead(in_queue)
        t.daemon = True
        t.start()
        
    #Open files
    rfile = open("input-all.csv","r").read().splitlines()

    #populate in_queue with all words
    for words in rfile:
        in_queue.put(words)

    #wait until all processing is done
    in_queue.join()
   
    print "\nThat's all folks!"
 
main()
print "Time elapsed is %s" % (time.time() - start_time)
