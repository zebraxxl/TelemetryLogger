import logging
from telemetry_logger.consts import INPUT_MODULE_SYSTEM, ARGUMENT_INPUT_MODULE, INPUT_MODULE_NET

__author__ = 'zebraxxl'
logger = logging.getLogger('input')


class InputModule:
    __on_frame = list()

    def _invoke_on_frame(self, frame):
        logger.trace('Invoking on frame handlers')

        for handler in self.__on_frame:
            handler(frame)

    def __init__(self, settings):
        pass

    def subscribe_to_frame(self, on_frame):
        self.__on_frame.append(on_frame)

    def start(self):
        pass


def init_input(settings):
    global input_module

    from telemetry_logger.input.system import SystemInputModule
    from telemetry_logger.input.net import NetInputModule

    input_modules = {
        INPUT_MODULE_SYSTEM: SystemInputModule,
        INPUT_MODULE_NET: NetInputModule,
    }

    input_module = input_modules[settings[ARGUMENT_INPUT_MODULE]](settings)


def subscribe_to_frame(on_frame):
    global input_module
    input_module.subscribe_to_frame(on_frame)


def start():
    global input_module
    input_module.start()
