function draw_disk_usage(graph_type, dest_id, raw_data) {
    var mount_points = [];

    for (var i in raw_data[0][1]) {
        mount_points.push(i);
    }

    return draw_multiple_line_chart(raw_data, dest_id, [
        'total',
        'used',
        'free',
        'percent'
    ], mount_points);
}
