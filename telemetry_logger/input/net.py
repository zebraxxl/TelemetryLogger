from socket import socket
import struct
from threading import Thread
import cPickle
from telemetry_logger.consts import ARGUMENT_INPUT_ADDRESS, ARGUMENT_INPUT_PORT
from telemetry_logger.input import InputModule

__author__ = 'zebraxxl'


class NetInputModule(InputModule):
    class NetInputReadThread(Thread):
        def __init__(self, module, sock):
            Thread.__init__(self)
            self.setDaemon(True)
            self.module = module
            self.sock = sock

        def run(self):
            try:
                while True:
                    data_len_raw = self.sock.recv(4)
                    data_len = struct.unpack('<I', data_len_raw)[0]

                    data_raw = self.sock.recv(data_len)
                    data = cPickle.loads(data_raw)
                    self.module._invoke_on_frame(data)
            except Exception as e:
                pass


    class NetInputThread(Thread):
        def __init__(self, module):
            Thread.__init__(self)
            self.setDaemon(True)
            self.module = module
            self.sock = None

        def run(self):
            self.sock = socket()
            self.sock.bind((self.module.settings[ARGUMENT_INPUT_ADDRESS],
                            int(self.module.settings[ARGUMENT_INPUT_PORT])))
            self.sock.listen(1)

            while True:
                try:
                    connection, address = self.sock.accept()
                    NetInputModule.NetInputReadThread(self.module, connection).start()
                except Exception as e:
                    pass

    def __init__(self, settings):
        InputModule.__init__(self, settings)
        self.settings = settings
        self.thread = None

    def start(self):
        self.thread = NetInputModule.NetInputThread(self)
        self.thread.start()
