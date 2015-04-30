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
    TELEMETRY_DISK_IO_COUNTERS_PER_DISK, TELEMETRY_PROCESS_MEM_INFO, \
    TELEMETRY_PROCESS_MEM_PERCENT, ARGUMENT_PROCESS_PID, ARGUMENT_PROCESS_PATH, ARGUMENT_PROCESS_REGEX, \
    ARGUMENT_PROCESS_PID_FILE
from graph_drawers.disk_drawers import draw_disk_usage, draw_disk_io_counters, draw_disk_io_counters_per_disk
from graph_drawers.mem_drawers import draw_mem_system, draw_mem_swap, draw_proc_mem_info, draw_proc_mem_percent
from graph_drawers.net_drawers import draw_net_io_counters, draw_net_io_counters_per_nic
from localization import get_string, UNKNOWN_TELEMETRY_TYPE, SYSTEM_TELEMETRY_STRING, PROCESS_INFO_STRING, \
    TELEMETRY_STRING, PROCESSES_STRING, PROCESS_FILTER_PID_STRING, PROCESS_FILTER_PATH_STRING, \
    PROCESS_FILTER_REGEX_STRING, PID_STRING, PPID_STRING, CMD_LINE_STRING, EXE_STRING, STATUS_STRING, USERNAME_STRING, \
    UIDS_STRING, NAME_STRING, CWD_STRING, CREATE_TIME_STRING, TERMINAL_STRING, GIDS_STRING, \
    PROCESS_FILTER_PID_FILE_STRING
from graph_drawers.cpu_drawers import draw_cpu_loadavg, draw_cpu_times, draw_cpu_times_per_cpu, draw_cpu_percent, \
    draw_cpu_percent_per_cpu, draw_cpu_times_percent, draw_cpu_times_percent_per_cpu
from utils import GraphIdCounter, dump_javascript


__author__ = 'zebraxxl'

__GRAPH_DRAWERS = {
    TELEMETRY_CPU_LOAD_AVG: draw_cpu_loadavg,
    TELEMETRY_CPU_TIMES: draw_cpu_times,
    TELEMETRY_CPU_TIMES_PER_CPU: draw_cpu_times_per_cpu,
    TELEMETRY_CPU_PERCENT: draw_cpu_percent,
    TELEMETRY_CPU_PERCENT_PER_CPU: draw_cpu_percent_per_cpu,
    TELEMETRY_CPU_TIMES_PERCENT: draw_cpu_times_percent,
    TELEMETRY_CPU_TIMES_PERCENT_PER_CPU: draw_cpu_times_percent_per_cpu,

    TELEMETRY_MEM_SYSTEM: draw_mem_system,
    TELEMETRY_MEM_SWAP: draw_mem_swap,

    TELEMETRY_DISK_USAGE: draw_disk_usage,
    TELEMETRY_DISK_IO_COUNTERS: draw_disk_io_counters,
    TELEMETRY_DISK_IO_COUNTERS_PER_DISK: draw_disk_io_counters_per_disk,

    TELEMETRY_NET_IO_COUNTERS: draw_net_io_counters,
    TELEMETRY_NET_IO_COUNTERS_PER_NIC: draw_net_io_counters_per_nic,
}

__PROCESS_GRAPH_DRAWERS = {
    TELEMETRY_CPU_PERCENT: draw_cpu_percent,
    TELEMETRY_CPU_TIMES: draw_cpu_times,
    TELEMETRY_PROCESS_MEM_INFO: draw_proc_mem_info,
    TELEMETRY_PROCESS_MEM_PERCENT: draw_proc_mem_percent,
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

    TELEMETRY_PROCESS_MEM_INFO: TELEMETRY_FAMILY_MEM,
    TELEMETRY_PROCESS_MEM_PERCENT: TELEMETRY_FAMILY_MEM,
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


def __draw_graph(tel_type, values, blocks, settings, graph_id_counter, graph_drawers=__GRAPH_DRAWERS):
    if tel_type in __TELEMETRY_FAMILIES:
        family_id = get_string(__TELEMETRY_FAMILIES[tel_type])
        if family_id not in blocks:
            blocks[family_id] = dict()
        blocks = blocks[family_id]

    if tel_type not in graph_drawers:
        blocks[get_string(tel_type)] = \
            '<div class="alert alert-danger" role="alert">{0}</div>'.format(get_string(UNKNOWN_TELEMETRY_TYPE))
        return ''
    else:
        marked_graph_id = graph_id_counter.mark_position()
        java_script = graph_drawers[tel_type](values, settings, graph_id_counter)

        tel_type_name = get_string(tel_type)
        blocks[tel_type_name] = ''
        for graph_id in graph_id_counter.get_generated_ids(marked_graph_id):
            blocks[tel_type_name] += '<div id="{0}"></div>'.format(graph_id)

        draw_func_name = graph_id + '_draw_func'
        java_script = '''
        function {draw_func_name}(){{
            {draw_code}
        }}

        $("#{graph_id}").parent().parent().on("shown.bs.collapse", function() {{
            {draw_func_name}();
        }});
        '''.format(
            draw_func_name=draw_func_name,
            draw_code=java_script,
            graph_id=graph_id
        )

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


def __get_html_for_process_info(pi):
    return '''
    <table class="table table-striped table-bordered"><tbody>
        <tr><td>{pid_string}</td><td>{pid}</td><td>{ppid_string}</td><td>{ppid}</td></tr>
        <tr><td>{cmd_line_string}</td><td>{cmd_line}</td><td>{name_string}</td><td>{name}</td></tr>
        <tr><td>{exe_string}</td><td>{exe}</td><td>{cwd_string}</td><td>{cwd}</td></tr>
        <tr><td>{status_string}</td><td>{status}</td><td>{create_time_string}</td><td>{create_time}</td></tr>
        <tr><td>{username_string}</td><td>{username}</td><td>{terminal_string}</td><td>{terminal}</td></tr>
        <tr><td>{uids_string}</td><td>{uids}</td><td>{gids_string}</td><td>{gids}</td></tr>
    </tbody></table>
    '''.format(**{
        'pid_string': PID_STRING,
        'ppid_string': PPID_STRING,
        'cmd_line_string': CMD_LINE_STRING,
        'exe_string': EXE_STRING,
        'status_string': STATUS_STRING,
        'username_string': USERNAME_STRING,
        'uids_string': UIDS_STRING,
        'name_string': NAME_STRING,
        'cwd_string': CWD_STRING,
        'create_time_string': CREATE_TIME_STRING,
        'terminal_string': TERMINAL_STRING,
        'gids_string': GIDS_STRING,
        'pid': pi['pid'],
        'ppid': pi['ppid'],
        'cmd_line': pi['cmd_line'],
        'name': pi['name'],
        'exe': pi['exe'],
        'cwd': pi['cwd'],
        'status': pi['status'],
        'create_time': pi['create_time'],
        'username': pi['username'],
        'terminal': pi['terminal'],
        'uids': pi['uids'],
        'gids': pi['gids'],
    })


def make_report(settings):
    frames = __read_all_frames(settings[ARGUMENT_COMMAND_PARAMETER])

    templates_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], TEMPLATE_DIRECTORY_NAME)
    with open(os.path.join(templates_path, TEMPLATE_HTML_FILE_NAME), 'r') as f:
        template = f.read()

    template = template.replace(TEMPLATE_HEADER_BLOCK, __make_header_block(templates_path))

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

    processes_blocks = dict()
    for process_filter in processes:
        processes_blocks[process_filter] = dict()
        pids = processes[process_filter]

        for pid in pids:
            pid_str = str(pid)
            processes_blocks[process_filter][pid_str] = dict()
            processes_blocks[process_filter][pid_str][get_string(PROCESS_INFO_STRING)] = \
                __get_html_for_process_info(pids[pid][0])
            processes_blocks[process_filter][pid_str][get_string(TELEMETRY_STRING)] = dict()
            for tel_type in pids[pid][1]:
                draw_script += __draw_graph(tel_type, pids[pid][1][tel_type],
                                            processes_blocks[process_filter][pid_str][get_string(TELEMETRY_STRING)],
                                            settings, graph_id_counter, __PROCESS_GRAPH_DRAWERS)
    content += __get_html_for_block(get_string(PROCESSES_STRING), processes_blocks, graph_id_counter)

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
