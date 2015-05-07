from matplotlib.dates import DateFormatter
from telemetry_logger.consts import TELEMETRY_CPU_PERCENT, TELEMETRY_PROCESS_MEM_PERCENT, TELEMETRY_CPU_TIMES
from telemetry_logger.localization import get_string

__author__ = 'zebraxxl'

TIME_FORMATTER = DateFormatter('%H:%M:%S.%f')


def __get_name(i, value, override_names):
    if override_names and isinstance(override_names, list) and len(override_names) > i:
        return get_string(override_names[i])
    elif override_names and isinstance(override_names, basestring):
        return get_string(override_names)
    elif hasattr(value, '_fields') and len(value._fields) > i:
        return get_string(value._fields[i])
    else:
        return 'Data ' + str(i)


def draw_single_plot(data, figure):
    axes = figure.add_subplot(1, 1, 1)
    times = [x[0] for x in data]
    values = [x[1] for x in data]

    axes.plot_date(times, values, '-')
    axes.xaxis.set_major_formatter(TIME_FORMATTER)
    return [axes]


def draw_multiple_plot(data, figure, override_names=None, ignore_subgraphs=None):
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
        names[oindex2rindex[i]] = __get_name(i, data[0][1], override_names)

    for value in data:
        times.append(value[0])
        for i in xrange(len(value[1])):
            if oindex2rindex[i] is not None:
                index = oindex2rindex[i]
                columns[index].append(value[1][i])

    axes = figure.add_subplot(1, 1, 1)
    for i in xrange(len(columns)):
        axes.plot_date(times, columns[i], '-', label=names[i])
        axes.xaxis.set_major_formatter(TIME_FORMATTER)
    return [axes]



PLOT_DRAWERS = {
    TELEMETRY_CPU_TIMES: draw_multiple_plot,
    TELEMETRY_CPU_PERCENT: draw_single_plot,

    TELEMETRY_PROCESS_MEM_PERCENT: draw_single_plot,
}
