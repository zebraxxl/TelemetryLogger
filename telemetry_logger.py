#!/usr/bin/env python2
import sys
import urllib
import urllib2
from telemetry_logger.logger import init_logger
from telemetry_logger.report import make_report
from telemetry_logger.consts import COMMAND_START, COMMAND_RESTART, COMMAND_STOP, ARGUMENT_COMMAND, COMMAND_MARKER, \
    ARGUMENT_COMMAND_PARAMETER, ARGUMENT_CONTROL_ADDR, ARGUMENT_CONTROL_PORT, REMOTE_COMMAND_MARKER, \
    REMOTE_COMMAND_MARKER_NAME, COMMAND_REPORT, ARGUMENT_RUNNING_LOG_CONFIG, PLATFORM_DATA, \
    PLATFORM_DEFAULT_LOG_DIRECTORY
from telemetry_logger import daemon
from telemetry_logger.arguments import process_settings

__author__ = 'zebraxxl'

__daemon_commands = frozenset([COMMAND_START, COMMAND_STOP, COMMAND_RESTART])


def send_marker_command(s, name):
    # TODO: Bad code. Need to be rewrited
    url = 'http://{addr}:{port}/control?command={command}&{command_param_name}={marker_name}'.format(
        addr=s[ARGUMENT_CONTROL_ADDR], port=s[ARGUMENT_CONTROL_PORT], command=REMOTE_COMMAND_MARKER,
        command_param_name=REMOTE_COMMAND_MARKER_NAME, marker_name=urllib.quote(name)
    )
    urllib2.urlopen(url).read()


if __name__ == '__main__':
    settings = process_settings()
    if not settings:
        sys.exit(1)

    if settings[ARGUMENT_COMMAND] in __daemon_commands:
        init_logger(PLATFORM_DATA[PLATFORM_DEFAULT_LOG_DIRECTORY], settings[ARGUMENT_RUNNING_LOG_CONFIG])
        daemon.run(settings)
    elif settings[ARGUMENT_COMMAND] == COMMAND_MARKER:
        send_marker_command(settings, settings[ARGUMENT_COMMAND_PARAMETER])
    elif settings[ARGUMENT_COMMAND] == COMMAND_REPORT:
        make_report(settings)
