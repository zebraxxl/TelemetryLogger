function make_system_telemetry_blocks() {
    result = {
    }

    for (telemetry_type in system_telemetry) {
        var parent_block = result;
        var parent_block_id = 'system_telemetry_';

        if (typeof(telemetry2block[telemetry_type]) != 'undefined') {
            if (typeof(result[telemetry2block[telemetry_type]]) == 'undefined')
                result[telemetry2block[telemetry_type]] = {}
            parent_block = result[telemetry2block[telemetry_type]];
            parent_block_id += telemetry2block[telemetry_type] + '_';
        }

        parent_block[telemetry_type] = draw_graph(telemetry_type, parent_block_id + telemetry_type,
            system_telemetry[telemetry_type]);
    }

    return result;
}

function format_process_info(pi) {
    var result = '<table class="table table-striped table-bordered"><tbody>';

    uids = pi['uids'].join(', ');
    gids = pi['gids'].join(', ');

    result += '<tr><td>' + get_localize_name(PID_STRING) + '</td><td>' + pi['pid'] + '</td><td>' + get_localize_name(PPID_STRING) + '</td><td>' + pi['ppid'] + '</td></tr>';
    result += '<tr><td>' + get_localize_name(CMD_LINE_STRING) + '</td><td>' + pi['cmd_line'] + '</td><td>' + get_localize_name(NAME_STRING) + '</td><td>' + pi['name'] + '</td></tr>';
    result += '<tr><td>' + get_localize_name(EXE_STRING) + '</td><td>' + pi['exe'] + '</td><td>' + get_localize_name(CWD_STRING) + '</td><td>' + pi['cwd'] + '</td></tr>';
    result += '<tr><td>' + get_localize_name(STATUS_STRING) + '</td><td>' + pi['status'] + '</td><td>' + get_localize_name(CREATE_TIME_STRING) + '</td><td>' + pi['create_time'] + '</td></tr>';
    result += '<tr><td>' + get_localize_name(USERNAME_STRING) + '</td><td>' + pi['username'] + '</td><td>' + get_localize_name(TERMINAL_STRING) + '</td><td>' + pi['terminal'] + '</td></tr>';
    result += '<tr><td>' + get_localize_name(UIDS_STRING) + '</td><td>' + uids + '</td><td>' + get_localize_name(GIDS_STRING) + '</td><td>' + gids + '</td></tr>';

    result += '<tbody></table>';
    return result;
}

function make_processes_blocks() {
    var result = {};

    for (var group in processes) {
        var group_block = {};

        for (var pid in processes[group]) {
            var pid_block = {};

            pid_block[get_localize_name(STRING_PROCESS_INFO)] = format_process_info(processes[group][pid][0]);

            telemetry_block = {};
            for (var t in processes[group][pid][1]) {
                telemetry_raw = processes[group][pid][1][t];

                var parent_block = telemetry_block;
                var parent_block_id = 'processes_' + group.replace(/[\s:]/g, '_') + pid + '__';

                if (typeof(telemetry2block[t]) != 'undefined') {
                    if (typeof(pid_block[telemetry2block[t]]) == 'undefined')
                        telemetry_block[telemetry2block[t]] = {};
                    parent_block = telemetry_block[telemetry2block[t]];
                    parent_block_id += telemetry2block[t] + '_';
                }

                parent_block[t] = draw_graph(t, parent_block_id + t, telemetry_raw);
            }

            pid_block[get_localize_name(STRING_TELEMETRY_STRING)] = telemetry_block;
            group_block[pid] = pid_block;
        }

        result[group] = group_block;
    }

    return result;
}

function get_code_for_block(block_name, block_id, block) {
    block_id = block_id.replace(/[\s:]/g, '_');
    var block_name_id = block_id + '_name';
    var block_body_id = block_id + '_body';
    var block_panel_id = block_id + '_panel';

    if (typeof(block) != 'string') {
        var block_string = '';

        for (var child in block) {
            block_string += get_code_for_block(child, block_id + '_' + child, block[child]);
        }

        block = block_string;
    }

    var result =
        '<div class="panel panel-default">' +
            '<div class="panel-heading" role="tab" id="' + block_name_id + '">' +
                '<h4 class="panel-title">' +
                    '<a data-toggle="collapse" href="#' + block_body_id + '" aria-expanded="true" aria-controls="' + block_body_id + '">' +
                        get_localize_name(block_name) +
                    '</a>' +
                '</h4>' +
            '</div>' +
            '<div id="' + block_body_id + '" class="panel-collapse collapse in" role="tabpanel" aria-labelledby="' + block_name_id + '">' +
                '<div class="panel-body">' + block + '</div>' +
            '</div>' +
        '</div>';

    return result;
}

$(function(){
    for (var marker in markers) {
        markers[marker][0] = new Date(markers[marker][0]);
    }
    for (var frame in frames_ids) {
        frames_ids[frame] = new Date(frames_ids[frame]);
    }

    var blocks = make_system_telemetry_blocks();
    var global_code = get_code_for_block('system_telemetry', 'system_telemetry', blocks);

    blocks = make_processes_blocks();
    global_code += get_code_for_block('processes', 'processes', blocks);

    $('#content').html(global_code);
    draw_cached_graphs();
    $('.collapse .in').removeClass('in');
});
