import logging

__author__ = 'zebraxxl'


def info(msg, *args, **kwargs):
    logging.info(msg.format(*args, **kwargs))


def error(msg, *args, **kwargs):
    logging.error(msg.format(*args, **kwargs))


def warning(msg, *args, **kwargs):
    logging.warning(msg.format(*args, **kwargs))