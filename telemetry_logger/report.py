from datetime import datetime
import json
import re
import struct
import cPickle
from consts import ARGUMENT_COMMAND_PARAMETER, FRAME_TYPE_TELEMETRY, FRAME_TYPE_MARKER, SYSTEM_TELEMETRY, \
    TELEMETRY_PROCESSES, ARGUMENT_OUTPUT, JSON_DUMP_INDENT
from utils import check_dict_for_key

__author__ = 'zebraxxl'


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


def __merge_process_info_dict(f, s):
    pass


def __process_pattern_to_string(pattern):
    if isinstance(pattern, int):
        return 'Pid: {0}'.format(pattern)
    elif hasattr(pattern, 'pattern'):
        return 'Regular expression: {0}'.format(pattern.pattern)
    else:
        return str(pattern)


def __default_json_serializer(obj):
    if isinstance(obj, datetime):
        delta = obj - datetime.utcfromtimestamp(0)

        return int(delta.total_seconds() * 1000)
    else:
        pass


def make_report(settings):
    frames = __read_all_frames(settings[ARGUMENT_COMMAND_PARAMETER])

    system_telemetry = dict()
    processes = dict()
    markers = list()
    frames_ids = list()

    for frame in frames:
        frame_id = len(frames_ids)
        frames_ids.append(frame[0])

        if frame[1] == FRAME_TYPE_TELEMETRY:
            for telemetry_value in frame[2]:
                if telemetry_value[0] in SYSTEM_TELEMETRY:
                    check_dict_for_key(system_telemetry, telemetry_value[0], list)
                    system_telemetry[telemetry_value[0]].append((frame_id, telemetry_value[1]))
                elif telemetry_value[0] == TELEMETRY_PROCESSES:
                    for process_value in telemetry_value[1]:
                        pattern = __process_pattern_to_string(process_value[0][1])
                        process_info = process_value[1]

                        check_dict_for_key(processes, pattern, dict)
                        if process_info['pid'] not in processes[pattern]:
                            processes[pattern][process_info['pid']] = (process_info, dict())
                        else:
                            __merge_process_info_dict(processes[pattern][process_info['pid']][0], process_info)

                        process_telemetry = processes[pattern][process_info['pid']][1]

                        for process_telemetry_value in process_value[2]:
                            check_dict_for_key(process_telemetry, process_telemetry_value[0], list)
                            process_telemetry[process_telemetry_value[0]].append((frame_id, process_telemetry_value[1]))
                else:
                    pass

        elif frame[1] == FRAME_TYPE_MARKER:
            markers.append((frame[0], frame[2]))

    with open(settings[ARGUMENT_OUTPUT], 'w') as f:
        f.write('system_telemetry = {0}\n'.format(json.dumps(system_telemetry, indent=JSON_DUMP_INDENT)))
        f.write('processes = {0}\n'.format(json.dumps(processes, indent=JSON_DUMP_INDENT)))
        f.write('markers = {0}\n'.format(json.dumps(markers, default=__default_json_serializer, indent=JSON_DUMP_INDENT)))
        f.write('frames_ids = {0}\n'.format(json.dumps(frames_ids, default=__default_json_serializer, indent=JSON_DUMP_INDENT)))
