from telemetry_logger.localization import DISK_NAME_STRING
from telemetry_logger.graph_drawers import SIZE_UNITS, draw_per_smth_line_graphs

__author__ = 'zebraxxl'


def draw_disk_usage(values, settings, graph_id_counter):
    # TODO: Percent graph
    return draw_per_smth_line_graphs(values, settings, graph_id_counter, DISK_NAME_STRING, units=SIZE_UNITS,
                                     ignore_sub_graphs=['total', 'percent'])
