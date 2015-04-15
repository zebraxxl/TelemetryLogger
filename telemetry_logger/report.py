import os
import struct
import cPickle

from consts import ARGUMENT_COMMAND_PARAMETER, TEMPLATE_DIRECTORY_NAME, TEMPLATE_HTML_FILE_NAME, TEMPLATE_HEADER_BLOCK, \
    TEMPLATE_STYLE_FILES, ARGUMENT_OUTPUT, TEMPLATE_JS_FILES, FRAME_TYPE_TELEMETRY, FRAME_TYPE_MARKER, \
    TELEMETRY_PROCESSES, TELEMETRY_CPU_LOAD_AVG
from localization import get_string, UNKNOWN_TELEMETRY_TYPE
from graph_drawers.cpu_drawers import draw_cpu_loadavg
from utils import GraphIdCounter


__author__ = 'zebraxxl'

__GRAPH_DRAWERS = {
    TELEMETRY_CPU_LOAD_AVG: draw_cpu_loadavg,
}

__TELEMETRY_FAMILIES = {

}


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


def __make_header_block(template_path):
    result = ''
    for style_file_name in TEMPLATE_STYLE_FILES:
        with open(os.path.join(template_path, style_file_name), 'r') as f:
            result += '<style type="text/css">{0}</style>\n'.format(f.read())

    for js_file_name in TEMPLATE_JS_FILES:
        with open(os.path.join(template_path, js_file_name), 'r') as f:
            result += '<script type="text/javascript">{0}</script>'.format(f.read())

    return result


def __draw_graph(tel_type, values, blocks, settings, graph_id_counter):
    if tel_type not in __GRAPH_DRAWERS:
        blocks[get_string(tel_type)] = \
            '<div class="alert alert-danger" role="alert">{0}</div>'.format(get_string(UNKNOWN_TELEMETRY_TYPE))
        return ''
    else:
        marked_graph_id = graph_id_counter.mark_position()
        java_script = __GRAPH_DRAWERS[tel_type](values, settings, graph_id_counter)

        if tel_type in __TELEMETRY_FAMILIES:
            family_id = get_string(__TELEMETRY_FAMILIES[tel_type])
            if family_id not in blocks:
                blocks[family_id] = dict()
            blocks = blocks[family_id]

        tel_type_name = get_string(tel_type)
        blocks[tel_type_name] = ''
        for graph_id in graph_id_counter.get_generated_ids(marked_graph_id):
            blocks[tel_type_name] += '<div id="{0}"></div>'.format(graph_id)

        return java_script


def make_report(settings):
    frames = __read_all_frames(settings[ARGUMENT_COMMAND_PARAMETER])

    templates_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], TEMPLATE_DIRECTORY_NAME)
    with open(os.path.join(templates_path, TEMPLATE_HTML_FILE_NAME), 'r') as f:
        template = f.read()

    template = template.replace(TEMPLATE_HEADER_BLOCK, __make_header_block(templates_path))

    telemetries = dict()    # key: TELEMETRY_TYPE, value: list of tuples (datetime, value)
    markers = list()        # list of tuples (datetime, string)
    for frame in frames:
        if frame[1] == FRAME_TYPE_TELEMETRY:
            for tel_value in frame[2]:      # tel_value: tuple(type, value)
                if tel_value[0] == TELEMETRY_PROCESSES:
                    pass
                else:
                    if tel_value[0] not in telemetries:
                        telemetries[tel_value[0]] = list()
                    telemetries[tel_value[0]].append((frame[0], tel_value[1]))
        elif frame[1] == FRAME_TYPE_MARKER:
            markers.append((frame[0], frame[2]))

    # TODO: Override markers lines
    blocks = dict()
    draw_script = ''
    graph_id_counter = GraphIdCounter()
    for tel_type in telemetries:
        draw_script += __draw_graph(tel_type, telemetries[tel_type], blocks, settings, graph_id_counter)

    with open(settings[ARGUMENT_OUTPUT], 'w') as f:
        f.write(template)
