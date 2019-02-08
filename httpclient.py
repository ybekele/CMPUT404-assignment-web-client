#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
#import urllib.parse
from urllib.parse import urlparse, urlencode


def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        data = data.split("\r\n")
        #[HTTP, code, message]
        line = data[0].split()
        #WILL BE 1XX,2XX,3XX,4XX
        print(line)
        code = int(line[1])



        return(code)

        #return None

    def get_headers(self,data):
        print("this is get_header")
        return None

    def get_body(self, data):
        # gets the body
        data = data.split("\r\n\r\n")
        body = data[1]
        return body

    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))

    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

        # Server response
# HTTP/1.1 200 OK
# Date: Mon, 27 Jul 2009 12:28:53 GMT
# Server: Apache/2.2.14 (Win32)
# Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
# Content-Length: 88
# Content-Type: text/html
# Connection: Closed


    # def make_response(self, mode, host, path):
    #     if mode == "GET":
    #         response = "GET /" + path + " " + "HTTP/1.1\r\n" + "Host: {}\r\n\r\n".format(host)
    #
    #     elif mode == "POST":
    #         response = "POST /" + path + " " + "HTTP/1.1\r\n" + "Host: {}\r\n\r\n".format(host)
    #
    #     else:
    #         return

    def GET(self, url, args=None):
        code = 500
        #a URL: scheme://netloc/path;parameters?query#fragment
        parsed_url = urlparse(url)
        host = parsed_url.hostname

        if host == None:
            raise ConnectionError("Can't find the host")
        path = parsed_url.path
        if path == None:
            raise ConnectionError("Can't find this path")
        port = parsed_url.port

        if port == None:
            port = 80
        #get_response = make_response("GET", host, path)
        #get_request = "GET " + path + " HTTP/1.1\r\n" + "Host: {}\r\n\r\n".format(host)
        get_request = ('GET {} HTTP/1.1\r\nHost: {} \r\nConnection: close\r\n\r\n'.format(path, host))
        self.connect(host, port)
        self.sendall(get_request)
        data = self.recvall(self.socket)
        self.close()
        if data == None:
            raise Exception("The response was empty")
        code = self.get_code(data)
        body = self.get_body(data)

        print(body)
        #code = 500
        return HTTPResponse(code, body)


    def POST(self, url, args=None):
        code = 500
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        path = parsed_url.path
        port = parsed_url.port

        if host == None:
            raise ConnectionError("Can't find this host")
        path = parsed_url.path
        if path == None:
            raise ConnectionError("Can't find this path")
        if port == None:
            port = 80

        args_encoded = ""
        if args is not None:
            args_encoded = urlencode(args)



        #if (path != None) and (host != None):
        #    post_request = "POST " + path + " HTTP/1.1\r\n" + "Host: {}\r\n".format(host)
        #    post_request += "Content-Type: application/x-www-form-urlencoded\r\n\\r\n"

            # if arguments were provided we have to set the content length

        #post_request += "Content-Length: {}\r\n\r\n".format(str(len(args_encoded)))
        #post_request += args_encoded
        post_request = ('POST {} HTTP/1.1\r\nHost: {} \r\n'.format(path, host)) + ('Content-Type: application/x-www-form-urlencoded\r\n') + ('Content-Length:{}\r\nConnection: close\r\n\r\n{}'.format(str(len(args_encoded)),args_encoded))


        # if we can't find the host or path

        # else:
        #     raise Exception('Either the path {} or host {} does not exist'.format(path, host))
        #     return

        self.connect(host, port)
        self.sendall(post_request)
        data = self.recvall(self.socket)

        self.close()
        if data == None:
            raise Exception("The response was empty")
        code = self.get_code(data)
        body = self.get_body(data)


    #    print(body)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )



if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
