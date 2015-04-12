import os
import psutil

__author__ = 'zebraxxl'


def get_load_avg():
    return os.getloadavg()


def get_cpu_times(process=None):
    if process:
        return process.cpu_times()
    return psutil.cpu_times(percpu=False)


def get_cpu_times_per_cpu():
    return psutil.cpu_times(percpu=True)


def get_cpu_percent(process=None):
    if process:
        return process.cpu_percent()
    return psutil.cpu_percent(percpu=False)  # TODO: Test for interval


def get_cpu_percent_per_cpu():
    return psutil.cpu_percent(percpu=True)  # TODO: Test for interval


def get_cpu_times_percent():
    return psutil.cpu_times_percent(percpu=False)   # TODO: Test for interval


def get_cpu_times_percent_per_cpu():
    return psutil.cpu_times_percent(percpu=True)    # TODO: Test for interval


def get_proc_cpu_affinity(process):
    return process.cpu_affinity()
