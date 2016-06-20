#!/usr/bin/env python
import os
import time
import redis
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = '127.0.0.1'
PORT_NUMBER = 9000
REMOTE_TIMEOUT = 300 #seconds


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        r = redis.StrictRedis(host='localhost', port=6379, db=0)

        if int(r.get('REMOTE_TIMEOUT')) + REMOTE_TIMEOUT < int(time.time()):
            os.system('systemctl restart memcached.service')
            r.set('REMOTE_TIMEOUT', int(time.time()))
            self.wfile.write(bytes('Memcached reiniciado!', 'utf8'))
        else:
            remain = str(int(r.get('REMOTE_TIMEOUT')) + REMOTE_TIMEOUT - int(time.time()))
            self.wfile.write(bytes('Esperar %s segundos!' % (remain), 'utf8'))

        return


def run():
    print('starting server...')
    server_address = (HOST_NAME, PORT_NUMBER)
    httpd = HTTPServer(server_address, Server)
    print('running server...')
    httpd.serve_forever()


run()

# class MyHandler(http.server.BaseHTTPServer.BaseHTTPRequestHandler):
#     def do_HEAD(s):
#         s.send_response(200)
#         s.send_header("Content-type", "text/html")
#         s.end_headers()
#     def do_GET(s):
#         """Respond to a GET request."""
#         s.send_response(200)
#         s.send_header("Content-type", "text/html")
#         s.end_headers()
#         s.wfile.write("<html><head><title>Title goes here.</title></head>")
#         s.wfile.write("<body><p>This is a test.</p>")
#         # If someone went to "http://something.somewhere.net/foo/bar/",
#         # then s.path equals "/foo/bar/".
#         s.wfile.write("<p>You accessed path: %s</p>" % s.path)
#         s.wfile.write("</body></html>")
#         print(s.path.split('/'))

# if __name__ == '__main__':
#     server_class = BaseHTTPServer.HTTPServer
#     httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
#     print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
#     try:
#         httpd.serve_forever()
#     except KeyboardInterrupt:
#         pass
#     httpd.server_close()
#     print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))
