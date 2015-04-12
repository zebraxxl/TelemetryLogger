function draw_cpu_load_avg_graph(graph_type, dest_id, raw_data) {
    return draw_c3_line_chart(dest_id, generate_c3_data_columns(raw_data, 3, [
        get_localize_name(LOAD_AVG_1_MIN),
        get_localize_name(LOAD_AVG_5_MIN),
        get_localize_name(LOAD_AVG_15_MIN),
    ]));
}

function draw_cpu_times_graph(graph_type, dest_id, raw_data) {
    return draw_c3_line_chart(dest_id, generate_c3_data_columns(raw_data, 10, [
        'user',
        'nice',
        'system',
        'idle',
        'iowait',
        'irq',
        'softirq',
        'steal',
        'guest',
        'nice',
    ]));
}

function draw_cpu_times_per_cpu(graph_type, dest_id, raw_data) {
    var cpus_names = []

    var cpus_raw = raw_data[0][1];
    for (var j = 0; j < cpus_raw.length; j++) {
        cpus_names.push(get_localize_name(STRING_CPU) + j);
    }

    return draw_multiple_line_chart(raw_data, dest_id, [
            'user',
            'nice',
            'system',
            'idle',
            'iowait',
            'irq',
            'softirq',
            'steal',
            'guest',
            'nice',
        ], cpus_names);
}

function draw_cpu_percent(graph_type, dest_id, raw_data) {
    return draw_c3_line_chart(dest_id, generate_c3_data_columns(raw_data, 1, [
        get_localize_name(STRING_PERCENT),
    ]));
}

function draw_cpu_percent_per_cpu(graph_type, dest_id, raw_data) {
    var cpus_names = []

    var cpus_raw = raw_data[0][1];
    for (var j = 0; j < cpus_raw.length; j++) {
        cpus_names.push(get_localize_name(STRING_CPU) + j);
    }

    return draw_multiple_line_chart(raw_data, dest_id, [get_localize_name(STRING_PERCENT)], cpus_names);
}

function draw_cpu_times_percent(graph_type, dest_id, raw_data) {
    return draw_c3_line_chart(dest_id, generate_c3_data_columns(raw_data, 10, [
        'user',
        'nice',
        'system',
        'idle',
        'iowait',
        'irq',
        'softirq',
        'steal',
        'guest',
        'nice',
    ]));
}

function draw_cpu_times_percent_per_cpu(graph_type, dest_id, raw_data) {
    var cpus_names = []

    var cpus_raw = raw_data[0][1];
    for (var j = 0; j < cpus_raw.length; j++) {
        cpus_names.push(get_localize_name(STRING_CPU) + j);
    }

    return draw_multiple_line_chart(raw_data, dest_id, [
        'user',
        'nice',
        'system',
        'idle',
        'iowait',
        'irq',
        'softirq',
        'steal',
        'guest',
        'nice',
    ], cpus_names);
}
