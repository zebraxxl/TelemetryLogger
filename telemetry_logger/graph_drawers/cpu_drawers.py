from telemetry_logger.graph_drawers import draw_line_graph, TIME_UNITS

__author__ = 'zebraxxl'


def draw_cpu_loadavg(values, settings, graph_id_counter):
    return draw_line_graph(values, settings, graph_id_counter, ['1 min', '5 min', '15 min'])


def draw_cpu_times(values, settings, graph_id_counter):
    return draw_line_graph(values, settings, graph_id_counter, units=TIME_UNITS)
