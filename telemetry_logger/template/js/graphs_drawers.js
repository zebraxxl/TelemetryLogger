function get_markers_grid_lines() {
    if (typeof(markers_grid_lines) != 'undefined') {
        return markers_grid_lines
    } else {
        markers_grid_lines = []

        for (var i = 0; i < markers.length; i++) {
            markers_grid_lines.push({
                value: markers[i][0],
                text: markers[i][1],
                position: 'start',
            })
        }

        return markers_grid_lines;
    }
}

function generate_c3_data_columns(raw_data, lines_count, names) {
    var result = [['x']];
    for (var i = 0; i < lines_count; i++) {
        result.push([names[i]]);
    }

    for (var i = 0; i < raw_data.length; i++) {
        var frame_id = raw_data[i][0];
        result[0].push(frames_ids[frame_id]);

        if (lines_count > 1) {
            for (var j = 0; j < lines_count; j++) {
                result[j + 1].push(raw_data[i][1][j]);
            }
        } else {
            result[1].push(raw_data[i][1]);
        }
    }

    return result;
}

function draw_c3_line_chart(dest_id, columns) {
    dest_id += '_chart';
    cached_graph_drawers.push(function(){
        var parent = $('#' + dest_id);

        var chart = c3.generate({
            bindto: '#' + dest_id,
            size: {
                width: parent.width(),
                height: 250,
            },
            data: {
                x: 'x',
                columns: columns
            },
            axis: {
                x: {
                    type: 'timeseries',
                    tick: {
                        format: '%H:%M:%S.%L'
                    },
                },
            },
            grid: {
                x: {
                    lines: get_markers_grid_lines(),
                },
            },
            zoom: {
                enabled: true
            }
        });
    });
    return '<div id="' + dest_id + '"></div>';
}

function draw_multiple_line_chart(raw_data, dest_id, columns_names, charts_names) {
    var per_columns = [];

    var per_raw = raw_data[0][1];
    for (var j in per_raw) {
        per_columns.push([]);
    }

    for (var i = 0; i < raw_data.length; i++) {
        var frame_id = raw_data[i][0];

        var per_raw = raw_data[i][1];

        var j = 0;
        for (var in_raw in per_raw) {
            per_columns[j].push([frame_id, per_raw[in_raw]]);
            j++;
        }
    }

    var result = '';
    for (var i = 0; i < per_columns.length; i++) {
        result += '<center><h2>' + charts_names[i] + '</h2></center>';
        result += draw_c3_line_chart(dest_id + 'per_smth' + i, generate_c3_data_columns(per_columns[i], columns_names.length, columns_names));
    }
    return result;
}

graph_drawers = {};
graph_drawers[TELEMETRY_CPU_LOAD_AVG] = draw_cpu_load_avg_graph;
graph_drawers[TELEMETRY_CPU_TIMES] = draw_cpu_times_graph;
graph_drawers[TELEMETRY_CPU_TIMES_PER_CPU] = draw_cpu_times_per_cpu;
graph_drawers[TELEMETRY_CPU_PERCENT] = draw_cpu_percent;
graph_drawers[TELEMETRY_CPU_PERCENT_PER_CPU] = draw_cpu_percent_per_cpu;
graph_drawers[TELEMETRY_CPU_TIMES_PERCENT] = draw_cpu_times_percent;
graph_drawers[TELEMETRY_CPU_TIMES_PERCENT_PER_CPU] = draw_cpu_times_percent_per_cpu;
graph_drawers[TELEMETRY_MEM_SYSTEM] = draw_mem_system;
graph_drawers[TELEMETRY_MEM_SWAP] = draw_mem_swap;
graph_drawers[TELEMETRY_DISK_USAGE] = draw_disk_usage;

cached_graph_drawers = [];

function draw_graph(graph_type, dest_id, data) {
    if (typeof(graph_drawers[graph_type]) != 'undefined') {
        return graph_drawers[graph_type](graph_type, dest_id, data);
    } else {
        return '<div class="alert alert-danger" role="alert">' + get_localize_name('unknown_graph_type') + '</div>';
    }
}

function draw_cached_graphs() {
    for (var a in cached_graph_drawers) {
        try {
            cached_graph_drawers[a]();
        } catch (err) {
        }
    }
}
