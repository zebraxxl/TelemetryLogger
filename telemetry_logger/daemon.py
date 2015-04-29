import os
import signal
from consts import ARGUMENT_COMMAND, COMMAND_STOP, COMMAND_RESTART, ARGUMENT_PID_FILE, COMMAND_START, \
    ARGUMENT_CONTROL_ADDR, ARGUMENT_CONTROL_PORT, ARGUMENT_DEBUG
import control
from logger import info, error
from telemetry_logger import run_logger
from utils import try_to_int

__author__ = 'zebraxxl'
pid_file = ''


def __daemon_main(settings):
    control.start(settings[ARGUMENT_CONTROL_ADDR], settings[ARGUMENT_CONTROL_PORT])
    run_logger(settings)


def __stop(settings):
    global pid_file
    info('Stopping the daemon...')

    pid_file = settings[ARGUMENT_PID_FILE]
    if not os.path.exists(pid_file) or not os.path.isfile(pid_file):
        error('Pid file {0} not exist', pid_file)
        return

    try:
        with open(pid_file, 'r') as f:
            pid = f.read()
    except Exception as e:
        error('Error while reading pid file {0} ({1})', pid_file, e)
        return
    finally:
        os.unlink(pid_file)

    pid = try_to_int(pid)

    if pid is None:
        error('Pid file was invalid')
        return

    # TODO: Check for pid exist
    os.kill(pid, signal.SIGKILL)
    info('Daemon stopped')


def __start(settings):
    global pid_file
    info('Starting the daemon...')

    pid_file = settings[ARGUMENT_PID_FILE]
    if os.path.exists(pid_file) and os.path.isfile(pid_file):
        error('Pid file {0} exist. Can\'t start new instance', pid_file)
        return

    if not settings[ARGUMENT_DEBUG]:
        if os.fork() != 0:
            info('Daemon started')
            return

    pid = os.getpid()

    try:
        with open(pid_file, 'w') as f:
            f.write(str(pid))
    except Exception as e:
        if os.path.exists(pid_file) and os.path.isfile(pid_file):
            os.remove(pid_file)
        error('Error while writing pid file {0} ({1}). Daemon was stopped', pid_file, e)
        return

    try:
        __daemon_main(settings)
    except Exception as e:
        error('Unhandled error while running daemon ({0})', e)

    info('Daemon stopped')


def run(settings):
    if settings[ARGUMENT_COMMAND] == COMMAND_STOP or settings[ARGUMENT_COMMAND] == COMMAND_RESTART:
        __stop(settings)
    if settings[ARGUMENT_COMMAND] == COMMAND_RESTART or settings[ARGUMENT_COMMAND] == COMMAND_START:
        __start(settings)