import time
from datetime import datetime
from consts import REMOTE_COMMAND_MARKER, REMOTE_COMMAND_MARKER_NAME, FRAME_TYPE_MARKER
from control import subscribe_to_command
from logger import error
from output import init_output, write_frame
from input import init_input, subscribe_to_frame, start

__author__ = 'zebraxxl'


def __set_marker(data):
    name = data[REMOTE_COMMAND_MARKER_NAME]
    frame = (datetime.now(), FRAME_TYPE_MARKER, name)
    write_frame(frame)


def run_logger(settings):
    try:
        init_output(settings)
    except Exception as e:
        error('Error while opening output ({0})', e)

    subscribe_to_command(REMOTE_COMMAND_MARKER, __set_marker)

    init_input(settings)
    subscribe_to_frame(lambda f: write_frame(f))
    start()

    while True:
        time.sleep(999999999)   # Sleep forever =)
