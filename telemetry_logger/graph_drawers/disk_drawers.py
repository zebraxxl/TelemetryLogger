from telemetry_logger.localization import DISK_NAME_STRING, PERCENTS_STRING
from telemetry_logger.graph_drawers import SIZE_UNITS, draw_per_smth_line_graphs, draw_line_graph

__author__ = 'zebraxxl'


def __draw_disk_usage(v, s, g):
    return draw_line_graph(v, s, g, units=SIZE_UNITS, ignore_sub_graphs=['total', 'percent']) +\
        draw_line_graph(v, s, g, override_names=PERCENTS_STRING, ignore_sub_graphs=['total', 'used', 'free'])


def draw_disk_usage(values, settings, graph_id_counter):
    return draw_per_smth_line_graphs(values, settings, graph_id_counter, DISK_NAME_STRING, __draw_disk_usage)
