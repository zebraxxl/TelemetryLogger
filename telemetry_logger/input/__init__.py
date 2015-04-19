from telemetry_logger.consts import INPUT_MODULE_SYSTEM, ARGUMENT_INPUT_MODULE

__author__ = 'zebraxxl'


class InputModule:
    __on_frame = list()

    def _invoke_on_frame(self, frame):
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

    input_modules = {
        INPUT_MODULE_SYSTEM: SystemInputModule,
    }

    input_module = input_modules[settings[ARGUMENT_INPUT_MODULE]](settings)


def subscribe_to_frame(on_frame):
    global input_module
    input_module.subscribe_to_frame(on_frame)


def start():
    global input_module
    input_module.start()
