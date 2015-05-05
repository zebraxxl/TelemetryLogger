from datetime import datetime
import logging
import re
from threading import Timer
import psutil
from telemetry_logger.consts import TELEMETRY_CPU_LOAD_AVG, TELEMETRY_CPU_TIMES_PERCENT_PER_CPU, TELEMETRY_DISK_IO_COUNTERS_PER_DISK, \
    TELEMETRY_NET_IO_COUNTERS_PER_NIC, TELEMETRY_PROCESS_MEM_PERCENT, TELEMETRY_PROCESS_MEM_INFO, TELEMETRY_CPU_PERCENT, \
    TELEMETRY_CPU_TIMES, TELEMETRY_NET_IO_COUNTERS, TELEMETRY_DISK_IO_COUNTERS, TELEMETRY_DISK_USAGE, TELEMETRY_MEM_SWAP, \
    TELEMETRY_MEM_SYSTEM, TELEMETRY_CPU_TIMES_PERCENT, TELEMETRY_CPU_PERCENT_PER_CPU, TELEMETRY_CPU_TIMES_PER_CPU, \
    ARGUMENT_TELEMETRY_TYPES, ARGUMENT_PROCESSES, ARGUMENT_PROCESS_PID, ARGUMENT_PROCESS_PATH, ARGUMENT_PROCESS_REGEX, \
    PROCESS_INFO_PID, PROCESS_INFO_PPID, PROCESS_INFO_NAME, PROCESS_INFO_EXE, PROCESS_INFO_CMDLINE, \
    PROCESS_INFO_CREATE_TIME, PROCESS_INFO_STATUS, PROCESS_INFO_CWD, PROCESS_INFO_USERNAME, PROCESS_INFO_UIDS, \
    PROCESS_INFO_GIDS, PROCESS_INFO_TERMINAL, TELEMETRY_PROCESSES, FRAME_TYPE_TELEMETRY, ARGUMENT_INTERVAL, \
    ARGUMENT_PROCESS_PID_FILE
from telemetry_logger.telemetry.cpu import get_load_avg, get_cpu_times, get_cpu_times_per_cpu, get_cpu_percent, get_cpu_percent_per_cpu, \
    get_cpu_times_percent, get_cpu_times_percent_per_cpu
from telemetry_logger.telemetry.disk import get_disk_usage, get_disk_io_counters_per_disk
from telemetry_logger.telemetry.disk import get_disk_io_counters
from telemetry_logger.telemetry.memory import get_mem_system, get_mem_swap, get_proc_mem_info, get_proc_mem_percent
from telemetry_logger.telemetry.net import get_net_io_counters, get_net_io_counters_per_nic
from telemetry_logger.input import InputModule

__author__ = 'zebraxxl'


class SystemInputModule(InputModule):
    logger = logging.getLogger('input:sys')

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

    def __get_process_argument(self, process, pids):
        if process.pid in pids:
            return pids[process.pid]

        for arg in self.settings[ARGUMENT_PROCESSES]:
            if arg[0] == ARGUMENT_PROCESS_PATH:
                if process.exe() == arg[1]:
                    return arg
            elif arg[0] == ARGUMENT_PROCESS_REGEX:
                if not (re.search(arg[1], ' '.join(process.cmdline())) is None):
                    return arg
        return None

    @staticmethod
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

    def __start_timer(self):
        timer = Timer(self.settings[ARGUMENT_INTERVAL], self.__get_frame)
        timer.setDaemon(True)
        timer.start()

    def __get_frame(self):
        telemetry_data = list()

        for t in self.settings[ARGUMENT_TELEMETRY_TYPES]:
            if t in self.__telemetry_getters:
                v = self.__telemetry_getters[t]()
                telemetry_data.append((t, v))

        pids = dict()
        for arg in self.settings[ARGUMENT_PROCESSES]:
            if arg[0] == ARGUMENT_PROCESS_PID:
                pids[arg[1]] = arg
            elif arg[0] == ARGUMENT_PROCESS_PID_FILE:
                try:
                    with open(arg[1], 'r') as f:
                        pid = int(f.read().strip(' \t\r\n\0'))
                    pids[pid] = arg
                except IOError:
                    pass

        processes = list()
        for p in psutil.process_iter():
            arg = self.__get_process_argument(p, pids)
            if arg is None:
                continue

            process_telemetry_data = list()
            for t in self.settings[ARGUMENT_TELEMETRY_TYPES]:
                if t in self.__process_telemetry_getters:
                    v = self.__process_telemetry_getters[t](p)
                    process_telemetry_data.append((t, v))

            process_value = (arg, SystemInputModule.__get_process_info(p), process_telemetry_data)
            processes.append(process_value)

        if len(processes) > 0:
            telemetry_data.append((TELEMETRY_PROCESSES, processes))

        result = (datetime.now(), FRAME_TYPE_TELEMETRY, telemetry_data)
        self.logger.trace('New frame generated')
        self.__start_timer()
        self._invoke_on_frame(result)

    def __init__(self, settings):
        InputModule.__init__(self, settings)
        self.settings = settings

    def start(self):
        self.__get_frame()
