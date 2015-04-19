import socket
import cPickle
import struct
from consts import ARGUMENT_OUTPUT, PICKLE_PROTOCOL_VERSION
from output import OutputModule

__author__ = 'zebraxxl'


class NetOutputModule(OutputModule):
    def __init__(self, settings):
        OutputModule.__init__(self, settings)
        addr = settings[ARGUMENT_OUTPUT].split(':')

        self.socket = socket.socket()
        self.socket.connect((addr[0], int(addr[1])))

    def write_frame(self, frame):
        raw_data = cPickle.dumps(frame, PICKLE_PROTOCOL_VERSION)
        raw_data_len = len(raw_data)

        self.socket.sendall(struct.pack('<I', raw_data_len))
        self.socket.sendall(raw_data)
