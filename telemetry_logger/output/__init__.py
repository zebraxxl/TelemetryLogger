from threading import Lock
from telemetry_logger.consts import OUTPUT_MODULE_FILE, ARGUMENT_OUTPUT_MODULE

__author__ = 'zebraxxl'


class OutputModule:
    def __init__(self, settings):
        pass

    def write_frame(self, frame):
        pass


write_lock = Lock()
output_module = None


def init_output(settings):
    from telemetry_logger.output.file import FileOutputModule
    global output_module

    __OUTPUT_MODULES = {
        OUTPUT_MODULE_FILE: FileOutputModule
    }

    output_module = __OUTPUT_MODULES[settings[ARGUMENT_OUTPUT_MODULE]](settings)


def write_frame(frame):
    global output_module

    write_lock.acquire()
    try:
        output_module.write_frame(frame)
    finally:
        write_lock.release()
