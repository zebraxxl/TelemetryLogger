import psutil

__author__ = 'zebraxxl'


def get_net_io_counters():
    return psutil.net_io_counters(pernic=False)


def get_net_io_counters_per_nic():
    return psutil.net_io_counters(pernic=True)


def get_net_connections():
    return psutil.net_connections()


def get_proc_net_connections(process):
    return process.connections()
