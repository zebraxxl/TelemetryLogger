import os
import struct
import cPickle

from consts import ARGUMENT_COMMAND_PARAMETER, TEMPLATE_DIRECTORY_NAME, TEMPLATE_HTML_FILE_NAME, TEMPLATE_HEADER_BLOCK, \
    TEMPLATE_STYLE_FILES, ARGUMENT_OUTPUT, TEMPLATE_JS_FILES, FRAME_TYPE_TELEMETRY, FRAME_TYPE_MARKER, \
    TELEMETRY_PROCESSES, TELEMETRY_CPU_LOAD_AVG, TEMPLATE_CONTENT_BLOCK, TEMPLATE_END_BLOCK, JS_VAR_MARKERS_LINES, \
    TELEMETRY_FAMILY_CPU, TELEMETRY_CPU_TIMES, TELEMETRY_CPU_TIMES_PER_CPU, TELEMETRY_CPU_TIMES_PERCENT_PER_CPU, \
    TELEMETRY_CPU_PERCENT, TELEMETRY_CPU_PERCENT_PER_CPU, TELEMETRY_CPU_TIMES_PERCENT, TELEMETRY_MEM_SYSTEM, \
    TELEMETRY_MEM_SWAP, TELEMETRY_FAMILY_MEM, TELEMETRY_NET_IO_COUNTERS, TELEMETRY_NET_IO_COUNTERS_PER_NIC, \
    TELEMETRY_FAMILY_NET, TELEMETRY_FAMILY_DISK, TELEMETRY_DISK_USAGE, TELEMETRY_DISK_IO_COUNTERS, \
    TELEMETRY_DISK_IO_COUNTERS_PER_DISK, TELEMETRY_PROCESS_CPU_AFFINITY, TELEMETRY_PROCESS_MEM_INFO, \
    TELEMETRY_PROCESS_MEM_PERCENT
from localization import get_string, UNKNOWN_TELEMETRY_TYPE, SYSTEM_TELEMETRY_STRING
from graph_drawers.cpu_drawers import draw_cpu_loadavg, draw_cpu_times, draw_cpu_times_per_cpu, draw_cpu_percent, \
    draw_cpu_percent_per_cpu
from utils import GraphIdCounter, dump_javascript


__author__ = 'zebraxxl'

__GRAPH_DRAWERS = {
    TELEMETRY_CPU_LOAD_AVG: draw_cpu_loadavg,
    TELEMETRY_CPU_TIMES: draw_cpu_times,
    TELEMETRY_CPU_TIMES_PER_CPU: draw_cpu_times_per_cpu,
    TELEMETRY_CPU_PERCENT: draw_cpu_percent,
    TELEMETRY_CPU_PERCENT_PER_CPU: draw_cpu_percent_per_cpu,
}

__TELEMETRY_FAMILIES = {
    TELEMETRY_CPU_LOAD_AVG: TELEMETRY_FAMILY_CPU,
    TELEMETRY_CPU_TIMES: TELEMETRY_FAMILY_CPU,
    TELEMETRY_CPU_TIMES_PER_CPU: TELEMETRY_FAMILY_CPU,
    TELEMETRY_CPU_PERCENT: TELEMETRY_FAMILY_CPU,
    TELEMETRY_CPU_PERCENT_PER_CPU: TELEMETRY_FAMILY_CPU,
    TELEMETRY_CPU_TIMES_PERCENT: TELEMETRY_FAMILY_CPU,
    TELEMETRY_CPU_TIMES_PERCENT_PER_CPU: TELEMETRY_FAMILY_CPU,

    TELEMETRY_MEM_SYSTEM: TELEMETRY_FAMILY_MEM,
    TELEMETRY_MEM_SWAP: TELEMETRY_FAMILY_MEM,

    TELEMETRY_DISK_USAGE: TELEMETRY_FAMILY_DISK,
    TELEMETRY_DISK_IO_COUNTERS: TELEMETRY_FAMILY_DISK,
    TELEMETRY_DISK_IO_COUNTERS_PER_DISK: TELEMETRY_FAMILY_DISK,

    TELEMETRY_NET_IO_COUNTERS: TELEMETRY_FAMILY_NET,
    TELEMETRY_NET_IO_COUNTERS_PER_NIC: TELEMETRY_FAMILY_NET,

    TELEMETRY_PROCESS_CPU_AFFINITY: TELEMETRY_FAMILY_CPU,
    TELEMETRY_PROCESS_MEM_INFO: TELEMETRY_FAMILY_CPU,
    TELEMETRY_PROCESS_MEM_PERCENT: TELEMETRY_FAMILY_CPU,
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
    if tel_type in __TELEMETRY_FAMILIES:
        family_id = get_string(__TELEMETRY_FAMILIES[tel_type])
        if family_id not in blocks:
            blocks[family_id] = dict()
        blocks = blocks[family_id]

    if tel_type not in __GRAPH_DRAWERS:
        blocks[get_string(tel_type)] = \
            '<div class="alert alert-danger" role="alert">{0}</div>'.format(get_string(UNKNOWN_TELEMETRY_TYPE))
        return ''
    else:
        marked_graph_id = graph_id_counter.mark_position()
        java_script = __GRAPH_DRAWERS[tel_type](values, settings, graph_id_counter)

        tel_type_name = get_string(tel_type)
        blocks[tel_type_name] = ''
        for graph_id in graph_id_counter.get_generated_ids(marked_graph_id):
            blocks[tel_type_name] += '<div id="{0}"></div>'.format(graph_id)

        return java_script


def __get_html_for_block(title, content,  graph_id_counter):
    block_id = graph_id_counter.get_next_value()
    block_id_name = block_id + '_name'
    block_id_body = block_id + '_body'

    if isinstance(content, dict):
        c = ''
        for v in content:
            c += __get_html_for_block(v, content[v], graph_id_counter)
        content = c

    result = '''<div class="panel panel-default">
                    <div class="panel-heading" role="tab" id="{name}">
                        <h4 class="panel-title">
                            <a data-toggle="collapse" href="#{body}" aria-expanded="true" aria-controls="{body}">
                                {title}
                            </a>
                        </h4>
                    </div>
                    <div id="{body}" class="panel-collapse collapse in" role="tabpanel" aria-labelledby="{name}">
                        <div class="panel-body">
                            {content}
                        </div>
                    </div>
                </div>'''.format(name=block_id_name, body=block_id_body, title=title, content=content)

    return result


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

    js_markers = []
    for marker in markers:
        js_markers.append({
            'value': marker[0].strftime('%H:%M:%S.%f')[:-3],
            'text': marker[1],
            'position': 'start',
        })

    blocks = dict()
    draw_script = '{0} = {1};\n'.format(JS_VAR_MARKERS_LINES, dump_javascript(js_markers))
    graph_id_counter = GraphIdCounter()
    for tel_type in telemetries:
        draw_script += __draw_graph(tel_type, telemetries[tel_type], blocks, settings, graph_id_counter)

    content = __get_html_for_block(get_string(SYSTEM_TELEMETRY_STRING), blocks, graph_id_counter)
    template = template.replace(TEMPLATE_CONTENT_BLOCK, content)
    template = template.replace(TEMPLATE_END_BLOCK,
                                '''<script type="text/javascript">
                                    $(function(){{
                                        {0}
                                        $('.collapse .in').removeClass('in');
                                    }});
                                    </script>'''.format(draw_script))

    with open(settings[ARGUMENT_OUTPUT], 'w') as f:
        f.write(template)
