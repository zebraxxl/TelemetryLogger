localization = {
    'system_telemetry': 'Общая системная телеметрия',
    'unknown_graph_type': 'Неизвестный тип графика',
}

function get_localize_name(id) {
    if (typeof(localization[id]) != 'undefined')
        return localization[id];
    else
        return id;
}

function format_time(d) {
    return d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds() + '.' + d.getMilliseconds();
}
