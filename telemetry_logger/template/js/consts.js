CPU_BLOCK = 'cpu_block';
MEM_BLOCK = 'mem_block';
DISK_BLOCK = 'disk_block';
NET_BLOCK = 'net_block';

telemetry2block = {};
telemetry2block[TELEMETRY_CPU_LOAD_AVG] = CPU_BLOCK;
telemetry2block[TELEMETRY_CPU_TIMES] = CPU_BLOCK;
telemetry2block[TELEMETRY_CPU_TIMES_PER_CPU] = CPU_BLOCK;
telemetry2block[TELEMETRY_CPU_PERCENT] = CPU_BLOCK;
telemetry2block[TELEMETRY_CPU_PERCENT_PER_CPU] = CPU_BLOCK;
telemetry2block[TELEMETRY_CPU_TIMES_PERCENT] = CPU_BLOCK;
telemetry2block[TELEMETRY_CPU_TIMES_PERCENT_PER_CPU] = CPU_BLOCK;
telemetry2block[TELEMETRY_MEM_SYSTEM] = MEM_BLOCK;
telemetry2block[TELEMETRY_MEM_SWAP] = MEM_BLOCK;
telemetry2block[TELEMETRY_DISK_USAGE] = DISK_BLOCK;
telemetry2block[TELEMETRY_DISK_IO_COUNTERS] = DISK_BLOCK;
telemetry2block[TELEMETRY_DISK_IO_COUNTERS_PER_DISK] = DISK_BLOCK;
telemetry2block[TELEMETRY_NET_IO_COUNTERS] = NET_BLOCK;
telemetry2block[TELEMETRY_NET_IO_COUNTERS_PER_NIC] = NET_BLOCK;
telemetry2block[TELEMETRY_NET_CONNECTIONS] = NET_BLOCK;
telemetry2block[TELEMETRY_PROCESS_CPU_AFFINITY] = CPU_BLOCK;
telemetry2block[TELEMETRY_PROCESS_MEM_INFO] = MEM_BLOCK;
telemetry2block[TELEMETRY_PROCESS_MEM_PERCENT] = MEM_BLOCK;
telemetry2block[TELEMETRY_PROCESS_MEM_MAP] = MEM_BLOCK;
telemetry2block[TELEMETRY_PROCESS_DISK_OPEN_FILES] = DISK_BLOCK;
telemetry2block[TELEMETRY_PROCESS_NET_CONNECTIONS] = NET_BLOCK;

STRING_TIME = 'time';
STRING_VALUE = 'value';
STRING_PERCENT = '%'
STRING_CPU = 'CPU';
STRING_TOTAL_MEMORY = 'Total memory: ';
STRING_BYTES = ' bytes';
STRING_PROCESS_INFO = 'process_info';
STRING_TELEMETRY_STRING = 'telemetry';

PID_STRING = 'pid';
CMD_LINE_STRING = 'cmd_line';
EXE_STRING = 'exe';
STATUS_STRING = 'status';
USERNAME_STRING = 'username';
UIDS_STRING = 'uids';
PPID_STRING = 'ppid';
NAME_STRING = 'name';
CWD_STRING = 'cwd';
CREATE_TIME_STRING = 'create_time';
TERMINAL_STRING = 'terminal';
GIDS_STRING = 'gids';

LOAD_AVG_1_MIN = '1 min';
LOAD_AVG_5_MIN = '5 min';
LOAD_AVG_15_MIN = '15 min';


COLORS = [
    '#CC3300',
    '#8B668B',
    '#FFDAB9',
    '#00EE00',
    '#0000CD',
    '#00F5FF',
    '#006400',
    '#DAA520',
    '#008B8B',
    '#FFC0CB',
];
