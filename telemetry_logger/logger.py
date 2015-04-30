import logging
import logging.config
from logging.handlers import RotatingFileHandler
import os

__author__ = 'zebraxxl'

RUNNING_LOG_FILENAME = 'TelemetryLog.Running.log'
RUNNING_LOG_MAX_BYTES = 1024 * 1024     # 1 Mb
RUNNING_LOG_BACKUP_COUNT = 10
RUNNING_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
RUNNING_LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

TRACE_LOG_LEVEL = logging.DEBUG / 2
BasicLoggerClass = logging.getLoggerClass()


class TraceLogger(BasicLoggerClass):
    def __init__(self, name, level=logging.NOTSET):
        BasicLoggerClass.__init__(self, name, level)

    def trace(self, msg, *args, **kwargs):
        if self.isEnabledFor(TRACE_LOG_LEVEL):
            self._log(TRACE_LOG_LEVEL, msg, args, kwargs)


logging.addLevelName(TRACE_LOG_LEVEL, 'TRACE')
logging.setLoggerClass(TraceLogger)


def init_logger(log_directory, log_settings_file):
    if not os.path.exists(log_directory) or not os.path.isdir(log_directory):
        os.mkdir(log_directory)

    logging.basicConfig(
        stream=RotatingFileHandler(os.path.join(log_directory, RUNNING_LOG_FILENAME), maxBytes=RUNNING_LOG_MAX_BYTES,
                                   backupCount=RUNNING_LOG_BACKUP_COUNT),
        format=RUNNING_LOG_FORMAT,
        datefmt=RUNNING_LOG_DATE_FORMAT,
        level=logging.INFO
    )
    if log_settings_file:
        logging.config.fileConfig(log_settings_file, disable_existing_loggers=False)
