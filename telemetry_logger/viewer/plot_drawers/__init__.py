from matplotlib.dates import DateFormatter
from telemetry_logger.consts import TELEMETRY_CPU_PERCENT, TELEMETRY_PROCESS_MEM_PERCENT, TELEMETRY_CPU_TIMES, \
    TELEMETRY_CPU_LOAD_AVG, TELEMETRY_CPU_TIMES_PER_CPU, TELEMETRY_CPU_PERCENT_PER_CPU, TELEMETRY_CPU_TIMES_PERCENT, \
    TELEMETRY_CPU_TIMES_PERCENT_PER_CPU, TELEMETRY_MEM_SYSTEM, TELEMETRY_MEM_SWAP
from telemetry_logger.localization import get_string

__author__ = 'zebraxxl'

TIME_FORMATTER = DateFormatter('%H:%M:%S.%f')


def __get_drawer_result(axes, lines, labels=None):
    return (axes, lines, labels)


def __get_name(i, value, override_names):
    if override_names and isinstance(override_names, list) and len(override_names) > i:
        return get_string(override_names[i])
    elif override_names and isinstance(override_names, basestring):
        return get_string(override_names)
    elif hasattr(value, '_fields') and len(value._fields) > i:
        return get_string(value._fields[i])
    else:
        return 'Data ' + str(i)


def draw_single_plot(data, figure, subplots_settings=[1, 1, 1]):
    axes = figure.add_subplot(*subplots_settings)
    times = [x[0] for x in data]
    values = [x[1] for x in data]

    line = axes.plot_date(times, values, '-')
    axes.xaxis.set_major_formatter(TIME_FORMATTER)
    return __get_drawer_result([axes], [line])


def draw_multiple_plot(data, figure, override_names=None, ignore_subgraphs=None, subplots_settings=[1, 1, 1]):
    times = list()
    columns = list()
    names = dict()
    oindex2rindex = dict()

    for i in xrange(len(data[0][1])):
        oindex2rindex[i] = None
        if ignore_subgraphs is not None and hasattr(data[0][1], '_fields') and data[0][1]._fields[i] in ignore_subgraphs:
                continue
        columns.append(list())
        oindex2rindex[i] = len(columns) - 1
        names[oindex2rindex[i]] = __get_name(i, data[0][1], override_names).decode('utf-8')

    for value in data:
        times.append(value[0])
        for i in xrange(len(value[1])):
            if oindex2rindex[i] is not None:
                index = oindex2rindex[i]
                columns[index].append(value[1][i])

    axes = figure.add_subplot(*subplots_settings)

    lines = list()
    labels = list()

    for i in xrange(len(columns)):
        line = axes.plot_date(times, columns[i], '-', label=names[i])
        axes.xaxis.set_major_formatter(TIME_FORMATTER)

        lines.extend(line)
        labels.append(names[i])

    return __get_drawer_result([axes], lines, labels=labels)


def __merge_draw_results(result, single_result):
    if result is None:
        return single_result

    _1 = list(result)
    _2 = list(single_result)

    result = list()
    for i in xrange(len(_1)):
        v1 = _1[i]
        v2 = _2[i]

        if v1 is None and v2 is None:
            result.append(None)
        elif v1 is None:
            result.append(v2)
        elif v2 is None:
            result.append(v1)
        else:
            if isinstance(v1, list) and isinstance(v2, list):
                v1.extend(v2)
                result.append(v1)
            elif isinstance(v1, list):
                v1.append(v2)
                result.append(v1)
            elif isinstance(v2, list):
                v2.append(v1)
                result.append(v2)
            else:
                result.append([v1, v2])
    return result


def draw_plots(plot_draw, data, figure, **kwargs):
    if plot_draw is None:
        plot_draw = draw_single_plot

    graphs = dict()
    names = dict()

    for i in xrange(len(data)):
        time = data[i][0]
        v = data[i][1]

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

    result = None
    i = 0
    for i in graphs:
        single_result = plot_draw(graphs[i], figure, subplots_settings=[len(graphs), 1, i], **kwargs)
        i += 1
        result = __merge_draw_results(result, single_result)

    return tuple(result)


PLOT_DRAWERS = {
    TELEMETRY_CPU_LOAD_AVG: lambda d, f: draw_multiple_plot(d, f, override_names=['1 min', '5 min', '15 min']),
    TELEMETRY_CPU_TIMES: draw_multiple_plot,
    TELEMETRY_CPU_PERCENT: draw_single_plot,
    TELEMETRY_CPU_TIMES_PER_CPU: lambda d, f: draw_plots(draw_multiple_plot, d, f),
    TELEMETRY_CPU_PERCENT_PER_CPU: lambda d, f: draw_plots(None, d, f),
    TELEMETRY_CPU_TIMES_PERCENT: draw_multiple_plot,
    TELEMETRY_CPU_TIMES_PERCENT_PER_CPU: lambda d, f: draw_plots(None, d, f),

    TELEMETRY_MEM_SYSTEM: lambda d, f: draw_multiple_plot(d, f, ignore_subgraphs=['total', 'percent']),
    TELEMETRY_MEM_SWAP: lambda d, f: draw_multiple_plot(d, f, ignore_subgraphs=['total', 'percent']),

    TELEMETRY_PROCESS_MEM_PERCENT: draw_single_plot,
}
