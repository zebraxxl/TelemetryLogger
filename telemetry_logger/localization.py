# -*- coding: utf-8 -*-
from consts import TELEMETRY_FAMILY_CPU, TELEMETRY_FAMILY_MEM, TELEMETRY_FAMILY_DISK, TELEMETRY_FAMILY_NET, \
    TELEMETRY_CPU_LOAD_AVG, TELEMETRY_CPU_TIMES, TELEMETRY_CPU_TIMES_PER_CPU, TELEMETRY_CPU_PERCENT, \
    TELEMETRY_CPU_PERCENT_PER_CPU, TELEMETRY_CPU_TIMES_PERCENT, TELEMETRY_CPU_TIMES_PERCENT_PER_CPU, \
    TELEMETRY_MEM_SYSTEM, TELEMETRY_MEM_SWAP, TELEMETRY_DISK_USAGE, TELEMETRY_DISK_IO_COUNTERS, \
    TELEMETRY_DISK_IO_COUNTERS_PER_DISK, TELEMETRY_NET_IO_COUNTERS, TELEMETRY_NET_IO_COUNTERS_PER_NIC, \
    TELEMETRY_PROCESS_MEM_INFO, TELEMETRY_PROCESS_MEM_PERCENT, TELEMETRY_PROCESS_THREADS_COUNT

__author__ = 'zebraxxl'

UNKNOWN_TELEMETRY_TYPE = 'UNKNOWN_TELEMETRY_TYPE'
SYSTEM_TELEMETRY_STRING = 'SYSTEM_TELEMETRY'
UNITS_STRING = 'UNITS_STRING'
CPU_INDEX_STRING = 'CPU_INDEX'
PERCENTS_STRING = 'PERCENTS'
DISK_MOUNT_POINT_STRING = 'DISK_MOUNT_POINT'
DISK_NAME_STRING = 'DISK_NAME'
NIC_STRING = 'NIC_STRING'
PROCESS_INFO_STRING = 'PROCESS_INFO'
TELEMETRY_STRING = 'TELEMETRY'
PROCESSES_STRING = 'PROCESSES'

PROCESS_FILTER_PID_STRING = 'PROCESS_FILTER_PID'
PROCESS_FILTER_PATH_STRING = 'PROCESS_FILTER_PATH'
PROCESS_FILTER_REGEX_STRING = 'PROCESS_FILTER_REGEX'
PROCESS_FILTER_PID_FILE_STRING = 'PROCESS_PID_FILE'

PID_STRING = 'PID'
PPID_STRING = 'PPID'
CMD_LINE_STRING = 'CMD_LINE'
EXE_STRING = 'EXE'
STATUS_STRING = 'STATUS'
USERNAME_STRING = 'USERNAME'
UIDS_STRING = 'UIDS'
NAME_STRING = 'NAME'
CWD_STRING = 'CWD'
CREATE_TIME_STRING = 'CREATE_TIME'
TERMINAL_STRING = 'TERMINAL'
GIDS_STRING = 'GIDS'

__LOCALIZED_STRINGS = {
    UNKNOWN_TELEMETRY_TYPE: 'Неизвестный тип телеметрии',
    SYSTEM_TELEMETRY_STRING: 'Системная телеметрия',
    UNITS_STRING: 'Единицы измерения',
    CPU_INDEX_STRING: 'ЦПУ {index}',
    PERCENTS_STRING: 'Проценты',
    DISK_MOUNT_POINT_STRING: 'Точка монтирования: {index}',
    DISK_NAME_STRING: 'Диск: {index}',
    NIC_STRING: 'Сетевое устройство: {index}',
    PROCESS_INFO_STRING: 'Информация о процессе',
    TELEMETRY_STRING: 'Телеметрия',
    PROCESSES_STRING: 'Процессы',

    PROCESS_FILTER_PID_STRING: 'ПИД: {0}',
    PROCESS_FILTER_PATH_STRING: 'Путь: {0}',
    PROCESS_FILTER_REGEX_STRING: 'Регулярное выражение: {0}',
    PROCESS_FILTER_PID_FILE_STRING: 'ПИД файл: {0}',

    PID_STRING: 'ПИД',
    PPID_STRING: 'Родитель',
    CMD_LINE_STRING: 'Коммандная строка',
    EXE_STRING: 'Исполняемый файл',
    STATUS_STRING: 'Статус',
    USERNAME_STRING: 'Имя пользователя',
    UIDS_STRING: 'UIDS',
    NAME_STRING: 'Имя процесса',
    CWD_STRING: 'Текущая папка',
    CREATE_TIME_STRING: 'Время создания',
    TERMINAL_STRING: 'Терминал',
    GIDS_STRING: 'GIDS',

    TELEMETRY_FAMILY_CPU: 'Процессор',
    TELEMETRY_FAMILY_MEM: 'Память',
    TELEMETRY_FAMILY_DISK: 'Жесткий диск',
    TELEMETRY_FAMILY_NET: 'Сеть',

    TELEMETRY_CPU_LOAD_AVG: 'Загрузка системы',
    TELEMETRY_CPU_TIMES: 'Процессорное время',
    TELEMETRY_CPU_TIMES_PER_CPU: 'Процессорное время по ядрам',
    TELEMETRY_CPU_PERCENT: 'Загрузка процессора в процентах',
    TELEMETRY_CPU_PERCENT_PER_CPU: 'Загрузка процессора в процентах по ядрам',
    TELEMETRY_CPU_TIMES_PERCENT: 'Процессорное время в процентах',
    TELEMETRY_CPU_TIMES_PERCENT_PER_CPU: 'Процессорное время в процентах по ядрам',

    TELEMETRY_MEM_SYSTEM: 'Системная память',
    TELEMETRY_MEM_SWAP: 'Раздел подкачки',

    TELEMETRY_DISK_USAGE: 'Использование диска',
    TELEMETRY_DISK_IO_COUNTERS: 'Общий ввод/вывод',
    TELEMETRY_DISK_IO_COUNTERS_PER_DISK: 'Ввод/Вывод по отдельным дискам',

    TELEMETRY_NET_IO_COUNTERS: 'Ввод/Вывод сети',
    TELEMETRY_NET_IO_COUNTERS_PER_NIC: 'Ввод/Вывод по интерфейсам',

    TELEMETRY_PROCESS_THREADS_COUNT: 'Количество потоков исполнения',
    TELEMETRY_PROCESS_MEM_INFO: 'Использование памяти',
    TELEMETRY_PROCESS_MEM_PERCENT: 'Использование памяти в процентах',

    '1 min': '1 мин',
    '5 min': '5 мин',
    '15 min': '15 мин',

    'msec': 'милисекунды',
    'sec': 'секунды',
    'min': 'минуты',
    'hour': 'часы',
    'day': 'дни',

    'bytes': 'байты',
    'kbytes': 'килобайты',
    'mbytes': 'мегабайты',
    'gbytes': 'гигабайты',
    'tbytes': 'терабайты',
    'pbytes': 'петабайты =)',     # Seriously? =)
}


def get_string(str_id):
    if str_id in __LOCALIZED_STRINGS:
        return __LOCALIZED_STRINGS[str_id]
    else:
        return str_id