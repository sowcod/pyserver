#-*- coding: utf-8 -*-

import BaseHTTPServer
import re

class URLHandler(object) :
    def __init__(self) :
        self.paths = []

    #decolator
    def url(self, pattern) :
        def wrap(func) :
            # func(name, request_handler, match)
            self.add_path(func, pattern)
            return func
        return wrap

    def do_handler(self, request_handler) :
        target_path = request_handler.path
        for path in self.paths :
            match = path[1].match(target_path)
            if match is not None :
                request_handler.send_response(200)
                if path[2] is None :
                    path[0](request_handler, match)
                else:
                    path[0](request_handler, match, path[2])
                return True
        return False

    def add_path(self, func, path_pattern, name = None) :
        # func(request_handler, match[, name])
        self.paths.append((func, re.compile(path_pattern), name))

class MyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler) :
    @classmethod
    def set_url_handler(cls, handler) :
        cls.handler = handler

    def get_favicon_path(self) :
        return 'favicon.png'

    def process_favicon(self) :
        self.send_response(200)
        self.send_headers({'Content-Type' : 'image/png'})
        with open(self.get_favicon_path(), 'rb') as f:
            self.wfile.write(f.read())

    def process_404(self) :
        self.send_response(404)
        self.send_headers()
        self.wfile.write('<html><header><title>404</title><body>404</body></html>')

    def do_GET(self) :
        if self.path == '/favicon.ico' :
            self.process_favicon()
            return

        if not self.__class__.handler.do_handler(self) :
            self.process_404()

    def get_basic_headers(self) :
        return {
                'Cache-Control' : 'no-cache',
                #'Connection' : 'close',
                'Content-Type' : 'text/html',
                'Location' : self.path,
                }

    def send_headers(self, headers = {}, replace = False) :
        if replace : new_headers = {}
        else       : new_headers = self.get_basic_headers()
        new_headers.update(headers)
        for key, value in sorted(new_headers.items(), key = lambda x : x[0]) :
            self.send_header(key, value)

        self.end_headers()

def runserver(handler, url, port) :
    MyRequestHandler.set_url_handler(handler)

    server = BaseHTTPServer.HTTPServer(('localhost', 8080), MyRequestHandler)
    server.serve_forever()

if __name__ == '__main__' :
    api_handler = URLHandler()

    @api_handler.url('/(?P<path>.*)$')
    def handle_root(handler, match) :
        handler.send_headers()
        handler.wfile.write('<html><body><b>')
        handler.wfile.write(match.group('path'))
        handler.wfile.write('</b></body></html>')

    #api_handler.add_path(handle_root, '^/$', 'root')
    runserver(api_handler, 'localhost', 8080)
