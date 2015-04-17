from localization import CPU_INDEX_STRING, PERCENTS_STRING
from telemetry_logger.graph_drawers import draw_line_graph, TIME_UNITS, draw_per_smth_line_graphs

__author__ = 'zebraxxl'


def draw_cpu_loadavg(values, settings, graph_id_counter):
    return draw_line_graph(values, settings, graph_id_counter, ['1 min', '5 min', '15 min'])


def draw_cpu_times(values, settings, graph_id_counter):
    return draw_line_graph(values, settings, graph_id_counter, units=TIME_UNITS)


def draw_cpu_times_per_cpu(values, settings, graph_id_counter):
    return draw_per_smth_line_graphs(values, settings, graph_id_counter, CPU_INDEX_STRING, units=TIME_UNITS)


def draw_cpu_percent(values, settings, graph_id_counter):
    return draw_line_graph(values, settings, graph_id_counter, override_names=[PERCENTS_STRING])
