from copy import deepcopy
from telemetry_logger.localization import get_string, UNITS_STRING
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

TIME_UNITS = {
    'sec': 1,
    'min': 60,
    'hour': 3600,
    'day': 86400,
}

SIZE_UNITS = {
    'bytes': 1,
    'kbytes': 1024,
    'mbytes': 1048576,
    'gbytes': 1073741824,
    'tbytes': 1099511627776,
    'pbytes': 1125899906842624,     # Seriously? =)
}


def __get_name(i, value, override_names):
    if override_names and isinstance(override_names, list) and len(override_names) > i:
        return get_string(override_names[i])
    elif override_names and isinstance(override_names, basestring):
        return get_string(override_names)
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


def __draw_graph(columns, names, graph_id, settings, units):
    chart_name = 'chart_' + graph_id
    chart_data = chart_name + '_data'

    params = get_new_standard_graph_settings(settings)
    params['bindto'] = '#' + graph_id
    params['data']['columns'] = JavaScriptInJsonExpression(chart_data)
    params['data']['names'] = names

    result = 'var parent_width = $("#{0}").parent().width();\n'.format(graph_id)
    result += '{chart_data} = {columns}\n'.format(chart_data=chart_data, columns=dump_javascript(columns))
    result += '{chart_name} = c3.generate({params});'.format(chart_name=chart_name, params=dump_javascript(params))

    if units:
        button_id = chart_name + '_units_button'
        default_units = get_string(units[units.keys()[0]])

        for unit in units:
            if units[unit] == 1:
                default_units = get_string(unit)
                break

        result += '''
        $('#{graph_id}').before('{units_string}: ').before(
            $('<div></div>', {{'class': 'dropdown', 'style': 'display: inline'}}).append(
                $('<button></button>', {{
                    'id': '{button_id}',
                    'type': 'button',
                    'data-toggle': 'dropdown',
                    'aria-haspopup': 'true',
                    'aria-expanded': 'false',
                }}).append('{default_units} <span class="caret"></span>')
            ).append(
                $('<ul></ul>', {{
                    'class': 'dropdown-menu',
                    'role': 'menu',
                    'aria-labelledby': '{button_id}',
                }})'''.format(graph_id=graph_id, button_id=button_id, default_units=default_units,
                              units_string=get_string(UNITS_STRING))

        for unit in units:
            result += '''
                .append(
                    $('<li></li>', {{
                        'role': 'presentation'
                    }}).append(
                        $('<a></a>', {{
                            'role': 'menuitem',
                            'tabindex': '-1',
                            'href': '#',
                            'text': '{unit_name}',
                            'click': function() {{
                                change_units({chart_name}, {chart_data}, {unit_value}, '{button_id}', '{unit_name}');
                            }}
                        }})
                    )
                )
            '''.format(unit_name=get_string(unit), unit_value=units[unit], chart_name=chart_name, chart_data=chart_data,
                       button_id=button_id)

        result += '''
            )
        );
        '''

    return result


def draw_line_graph(values, settings, graph_id_counter, override_names=None, units=None, ignore_sub_graphs=list()):
    result = ''

    columns = list()
    columns.append(['x'])
    names = dict()
    oindex2rindex = dict()

    if isinstance(values[0][1], float) or isinstance(values[0][1], int):
        columns.append(['data'])
        names['data'] = __get_name(0, values[0][0], override_names)
    else:
        for i in xrange(len(values[0][1])):
            oindex2rindex[i] = None
            if hasattr(values[0][1], '_fields') and values[0][1]._fields[i] in ignore_sub_graphs:
                continue

            data_name = 'data{0}'.format(i)
            columns.append([data_name])
            names[data_name] = __get_name(i, values[0][1], override_names)
            oindex2rindex[i] = len(columns) - 1

    for value in values:
        columns[0].append(value[0].strftime('%H:%M:%S.%f')[:-3])

        if isinstance(values[0][1], float) or isinstance(values[0][1], int):
            columns[1].append(value[1])
        else:
            for i in xrange(len(value[1])):
                if not (oindex2rindex[i] is None):
                    index = oindex2rindex[i]
                    columns[index].append(value[1][i])

    if settings[ARGUMENT_SPLIT_GRAPHS]:
        for i in xrange(len(names)):
            result += __draw_graph([columns[0], columns[i + 1]], {columns[i + 1][0]: names[columns[i + 1][0]]},
                                   graph_id_counter.get_next_value(), settings, units)
    else:
        result += __draw_graph(columns, names, graph_id_counter.get_next_value(), settings, units)

    return result


def draw_per_smth_line_graphs(values, settings, graph_id_counter, title_format_string, override_names=None, units=None,
                              ignore_sub_graphs=list()):
    result = ''

    graphs = dict()
    names = dict()

    for i in xrange(len(values)):
        time = values[i][0]
        v = values[i][1]

        if isinstance(v, list):
            for j in xrange(len(v)):
                if j not in graphs:
                    graphs[j] = list()
                    names[j] = j
                graphs[j].append((time, v[j]))

        elif isinstance(v, dict):
            j = 0
            for k in v:
                if j not in graphs:
                    graphs[j] = list()
                    names[j] = k
                graphs[j].append((time, v[k]))
                j += 1

    for i in graphs:
        title_id = graph_id_counter.get_next_value()

        result += draw_line_graph(graphs[i], settings, graph_id_counter, override_names, units, ignore_sub_graphs)

        result += '$("#{title_id}").html("<center><h3>{title}</h3></center>");\n'\
            .format(title_id=title_id, title=get_string(title_format_string).format(index=names[i]))

    return result
