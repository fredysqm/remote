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

        if not r.exists('REMOTE_TIMEOUT'):
            r.set('REMOTE_TIMEOUT', 0)

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
