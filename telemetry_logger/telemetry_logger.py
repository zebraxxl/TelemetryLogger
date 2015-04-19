import re
import time
from datetime import datetime
import psutil
from consts import ARGUMENT_OUTPUT, TELEMETRY_CPU_LOAD_AVG, ARGUMENT_TELEMETRY_TYPES, FRAME_TYPE_TELEMETRY, \
    ARGUMENT_INTERVAL, TELEMETRY_CPU_TIMES, TELEMETRY_CPU_TIMES_PER_CPU, TELEMETRY_CPU_PERCENT, \
    TELEMETRY_CPU_PERCENT_PER_CPU, TELEMETRY_CPU_TIMES_PERCENT, TELEMETRY_CPU_TIMES_PERCENT_PER_CPU, \
    TELEMETRY_MEM_SYSTEM, TELEMETRY_MEM_SWAP, TELEMETRY_DISK_USAGE, TELEMETRY_DISK_IO_COUNTERS, \
    TELEMETRY_DISK_IO_COUNTERS_PER_DISK, TELEMETRY_NET_IO_COUNTERS, TELEMETRY_NET_IO_COUNTERS_PER_NIC, \
    ARGUMENT_PROCESSES, ARGUMENT_PROCESS_PID, ARGUMENT_PROCESS_PATH, ARGUMENT_PROCESS_REGEX, \
    TELEMETRY_PROCESSES, PROCESS_INFO_PID, PROCESS_INFO_PPID, PROCESS_INFO_NAME, PROCESS_INFO_EXE, PROCESS_INFO_CMDLINE, \
    PROCESS_INFO_CREATE_TIME, PROCESS_INFO_STATUS, PROCESS_INFO_CWD, PROCESS_INFO_USERNAME, PROCESS_INFO_GIDS, \
    PROCESS_INFO_UIDS, PROCESS_INFO_TERMINAL, TELEMETRY_PROCESS_MEM_INFO, \
    TELEMETRY_PROCESS_MEM_PERCENT, REMOTE_COMMAND_MARKER, REMOTE_COMMAND_MARKER_NAME, FRAME_TYPE_MARKER
from control import subscribe_to_command
from logger import error
from output import init_output_file, write_frame
from telemetry.cpu import get_load_avg, get_cpu_times, get_cpu_times_per_cpu, get_cpu_percent, get_cpu_percent_per_cpu, \
    get_cpu_times_percent, get_cpu_times_percent_per_cpu
from telemetry.disk import get_disk_usage, get_disk_io_counters, get_disk_io_counters_per_disk
from telemetry.memory import get_mem_system, get_mem_swap, get_proc_mem_info, get_proc_mem_percent
from telemetry.net import get_net_io_counters, get_net_io_counters_per_nic

__author__ = 'zebraxxl'

__telemetry_getters = {
    TELEMETRY_CPU_LOAD_AVG: get_load_avg,
    TELEMETRY_CPU_TIMES: get_cpu_times,
    TELEMETRY_CPU_TIMES_PER_CPU: get_cpu_times_per_cpu,
    TELEMETRY_CPU_PERCENT: get_cpu_percent,
    TELEMETRY_CPU_PERCENT_PER_CPU: get_cpu_percent_per_cpu,
    TELEMETRY_CPU_TIMES_PERCENT: get_cpu_times_percent,
    TELEMETRY_CPU_TIMES_PERCENT_PER_CPU: get_cpu_times_percent_per_cpu,

    TELEMETRY_MEM_SYSTEM: get_mem_system,
    TELEMETRY_MEM_SWAP: get_mem_swap,

    TELEMETRY_DISK_USAGE: get_disk_usage,
    TELEMETRY_DISK_IO_COUNTERS: get_disk_io_counters,
    TELEMETRY_DISK_IO_COUNTERS_PER_DISK: get_disk_io_counters_per_disk,

    TELEMETRY_NET_IO_COUNTERS: get_net_io_counters,
    TELEMETRY_NET_IO_COUNTERS_PER_NIC: get_net_io_counters_per_nic,
}

__process_telemetry_getters = {
    TELEMETRY_CPU_TIMES: get_cpu_times,
    TELEMETRY_CPU_PERCENT: get_cpu_percent,

    TELEMETRY_PROCESS_MEM_INFO: get_proc_mem_info,
    TELEMETRY_PROCESS_MEM_PERCENT: get_proc_mem_percent,
}


def __get_process_argument(process, settings):
    for arg in settings[ARGUMENT_PROCESSES]:
        if arg[0] == ARGUMENT_PROCESS_PID:
            if process.pid == arg[1]:
                return arg
        elif arg[0] == ARGUMENT_PROCESS_PATH:
            if process.exe() == arg[1]:
                return arg
        elif arg[0] == ARGUMENT_PROCESS_REGEX:
            if not (re.search(arg[1], ' '.join(process.cmdline())) is None):
                return arg
    return None


def __get_process_info(process):
    return {
        PROCESS_INFO_PID: process.pid,
        PROCESS_INFO_PPID: process.ppid(),
        PROCESS_INFO_NAME: process.name(),
        PROCESS_INFO_EXE: process.exe(),
        PROCESS_INFO_CMDLINE: ' '.join(process.cmdline()),
        PROCESS_INFO_CREATE_TIME: process.create_time(),
        PROCESS_INFO_STATUS: process.status(),
        PROCESS_INFO_CWD: process.cwd(),
        PROCESS_INFO_USERNAME: process.username(),
        PROCESS_INFO_UIDS: process.uids(),
        PROCESS_INFO_GIDS: process.gids(),
        PROCESS_INFO_TERMINAL: process.terminal(),
    }


def __get_frame(settings):
    telemetry_data = list()

    for t in settings[ARGUMENT_TELEMETRY_TYPES]:
        if t in __telemetry_getters:
            v = __telemetry_getters[t]()
            telemetry_data.append((t, v))

    processes = list()
    for p in psutil.process_iter():
        arg = __get_process_argument(p, settings)
        if arg is None:
            continue

        process_telemetry_data = list()
        for t in settings[ARGUMENT_TELEMETRY_TYPES]:
            if t in __process_telemetry_getters:
                v = __process_telemetry_getters[t](p)
                process_telemetry_data.append((t, v))

        process_value = (arg, __get_process_info(p), process_telemetry_data)
        processes.append(process_value)

    if len(processes) > 0:
        telemetry_data.append((TELEMETRY_PROCESSES, processes))

    result = (datetime.now(), FRAME_TYPE_TELEMETRY, telemetry_data)

    return result


def __set_marker(data):
    name = data[REMOTE_COMMAND_MARKER_NAME]
    frame = (datetime.now(), FRAME_TYPE_MARKER, name)
    write_frame(frame)


def run_logger(settings):
    try:
        init_output_file(settings[ARGUMENT_OUTPUT])
    except Exception as e:
        error('Error while opening output file ({0})', e)

    subscribe_to_command(REMOTE_COMMAND_MARKER, __set_marker)

    while True:
        frame = __get_frame(settings)

        try:
            write_frame(frame)
        except Exception as e:
            error('Error while writing frame ({0}). File can be corrupted', e)

        time.sleep(settings[ARGUMENT_INTERVAL])
