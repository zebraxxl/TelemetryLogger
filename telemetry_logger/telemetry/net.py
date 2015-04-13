import psutil

__author__ = 'zebraxxl'


def get_net_io_counters():
    return psutil.net_io_counters(pernic=False)


def get_net_io_counters_per_nic():
    return psutil.net_io_counters(pernic=True)
