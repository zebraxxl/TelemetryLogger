import logging
import os
import signal
from traceback import format_exc
from consts import ARGUMENT_COMMAND, COMMAND_STOP, COMMAND_RESTART, ARGUMENT_PID_FILE, COMMAND_START, \
    ARGUMENT_CONTROL_ADDR, ARGUMENT_CONTROL_PORT, ARGUMENT_DEBUG
import control
from telemetry_logger import run_logger
from utils import try_to_int

__author__ = 'zebraxxl'
pid_file = ''

logger = logging.getLogger('daemon')


def __daemon_main(settings):
    logging.info('')
    logging.info('================================= NEW SESSION =================================')
    logging.info('')

    control.start(settings[ARGUMENT_CONTROL_ADDR], settings[ARGUMENT_CONTROL_PORT])
    run_logger(settings)


def __stop(settings):
    global pid_file
    logger.info('Stopping the daemon...')

    pid_file = settings[ARGUMENT_PID_FILE]
    if not os.path.exists(pid_file) or not os.path.isfile(pid_file):
        logger.error('Pid file %s not exist', pid_file)
        return

    try:
        with open(pid_file, 'r') as f:
            pid = f.read()
    except Exception as e:
        logger.error('Error while reading pid file %s (%s)', pid_file, e)
        return
    finally:
        os.unlink(pid_file)

    pid = try_to_int(pid)

    if pid is None:
        logger.error('Pid file was invalid')
        return

    # TODO: Check for pid exist
    os.kill(pid, signal.SIGKILL)
    logger.info('Daemon stopped')


def __start(settings):
    global pid_file
    logger.info('Starting the daemon...')

    pid_file = settings[ARGUMENT_PID_FILE]
    if os.path.exists(pid_file) and os.path.isfile(pid_file):
        logger.error('Pid file %s exist. Can\'t start new instance', pid_file)
        return

    if not settings[ARGUMENT_DEBUG]:
        if os.fork() != 0:
            logger.info('Daemon started')
            return

    pid = os.getpid()

    try:
        with open(pid_file, 'w') as f:
            f.write(str(pid))
    except Exception as e:
        if os.path.exists(pid_file) and os.path.isfile(pid_file):
            os.remove(pid_file)
        logger.error('Error while writing pid file %s (%s). Daemon was stopped', pid_file, e)
        return

    try:
        __daemon_main(settings)
    except Exception as e:
        logger.error('Unhandled error while running daemon (%s)', e)
        logger.error('', format_exc())

    logger.info('Daemon stopped')


def run(settings):
    if settings[ARGUMENT_COMMAND] == COMMAND_STOP or settings[ARGUMENT_COMMAND] == COMMAND_RESTART:
        __stop(settings)
    if settings[ARGUMENT_COMMAND] == COMMAND_RESTART or settings[ARGUMENT_COMMAND] == COMMAND_START:
        __start(settings)