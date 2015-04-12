import BaseHTTPServer
import SocketServer
import json
from threading import Thread, current_thread
import urllib
from urlparse import urlparse

__author__ = 'zebraxxl'


class ControlHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def process_request(self, arguments):
        try:
            url = urlparse(self.path)
            queries = url.query.split('&')
            for arg in queries:
                delimiter = arg.find('=')
                if delimiter < 0:
                    delimiter = len(arg)

                name = urllib.unquote(arg[:delimiter])
                value = urllib.unquote(arg[delimiter + 1:])
                arguments[name] = value

            result = current_thread().event_handlers[arguments['command']](arguments)

            self.send_response(200, result)
        except Exception as e:
            self.send_response(500, '{0}'.format(e))

    def do_GET(self):
        self.process_request(dict())

    def do_POST(self):
        try:
            data = json.loads(self.rfile.read())
            self.process_request(data)
        except Exception as e:
            self.send_response(500, '{0}'.format(e))


class ControlThread(Thread):
    event_handlers = dict()

    def __init__(self, address):
        Thread.__init__(self)
        self.setDaemon(True)
        self.__httpd = SocketServer.TCPServer(address, ControlHandler)

    def run(self):
        self.__httpd.serve_forever()
