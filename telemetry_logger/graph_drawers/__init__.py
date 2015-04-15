from copy import deepcopy
from telemetry_logger.consts import ARGUMENT_SPLIT_GRAPHS
from utils import JavaScriptInJsonExpression, dump_javascript

__author__ = 'zebraxxl'

GRAPH_STANDART_SETTINGS = {
    'size': {
        'height': 250,
        'width': 500,
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
    # 'grid': {
    #     'x': {
    #         'lines': None,
    #     }
    # },
    'zoom': {'enabled': True}
}


def __get_name(i, value, override_names):
    return str(i)


def draw_line_graph(values, settings, graph_id_counter, override_names=None):
    result = ''

    columns = list()
    columns.append(['x'])
    names = list()

    for i in xrange(len(values[0][1])):
        columns.append(['data{0}'.format(i)])
        names.append(__get_name(i, values[0][1], override_names))

    for value in values:
        columns[0].append(value[0].strftime('%H:%M:%S.%f')[:-3])
        for i in xrange(len(value[1])):
            columns[i + 1].append(value[1][i])

    if settings[ARGUMENT_SPLIT_GRAPHS]:
        pass
    else:
        graph_id = graph_id_counter.get_next_value()

        params = deepcopy(GRAPH_STANDART_SETTINGS)
        params['bindto'] = '#' + graph_id
        params['size']['width'] = JavaScriptInJsonExpression('parent_width')

        result += 'var parent_width = $("#{0}").parent().width();\n'.format(graph_id)
        result += 'var chart = c3.generate({0});'.format(dump_javascript(params))

    return result