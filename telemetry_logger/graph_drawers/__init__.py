from copy import deepcopy
from telemetry_logger.localization import get_string
from telemetry_logger.consts import ARGUMENT_SPLIT_GRAPHS, JS_VAR_MARKERS_LINES, ARGUMENT_SUB_CHART
from telemetry_logger.utils import JavaScriptInJsonExpression, dump_javascript

__author__ = 'zebraxxl'

GRAPH_STANDARD_SETTINGS = {
    'size': {
        'height': 250,
        'width': JavaScriptInJsonExpression('parent_width'),
    },
    'data': {
        'x': 'x',
        'xFormat': '%H:%M:%S.%L',
        'columns': None,
    },
    'axis': {
        'x': {
            'type': 'timeseries',
            'tick': {'format': '%H:%M:%S.%L'},
        },
    },
    'grid': {
        'x': {
            'lines': JavaScriptInJsonExpression(JS_VAR_MARKERS_LINES),
        }
    },
    'zoom': {'enabled': True}
}


def __get_name(i, value, override_names):
    if override_names and len(override_names) > i:
        return get_string(override_names[i])
    elif hasattr(value, '_fields') and len(value._fields) > i:
        return get_string(value._fields[i])
    else:
        return 'Data ' + str(i)


def get_new_standard_graph_settings(settings):
    result = deepcopy(GRAPH_STANDARD_SETTINGS)

    if settings[ARGUMENT_SUB_CHART]:
        result['size']['height'] = 300
        result['subchart'] = {'show': True}

    return result


def __draw_graph(columns, names, graph_id_counter, settings):
    graph_id = graph_id_counter.get_next_value()

    params = get_new_standard_graph_settings(settings)
    params['bindto'] = '#' + graph_id
    params['data']['columns'] = columns
    params['data']['names'] = names

    result = 'var parent_width = $("#{0}").parent().width();\n'.format(graph_id)
    result += 'var chart = c3.generate({0});'.format(dump_javascript(params))
    return result


def draw_line_graph(values, settings, graph_id_counter, override_names=None):
    result = ''

    columns = list()
    columns.append(['x'])
    names = dict()

    for i in xrange(len(values[0][1])):
        data_name = 'data{0}'.format(i)
        columns.append([data_name])
        names[data_name] = __get_name(i, values[0][1], override_names)

    for value in values:
        columns[0].append(value[0].strftime('%H:%M:%S.%f')[:-3])
        for i in xrange(len(value[1])):
            columns[i + 1].append(value[1][i])

    if settings[ARGUMENT_SPLIT_GRAPHS]:
        for i in xrange(len(names)):
            result += __draw_graph([columns[0], columns[i + 1]], {columns[i + 1][0]: names[columns[i + 1][0]]},
                                   graph_id_counter, settings)
    else:
        result += __draw_graph(columns, names, graph_id_counter, settings)

    return result