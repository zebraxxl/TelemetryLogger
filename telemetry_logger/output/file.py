import cPickle
import logging
import struct
from telemetry_logger.consts import PICKLE_PROTOCOL_VERSION, ARGUMENT_OUTPUT
from telemetry_logger.output import OutputModule

__author__ = 'zebraxxl'
logger = logging.getLogger('output:file')


class FileOutputModule(OutputModule):
    def __init__(self, settings):
        OutputModule.__init__(self, settings)
        self.output_file = open(settings[ARGUMENT_OUTPUT], 'ab')

    def write_frame(self, frame):
        logger.trace('Frame writing')

        raw_data = cPickle.dumps(frame, PICKLE_PROTOCOL_VERSION)
        raw_data_len = len(raw_data)

        self.output_file.write(struct.pack('<I', raw_data_len))
        self.output_file.write(raw_data)
        self.output_file.flush()