import struct
from threading import Lock
import cPickle
from consts import PICKLE_PROTOCOL_VERSION

__author__ = 'zebraxxl'


write_lock = Lock()


def init_output_file(file_name):
    global output_file

    output_file = open(file_name, 'ab')


def write_frame(frame):
    global output_file

    write_lock.acquire()
    try:
        raw_data = cPickle.dumps(frame, PICKLE_PROTOCOL_VERSION)
        raw_data_len = len(raw_data)

        output_file.write(struct.pack('<I', raw_data_len))
        output_file.write(raw_data)
        output_file.flush()
    finally:
        write_lock.release()