import psutil

__author__ = 'zebraxxl'


def get_mem_system():
    return psutil.virtual_memory()


def get_mem_swap():
    return psutil.swap_memory()


def get_proc_mem_info(process):
    return process.memory_info_ex()


def get_proc_mem_percent(process):
    return process.memory_percent()
