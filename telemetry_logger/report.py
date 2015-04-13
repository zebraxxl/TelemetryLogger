from datetime import datetime
import os
import struct
import cPickle
from consts import ARGUMENT_COMMAND_PARAMETER, TEMPLATE_DIRECTORY_NAME, TEMPLATE_HTML_FILE_NAME, TEMPLATE_HEADER_BLOCK, \
    TEMPLATE_STYLE_FILES, ARGUMENT_OUTPUT, TEMPLATE_JS_FILES

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


def __make_header_block(template_path):
    result = ''
    for style_file_name in TEMPLATE_STYLE_FILES:
        with open(os.path.join(template_path, style_file_name), 'r') as f:
            result += '<style type="text/css">{0}</style>\n'.format(f.read())

    for js_file_name in TEMPLATE_JS_FILES:
        with open(os.path.join(template_path, js_file_name), 'r') as f:
            result += '<script type="text/javascript">{0}</script>'.format(f.read())

    return result


def make_report(settings):
    frames = __read_all_frames(settings[ARGUMENT_COMMAND_PARAMETER])

    templates_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], TEMPLATE_DIRECTORY_NAME)
    with open(os.path.join(templates_path, TEMPLATE_HTML_FILE_NAME), 'r') as f:
        template = f.read()

    template = template.replace(TEMPLATE_HEADER_BLOCK, __make_header_block(templates_path))

    with open(settings[ARGUMENT_OUTPUT], 'w') as f:
        f.write(template)
