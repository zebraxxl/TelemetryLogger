from telemetry_logger.localization import PERCENTS_STRING
from telemetry_logger.graph_drawers import draw_line_graph, SIZE_UNITS

__author__ = 'zebraxxl'


def draw_mem_system(values, settings, graph_id_counter):
    result = draw_line_graph(values, settings, graph_id_counter, units=SIZE_UNITS,
                             ignore_sub_graphs=['total', 'percent'])
    return result + draw_line_graph(values, settings, graph_id_counter,
                                    override_names=PERCENTS_STRING,
                                    ignore_sub_graphs=['total', 'available', 'used', 'free', 'active', 'inactive',
                                                       'buffers', 'cached'])


def draw_mem_swap(values, settings, graph_id_counter):
    result = draw_line_graph(values, settings, graph_id_counter, units=SIZE_UNITS,
                             ignore_sub_graphs=['total', 'percent'])
    return result + draw_line_graph(values, settings, graph_id_counter, override_names=PERCENTS_STRING,
                                    ignore_sub_graphs=['total', 'used', 'free', 'sin', 'sout'])
