from telemetry_logger.localization import CPU_INDEX_STRING, PERCENTS_STRING
from telemetry_logger.graph_drawers import draw_line_graph, TIME_UNITS, draw_per_smth_line_graphs

__author__ = 'zebraxxl'


def draw_cpu_loadavg(values, settings, graph_id_counter):
    return draw_line_graph(values, settings, graph_id_counter, ['1 min', '5 min', '15 min'])


def draw_cpu_times(values, settings, graph_id_counter):
    return draw_line_graph(values, settings, graph_id_counter, units=TIME_UNITS)


def draw_cpu_times_per_cpu(values, settings, graph_id_counter):
    return draw_per_smth_line_graphs(values, settings, graph_id_counter, CPU_INDEX_STRING,
                                     lambda v, s, g: draw_line_graph(v, s, g, units=TIME_UNITS))


def draw_cpu_percent(values, settings, graph_id_counter):
    return draw_line_graph(values, settings, graph_id_counter, override_names=[PERCENTS_STRING])


def draw_cpu_percent_per_cpu(values, settings, graph_id_counter):
    return draw_per_smth_line_graphs(values, settings, graph_id_counter, CPU_INDEX_STRING)


def draw_cpu_times_percent(values, settings, graph_id_counter):
    return draw_line_graph(values, settings, graph_id_counter)


def draw_cpu_times_percent_per_cpu(values, settings, graph_id_counter):
    return draw_per_smth_line_graphs(values, settings, graph_id_counter, CPU_INDEX_STRING)

def draw_proc_threads_count(values, settings, graph_id_counter):
    return draw_line_graph(values, settings, graph_id_counter)
