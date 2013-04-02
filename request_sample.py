#-*- coding: utf-8 -*-

import urllib2
import urllib
import sys

if __name__ == '__main__' :
    opener = urllib2.build_opener()
    request = urllib2.Request('http://localhost:8080/streaming')
    response = opener.open(request)
    #response = urllib2.urlopen('http://localhost:8080/streaming')
    #print(response._rbufsize)
    #print(dir(response.fp))
    response.fp._rbufsize = 1

    for line in iter(response.readline, '') :
        sys.stdout.write(line)
