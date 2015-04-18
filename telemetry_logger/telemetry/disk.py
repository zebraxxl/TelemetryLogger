import psutil

__author__ = 'zebraxxl'
disk_partitions = psutil.disk_partitions()


def get_disk_usage():
    result = {}

    for partition in disk_partitions:
        result[partition.mountpoint] = psutil.disk_usage(partition.mountpoint)

    return result


def get_disk_io_counters():
    return psutil.disk_io_counters(perdisk=False)


def get_disk_io_counters_per_disk():
    return psutil.disk_io_counters(perdisk=True)
