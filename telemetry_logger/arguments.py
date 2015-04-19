import json
from logger import error, warning
import re
import sys
from consts import ARGUMENTS_DEFAULT, ARGUMENT_PID_FILE, ARGUMENT_CONTROL_ADDR, \
    ARGUMENT_CONTROL_PORT, ARGUMENT_TELEMETRY_TYPES, ARGUMENT_PROCESSES, ARGUMENT_SHOW_HELP, TELEMETRY_TYPES_DELIMITER, \
    ALL_TELEMETRY, ARGUMENT_PROCESS_REGEX, ARGUMENT_PROCESS_PATH, ARGUMENT_PROCESS_PID, ARGUMENT_CONFIG_FILE, ARGUMENT_OUTPUT, \
    ARGUMENT_INTERVAL, ALL_COMMANDS, ARGUMENT_COMMAND, COMMAND_MARKER, ARGUMENT_COMMAND_PARAMETER, MAX_VALID_PORT, \
    COMMAND_START, COMMAND_REPORT, ARGUMENT_SPLIT_GRAPHS, ARGUMENT_SUB_CHART, ARGUMENT_OUTPUT_MODULE, ALL_OUTPUT_MODULES, \
    ARGUMENT_INPUT_MODULE
from utils import try_to_int

__author__ = 'zebraxxl'

__only_write_arguments = frozenset({ARGUMENT_PID_FILE, ARGUMENT_CONTROL_ADDR, ARGUMENT_CONTROL_PORT, ARGUMENT_OUTPUT,
                                    ARGUMENT_INTERVAL, ARGUMENT_OUTPUT_MODULE, ARGUMENT_INPUT_MODULE})
__process_arguments = frozenset({ARGUMENT_PROCESS_PID, ARGUMENT_PROCESS_PATH, ARGUMENT_PROCESS_REGEX})
__command_need_output = frozenset({COMMAND_START, COMMAND_REPORT})
__command_need_parameter = frozenset({COMMAND_MARKER, COMMAND_REPORT})
__arguments_flags = frozenset({ARGUMENT_SPLIT_GRAPHS, ARGUMENT_SUB_CHART})

__cf_process_type = 'type'
__cf_process_value = 'value'


def __parse_config_file(file_name, result):
    try:
        with open(file_name, 'r') as config_file:
            config = json.load(config_file)

        if not isinstance(config, dict):
            error('Invalid config file {0}. Expected dict as root object.', file_name)

        for arg in config:
            if arg in __only_write_arguments:
                result[arg] = config[arg]
            elif arg in __arguments_flags:
                result[arg] = config[arg]
            elif arg == ARGUMENT_TELEMETRY_TYPES:
                if not isinstance(config[arg], list):
                    error('Expected list type for argument {1}.', arg)
                    continue
                for telemetry_type in config[arg]:
                    if telemetry_type in ALL_TELEMETRY:
                        result[ARGUMENT_TELEMETRY_TYPES].add(telemetry_type)
                    else:
                        warning('Telemetry type {0} is unknown. Skipping it.', telemetry_type)
            elif arg == ARGUMENT_PROCESSES:
                if not isinstance(config[arg], list):
                    error('Expected list type for argument {1}.', arg)
                    continue
                for process in config[arg]:
                    if not isinstance(process, dict):
                        error('Expected dict type for process argument')
                        continue
                    if __cf_process_type not in process.keys() or __cf_process_value not in process.keys():
                        error('Invalid process dictionary')
                        continue
                    process_type = process[__cf_process_type]
                    process_value = process[__cf_process_value]
                    if process_type not in __process_arguments:
                        error('Unknown process argument type: {0}', process_type)
                        continue
                    result[ARGUMENT_PROCESSES].append((process_type, process_value))
            else:
                warning('Unknown argument {0} in config file {1}', arg, file_name)
    except ValueError as e:
        error('Error while parsing json in config file {0}: {1}', file_name, e)
    except IOError as e:
        error('IO error while processing config file {0}: {1}', file_name, e)
    except Exception as e:
        error('Unexpected error while processing config file {0}: {1}', file_name, e)


def __parse_argument(name, i, result):
    if name in __only_write_arguments:
        result[name] = sys.argv[i + 1]
        return i + 2
    elif name in __arguments_flags:
        result[name] = True
        return i + 1
    elif name == 'help':
        result[ARGUMENT_SHOW_HELP] = True
        return i + 1
    elif name == ARGUMENT_TELEMETRY_TYPES:
        telemetry_types = sys.argv[i + 1].split(TELEMETRY_TYPES_DELIMITER)
        for telemetry_type in telemetry_types:
            if telemetry_type in ALL_TELEMETRY:
                result[ARGUMENT_TELEMETRY_TYPES].add(telemetry_type)
            else:
                warning('Telemetry type {0} is unknown. Skipping it.', telemetry_type)
        return i + 2
    elif name in __process_arguments:
        process = (name, sys.argv[i + 1])
        result[ARGUMENT_PROCESSES].append(process)
        return i + 2
    elif name == ARGUMENT_CONFIG_FILE:
        __parse_config_file(sys.argv[i + 1], result)
        return i + 2
    else:
        warning('Passed argument {0} is unknown. Skipping it.', name)
        return i + 1


def __validate_settings(result):
    # ARGUMENT_CONTROL_PORT
    value = result[ARGUMENT_CONTROL_PORT]
    if not isinstance(value, int):
        value = try_to_int(value)
        if value is None:
            error('Argument {0} is not valid port. Setting it to default {1}.', ARGUMENT_CONTROL_PORT,
                  ARGUMENTS_DEFAULT[ARGUMENT_CONTROL_PORT])
            value = ARGUMENTS_DEFAULT[ARGUMENT_CONTROL_PORT]
    if (0 > value) or (value > MAX_VALID_PORT):
        error('Argument {0} is not valid port. Setting it to default {1}.', ARGUMENT_CONTROL_PORT,
              ARGUMENTS_DEFAULT[ARGUMENT_CONTROL_PORT])
        value = ARGUMENTS_DEFAULT[ARGUMENT_CONTROL_PORT]
    result[ARGUMENT_CONTROL_PORT] = value

    # ARGUMENT_PROCESSES
    for process in result[ARGUMENT_PROCESSES]:
        if process[0] == ARGUMENT_PROCESS_PID:
            value = process[1]
            if not isinstance(value, int):
                result[ARGUMENT_PROCESSES].remove(process)
                value = try_to_int(value)
                if value is None:
                    error('{0} is not valid pid. Removing it.', process[1])
                else:
                    result[ARGUMENT_PROCESSES].append((ARGUMENT_PROCESS_PID, value))
        elif process[0] == ARGUMENT_PROCESS_REGEX:
            result[ARGUMENT_PROCESSES].remove(process)
            try:
                value = re.compile(process[1])
            except error as v:
                error('{0} is not valid regular expression ({1})', process[1], v)
            else:
                result[ARGUMENT_PROCESSES].append((ARGUMENT_PROCESS_REGEX, value))

    # ARGUMENT_INTERVAL
    value = result[ARGUMENT_INTERVAL]
    if not isinstance(value, float):
        value = try_to_int(value)
        if value is None:
            error('{0} is not valid interval value. Using default {1}', result[ARGUMENT_INTERVAL],
                  ARGUMENTS_DEFAULT[ARGUMENT_INTERVAL])
            value = ARGUMENTS_DEFAULT[ARGUMENT_INTERVAL]
        result[ARGUMENT_INTERVAL] = value


def __show_help(result):
    if result[ARGUMENT_SHOW_HELP]:
        return True
    if result[ARGUMENT_COMMAND] is None:
        if len(sys.argv) > 1:
            error('Command not specified')
        return True
    if result[ARGUMENT_COMMAND] in __command_need_output and result[ARGUMENT_OUTPUT] is None:
        error('Output file not specified')
        return True
    return False


def __get_supported_line(temp_all_telemetry):
    supported_telemetry_types_lines = list()
    supported_telemetry_types_lines.append(temp_all_telemetry[0])
    for i in xrange(1, len(temp_all_telemetry)):
        new_line_len = len(supported_telemetry_types_lines[-1]) + 2 + len(temp_all_telemetry[i])
        if new_line_len <= 80:
            supported_telemetry_types_lines[-1] = supported_telemetry_types_lines[-1] + ', ' + temp_all_telemetry[i]
        else:
            supported_telemetry_types_lines[-1] += ','
            supported_telemetry_types_lines.append('    ' + temp_all_telemetry[i])
    supported_telemetry_types = '\n'.join(supported_telemetry_types_lines)
    return supported_telemetry_types


def process_settings():
    result = ARGUMENTS_DEFAULT

    args_len = len(sys.argv)
    i = 1

    while i < args_len:
        arg = sys.argv[i]
        if arg.startswith('--'):
            i = __parse_argument(arg[2:], i, result)
        elif arg.startswith('-'):
            i = __parse_argument(arg[1:], i, result)
        elif arg in ALL_COMMANDS:
            if result[ARGUMENT_COMMAND] is None:
                result[ARGUMENT_COMMAND] = arg
                i += 1
                if arg in __command_need_parameter:
                    result[ARGUMENT_COMMAND_PARAMETER] = sys.argv[i]
                    i += 1
            else:
                warning('Duplicated command. Skip second.')
        else:
            warning('Command {0} unknown. Skipping it.', arg)
            i += 1

    if __show_help(result):
        supported_telemetry_types = __get_supported_line(list(ALL_TELEMETRY))
        supported_output_modules = __get_supported_line(list(ALL_OUTPUT_MODULES))

        print('Usage: {program_name} COMMAND [PARAMETER] [SETTING] ...\n'
              'Valid commands with parameters:\n'
              '    start        - start telemetry logger daemon\n'
              '    stop         - stop telemetry logger daemon\n'
              '    restart      - restart telemetry logger daemon with new settings\n'
              '    marker NAME  - add time marker with name NAME\n'
              '    report FILE  - generate report file from telemetry log in FILE\n'
              'Valid settings:\n'
              '    --help                 - show this help message\n'
              '    --interval INTERVAL    - set interval for logging telemetry in seconds\n'
              '    --output_module MODULE - set output module to MODULE\n'
              '    --output OUTPUT        - output data to OUTPUT.\n'
              '                             OUTPUT value depends of output module\n'
              '    --input_module INPUT   - set input module to MODULE\n'
              '    --pid_file FILE        - save pid of running telemetry logger in FILE\n'
              '    --control_addr ADDR    - listen for or send control commands on ADDR address\n'
              '    --control_port PORT    - listen for or send control commands on PORT port\n'
              '    --telemetry_type TYPES - set logging telemetry types to TYPES.\n'
              '                             TYPES must be divided by "{telemetry_types_divide}" symbol\n'
              '    --process_pid PID      - log telemetry for process with pid PID\n'
              '    --process_path PATH    - log telemetry for processes whose executable file\n'
              '                             is located in PATH\n'
              '    --process_regex REGEX  - log telemetry for processes whose command line\n'
              '                             matches the regular expression REGEX\n'
              '    --config_file FILE     - load settings from file FILE\n'
              '    --split_graphs         - split multiple graphs in report\n'
              '    --sub_chart            - show sub chart\n'
              'Supported telemetry types:\n'
              '    {supported_telemetry_types}\n'
              'Supported output modules:\n'
              '    {supported_output_modules}\n'
              'Default values for settings:\n'
              '    interval         {default_interval} sec\n'
              '    output_module    {default_output_module}\n'
              '    input_module     {default_input_module}\n'
              '    pid_file         {default_pid_file}\n'
              '    control_addr     {default_control_addr}\n'
              '    control_port     {default_control_port}\n'
              '    telemetry_type   all supported\n'
              '    split_graphs     {default_split_graphs}\n'
              '    sub_char         {default_sub_chart}'
              .format(program_name=sys.argv[0],
                      telemetry_types_divide=TELEMETRY_TYPES_DELIMITER,
                      supported_telemetry_types=supported_telemetry_types,
                      supported_output_modules=supported_output_modules,
                      default_interval=ARGUMENTS_DEFAULT[ARGUMENT_INTERVAL],
                      default_output_module=ARGUMENTS_DEFAULT[ARGUMENT_OUTPUT_MODULE],
                      default_input_module=ARGUMENTS_DEFAULT[ARGUMENT_INPUT_MODULE],
                      default_pid_file=ARGUMENTS_DEFAULT[ARGUMENT_PID_FILE],
                      default_control_addr=ARGUMENTS_DEFAULT[ARGUMENT_CONTROL_ADDR],
                      default_control_port=ARGUMENTS_DEFAULT[ARGUMENT_CONTROL_PORT],
                      default_split_graphs=ARGUMENTS_DEFAULT[ARGUMENT_SPLIT_GRAPHS],
                      default_sub_chart=ARGUMENTS_DEFAULT[ARGUMENT_SUB_CHART]))
        return None

    __validate_settings(result)

    if len(result[ARGUMENT_TELEMETRY_TYPES]) == 0:
        result[ARGUMENT_TELEMETRY_TYPES] = ALL_TELEMETRY

    return result
