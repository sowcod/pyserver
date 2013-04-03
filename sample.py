#-*- coding: utf-8 -*-

import pyserver

handler = pyserver.URLHandler()

@handler.url('/$')
def toppage(handler, match) :
    handler.send_headers()
    handler.wfile.write('<html><body><b>')
    handler.wfile.write('Welcome to pyserver')
    handler.wfile.write('</b></body></html>')

@handler.url('/json')
def json(handler, match) :
    handler.send_headers({'Content-Type' : 'application/json'})
    handler.wfile.write('{"key1" : 1, "key2" : 2}')

@handler.url('/streaming')
def streaming(handler, match) :
    import time
    handler.send_headers({'Content-Type' : 'text/event-stream'})
    for i in range(10) :
        handler.wfile.write('response %d\r\n' % i)
        time.sleep(1)

if __name__ == '__main__' :
    pyserver.runserver(handler, 'localhost', 8080)
