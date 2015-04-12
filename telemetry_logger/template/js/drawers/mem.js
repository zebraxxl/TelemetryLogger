function draw_mem_system(graph_type, dest_id, raw_data){
    var total_mem = raw_data[0][1][1];

    var mem_abs = [];
    var mem_percent = [];

    for (var i = 0; i < raw_data.length; i++) {
        var frame_id = raw_data[i][0];

        mem_abs.push([frame_id, [
            raw_data[i][1][1],
            raw_data[i][1][3],
            raw_data[i][1][4],
            raw_data[i][1][5],
            raw_data[i][1][6],
            raw_data[i][1][7],
            raw_data[i][1][8],
        ]]);
        mem_percent.push([frame_id, raw_data[i][1][2]]);
    }

    return '<h3>' + get_localize_name(STRING_TOTAL_MEMORY) + total_mem + get_localize_name(STRING_BYTES) + '<h3>' +
        draw_c3_line_chart(dest_id + '_percent', generate_c3_data_columns(mem_percent, 1, [get_localize_name(STRING_PERCENT)])) +
        draw_c3_line_chart(dest_id + '_absolute', generate_c3_data_columns(mem_abs, 7, [
            'available',
            'used',
            'free',
            'active',
            'inactive',
            'buffers',
            'cached',
        ]));
}

function draw_mem_swap(graph_type, dest_id, raw_data){
    var total_mem = raw_data[0][1][1];

    var mem_abs = [];
    var mem_percent = [];

    for (var i = 0; i < raw_data.length; i++) {
        var frame_id = raw_data[i][0];

        mem_abs.push([frame_id, [
            raw_data[i][1][1],
            raw_data[i][1][2],
            raw_data[i][1][4],
            raw_data[i][1][5],
        ]]);
        mem_percent.push([frame_id, raw_data[i][1][3]]);
    }

    return '<h3>' + get_localize_name(STRING_TOTAL_MEMORY) + total_mem + get_localize_name(STRING_BYTES) + '<h3>' +
        draw_c3_line_chart(dest_id + '_percent', generate_c3_data_columns(mem_percent, 1, [get_localize_name(STRING_PERCENT)])) +
        draw_c3_line_chart(dest_id + '_absolute', generate_c3_data_columns(mem_abs, 4, [
            'used',
            'free',
            'sin',
            'sout',
        ]));
}
