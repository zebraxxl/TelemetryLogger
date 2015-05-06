import struct
import cPickle
from telemetry_logger.consts import ARGUMENT_PROCESS_PID, ARGUMENT_PROCESS_PATH, ARGUMENT_PROCESS_REGEX, \
    ARGUMENT_PROCESS_PID_FILE, ARGUMENT_COMMAND_PARAMETER, FRAME_TYPE_TELEMETRY, TELEMETRY_PROCESSES, FRAME_TYPE_MARKER
from telemetry_logger.localization import get_string, PROCESS_FILTER_PATH_STRING, PROCESS_FILTER_REGEX_STRING, \
    PROCESS_FILTER_PID_FILE_STRING
from telemetry_logger.localization import PROCESS_FILTER_PID_STRING
from telemetry_logger.viewer.viewer_window import ViewerWindow


__author__ = 'pryanichnikov'


def __read_all_frames(file_name):
    input_file = open(file_name, 'rb')
    result = list()

    while True:
        frame_len_raw = input_file.read(4)
        if frame_len_raw == '':
            break

        frame_len = struct.unpack('<I', frame_len_raw)[0]
        raw_frame = input_file.read(frame_len)
        result.append(cPickle.loads(raw_frame))

    return result


def __get_process_filter_string(pattern):
    if pattern[0] == ARGUMENT_PROCESS_PID:
        return get_string(PROCESS_FILTER_PID_STRING).format(pattern[1])
    elif pattern[0] == ARGUMENT_PROCESS_PATH:
        return get_string(PROCESS_FILTER_PATH_STRING).format(pattern[1])
    elif pattern[0] == ARGUMENT_PROCESS_REGEX:
        return get_string(PROCESS_FILTER_REGEX_STRING).format(pattern[1].pattern)
    elif pattern[0] == ARGUMENT_PROCESS_PID_FILE:
        return get_string(PROCESS_FILTER_PID_FILE_STRING).format(pattern[1])
    else:
        return str(pattern)


def __merge_process_info(old_pi, new_pi):
    pi = old_pi[0]

    for v in pi:
        if str(new_pi[v]) not in str(pi[v]):
            pi[v] = str(pi[v]) + ', ' + str(new_pi[v])

    result = (pi, old_pi[1])
    return result


def view(settings):
    frames = __read_all_frames(settings[ARGUMENT_COMMAND_PARAMETER])

    # TODO: Share this code with report sub-module
    telemetries = dict()    # key: TELEMETRY_TYPE, value: list of tuples (datetime, value)
    markers = list()        # list of tuples (datetime, string)
    processes = dict()      # key: process filter, value: dict of key:pid, value:(process_info: dict, telemetries: dict)
    for frame in frames:
        if frame[1] == FRAME_TYPE_TELEMETRY:
            for tel_value in frame[2]:      # tel_value: tuple(type, value)
                if tel_value[0] == TELEMETRY_PROCESSES:
                    for process in tel_value[1]:
                        filter_string = __get_process_filter_string(process[0])
                        if filter_string not in processes:
                            processes[filter_string] = dict()

                        pid = process[1]['pid']
                        if pid not in processes[filter_string]:
                            processes[filter_string][pid] = (process[1], dict())
                        else:
                            processes[filter_string][pid] = __merge_process_info(processes[filter_string][pid],
                                                                                 process[1])
                        for p_tel_value in process[2]:
                            if p_tel_value[0] not in processes[filter_string][pid][1]:
                                processes[filter_string][pid][1][p_tel_value[0]] = list()
                            processes[filter_string][pid][1][p_tel_value[0]].append((frame[0], p_tel_value[1]))
                else:
                    if tel_value[0] not in telemetries:
                        telemetries[tel_value[0]] = list()
                    telemetries[tel_value[0]].append((frame[0], tel_value[1]))
        elif frame[1] == FRAME_TYPE_MARKER:
            markers.append((frame[0], frame[2]))

    window = ViewerWindow(settings, telemetries, processes, markers)
    window.show()
