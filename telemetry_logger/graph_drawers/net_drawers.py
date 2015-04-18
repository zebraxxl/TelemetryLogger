from telemetry_logger.localization import NIC_STRING
from telemetry_logger.graph_drawers import draw_line_graph, SIZE_UNITS, draw_per_smth_line_graphs

__author__ = 'zebraxxl'


def draw_net_io_counters(values, settings, graph_id_counter):
    result = draw_line_graph(values, settings, graph_id_counter, units=SIZE_UNITS,
                             ignore_sub_graphs=['packets_sent', 'packets_recv', 'errin', 'errout', 'dropin', 'dropout'])
    return result + draw_line_graph(values, settings, graph_id_counter, ignore_sub_graphs=['bytes_sent', 'bytes_recv'])


def draw_net_io_counters_per_nic(values, settings, graph_id_counter):
    return draw_per_smth_line_graphs(values, settings, graph_id_counter, NIC_STRING, draw_net_io_counters)
