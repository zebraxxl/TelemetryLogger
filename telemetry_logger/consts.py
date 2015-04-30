import platform
import sys
import logging

__author__ = 'zebraxxl'

PICKLE_PROTOCOL_VERSION = 2

PLATFORM_DEFAULT_PID_FILE = 'default_pid_file'
PLATFORM_DEFAULT_LOG_DIRECTORY = 'default_log_directory'


def get_platform_data():
    system = platform.system()

    if system == 'Linux':
        return {
            PLATFORM_DEFAULT_PID_FILE: '/tmp/telemetry_logger.pid',
            PLATFORM_DEFAULT_LOG_DIRECTORY: '/var/log/TelemetryLogger/',
        }
    else:
        logging.error('"{0}" system not supported'.format(system))
        sys.exit(1)


PLATFORM_DATA = get_platform_data()

FRAME_TYPE_TELEMETRY = 0
FRAME_TYPE_MARKER = 1

TELEMETRY_PROCESSES = 'PROCESSES'

TELEMETRY_CPU_LOAD_AVG = 'CPU_LOAD_AVG'
TELEMETRY_CPU_TIMES = 'CPU_TIMES'
TELEMETRY_CPU_TIMES_PER_CPU = 'CPU_TIMES_PER_CPU'
TELEMETRY_CPU_PERCENT = 'CPU_PERCENT'
TELEMETRY_CPU_PERCENT_PER_CPU = 'CPU_PERCENT_PER_CPU'
TELEMETRY_CPU_TIMES_PERCENT = 'CPU_TIMES_PERCENT'
TELEMETRY_CPU_TIMES_PERCENT_PER_CPU = 'CPU_TIMES_PERCENT_PER_CPU'

TELEMETRY_MEM_SYSTEM = 'MEM_SYSTEM'
TELEMETRY_MEM_SWAP = 'MEM_SWAP'

TELEMETRY_DISK_USAGE = 'DISK_USAGE'
TELEMETRY_DISK_IO_COUNTERS = 'DISK_IO_COUNTERS'
TELEMETRY_DISK_IO_COUNTERS_PER_DISK = 'DISK_IO_COUNTERS_PER_DISK'

TELEMETRY_NET_IO_COUNTERS = 'NET_IO_COUNTERS'
TELEMETRY_NET_IO_COUNTERS_PER_NIC = 'NET_IO_COUNTERS_PER_NIC'

TELEMETRY_PROCESS_MEM_INFO = 'PROC_MEM_INFO'
TELEMETRY_PROCESS_MEM_PERCENT = 'PROC_MEM_PERCENT'

ALL_TELEMETRY = frozenset([
    TELEMETRY_CPU_LOAD_AVG, TELEMETRY_CPU_TIMES, TELEMETRY_CPU_TIMES_PER_CPU, TELEMETRY_CPU_PERCENT,
    TELEMETRY_CPU_PERCENT_PER_CPU, TELEMETRY_CPU_TIMES_PERCENT, TELEMETRY_CPU_TIMES_PERCENT_PER_CPU,

    TELEMETRY_MEM_SYSTEM, TELEMETRY_MEM_SWAP,

    TELEMETRY_DISK_USAGE, TELEMETRY_DISK_IO_COUNTERS, TELEMETRY_DISK_IO_COUNTERS_PER_DISK,

    TELEMETRY_NET_IO_COUNTERS, TELEMETRY_NET_IO_COUNTERS_PER_NIC,

    TELEMETRY_PROCESS_MEM_INFO, TELEMETRY_PROCESS_MEM_PERCENT,
])

SYSTEM_TELEMETRY = frozenset([
    TELEMETRY_CPU_LOAD_AVG, TELEMETRY_CPU_TIMES, TELEMETRY_CPU_TIMES_PER_CPU, TELEMETRY_CPU_PERCENT,
    TELEMETRY_CPU_PERCENT_PER_CPU, TELEMETRY_CPU_TIMES_PERCENT, TELEMETRY_CPU_TIMES_PERCENT_PER_CPU,

    TELEMETRY_MEM_SYSTEM, TELEMETRY_MEM_SWAP,

    TELEMETRY_DISK_USAGE, TELEMETRY_DISK_IO_COUNTERS, TELEMETRY_DISK_IO_COUNTERS_PER_DISK,

    TELEMETRY_NET_IO_COUNTERS, TELEMETRY_NET_IO_COUNTERS_PER_NIC,
])

TELEMETRY_TYPES_DELIMITER = ';'

OUTPUT_MODULE_FILE = 'file'
OUTPUT_MODULE_NET = 'net'
ALL_OUTPUT_MODULES = frozenset([OUTPUT_MODULE_FILE, OUTPUT_MODULE_NET])

INPUT_MODULE_SYSTEM = 'system'
INPUT_MODULE_NET = 'net'
ALL_INPUT_MODULES = frozenset([INPUT_MODULE_SYSTEM, INPUT_MODULE_NET])

ARGUMENT_SHOW_HELP = 'show_help'
ARGUMENT_COMMAND = 'command'
ARGUMENT_PID_FILE = 'pid_file'
ARGUMENT_CONTROL_ADDR = 'control_addr'
ARGUMENT_CONTROL_PORT = 'control_port'
ARGUMENT_TELEMETRY_TYPES = 'telemetry_types'
ARGUMENT_PROCESSES = 'processes'
ARGUMENT_CONFIG_FILE = 'config_file'
ARGUMENT_OUTPUT = 'output'
ARGUMENT_INTERVAL = 'interval'
ARGUMENT_SPLIT_GRAPHS = 'split_graphs'
ARGUMENT_SUB_CHART = 'sub_chart'
ARGUMENT_OUTPUT_MODULE = 'output_module'
ARGUMENT_INPUT_MODULE = 'input_module'
ARGUMENT_INPUT_ADDRESS = 'input_address'
ARGUMENT_INPUT_PORT = 'input_port'
ARGUMENT_SHOW_GRAPH_POINTS = 'show_graph_points'
ARGUMENT_RUNNING_LOG_CONFIG = 'running_log_config'
ARGUMENT_DEBUG = 'debug'

ARGUMENT_PROCESS_PID = 'process_pid'
ARGUMENT_PROCESS_PATH = 'process_path'
ARGUMENT_PROCESS_REGEX = 'process_regex'
ARGUMENT_PROCESS_PID_FILE = 'process_pid_file'

ARGUMENT_COMMAND_PARAMETER = 'command_parameter'

ARGUMENTS_DEFAULT = {
    ARGUMENT_SHOW_HELP: False,
    ARGUMENT_COMMAND: None,
    ARGUMENT_COMMAND_PARAMETER: None,
    ARGUMENT_PID_FILE: PLATFORM_DATA[PLATFORM_DEFAULT_PID_FILE],
    ARGUMENT_CONTROL_ADDR: '127.0.0.1',
    ARGUMENT_CONTROL_PORT: 23051,
    ARGUMENT_TELEMETRY_TYPES: set(),
    ARGUMENT_PROCESSES: [],
    ARGUMENT_OUTPUT: None,
    ARGUMENT_INTERVAL: 1.0,
    ARGUMENT_SPLIT_GRAPHS: False,
    ARGUMENT_SUB_CHART: False,
    ARGUMENT_OUTPUT_MODULE: OUTPUT_MODULE_FILE,
    ARGUMENT_INPUT_MODULE: INPUT_MODULE_SYSTEM,
    ARGUMENT_INPUT_ADDRESS: '',
    ARGUMENT_INPUT_PORT: 23052,
    ARGUMENT_DEBUG: False,
    ARGUMENT_SHOW_GRAPH_POINTS: False,
    ARGUMENT_RUNNING_LOG_CONFIG: None,
}

COMMAND_START = 'start'
COMMAND_STOP = 'stop'
COMMAND_RESTART = 'restart'
COMMAND_MARKER = 'marker'
COMMAND_REPORT = 'report'

ALL_COMMANDS = frozenset([COMMAND_START, COMMAND_STOP, COMMAND_RESTART, COMMAND_MARKER, COMMAND_REPORT])

MAX_VALID_PORT = 65535

PROCESS_INFO_PID = 'pid'
PROCESS_INFO_PPID = 'ppid'
PROCESS_INFO_NAME = 'name'
PROCESS_INFO_EXE = 'exe'
PROCESS_INFO_CMDLINE = 'cmd_line'
PROCESS_INFO_CREATE_TIME = 'create_time'
PROCESS_INFO_STATUS = 'status'
PROCESS_INFO_CWD = 'cwd'
PROCESS_INFO_USERNAME = 'username'
PROCESS_INFO_UIDS = 'uids'
PROCESS_INFO_GIDS = 'gids'
PROCESS_INFO_TERMINAL = 'terminal'

REMOTE_COMMAND_MARKER = 'marker'
REMOTE_COMMAND_MARKER_NAME = 'name'

TEMPLATE_SCRIPTS_INDENT = 2
TEMPLATE_DIRECTORY_NAME = 'template'
TEMPLATE_HTML_FILE_NAME = 'template.html'
TEMPLATE_HEADER_BLOCK = '{{ header_block }}'
TEMPLATE_CONTENT_BLOCK = '{{ content_block }}'
TEMPLATE_END_BLOCK = '{{ end_block }}'
TEMPLATE_STYLE_FILES = ['css/bootstrap.min.css', 'css/c3.min.css']
TEMPLATE_JS_FILES = ['js/jquery.min.js', 'js/bootstrap.min.js', 'js/d3.min.js', 'js/c3.min.js']

JS_VAR_MARKERS_LINES = 'markers_lines'

TELEMETRY_FAMILY_CPU = 'FAMILY_CPU'
TELEMETRY_FAMILY_MEM = 'FAMILY_MEM'
TELEMETRY_FAMILY_DISK = 'FAMILY_DISK'
TELEMETRY_FAMILY_NET = 'FAMILY_NET'
