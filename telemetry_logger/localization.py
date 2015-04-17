# -*- coding: utf-8 -*-
from consts import TELEMETRY_FAMILY_CPU, TELEMETRY_FAMILY_MEM, TELEMETRY_FAMILY_DISK, TELEMETRY_FAMILY_NET, \
    TELEMETRY_CPU_LOAD_AVG, TELEMETRY_CPU_TIMES, TELEMETRY_CPU_TIMES_PER_CPU, TELEMETRY_CPU_PERCENT, \
    TELEMETRY_CPU_PERCENT_PER_CPU, TELEMETRY_CPU_TIMES_PERCENT, TELEMETRY_CPU_TIMES_PERCENT_PER_CPU, \
    TELEMETRY_MEM_SYSTEM, TELEMETRY_MEM_SWAP, TELEMETRY_DISK_USAGE, TELEMETRY_DISK_IO_COUNTERS, \
    TELEMETRY_DISK_IO_COUNTERS_PER_DISK, TELEMETRY_NET_IO_COUNTERS, TELEMETRY_NET_IO_COUNTERS_PER_NIC, \
    TELEMETRY_PROCESS_CPU_AFFINITY, TELEMETRY_PROCESS_MEM_INFO, TELEMETRY_PROCESS_MEM_PERCENT

__author__ = 'zebraxxl'

UNKNOWN_TELEMETRY_TYPE = 'UNKNOWN_TELEMETRY_TYPE'
SYSTEM_TELEMETRY_STRING = 'SYSTEM_TELEMETRY'
UNITS_STRING = 'UNITS_STRING'
CPU_INDEX_STRING = 'CPU_INDEX'
PERCENTS_STRING = 'PERCENTS'

__LOCALIZED_STRINGS = {
    UNKNOWN_TELEMETRY_TYPE: 'Неизвестный тип телеметрии',
    SYSTEM_TELEMETRY_STRING: 'Системная телеметрия',
    UNITS_STRING: 'Единицы измерения',
    CPU_INDEX_STRING: 'ЦПУ {index}',
    PERCENTS_STRING: 'Проценты',

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
    TELEMETRY_DISK_IO_COUNTERS: 'Ввод/Вывод диска',
    TELEMETRY_DISK_IO_COUNTERS_PER_DISK: 'Ввод/Вывод по отдельным дискам',

    TELEMETRY_NET_IO_COUNTERS: 'Ввод/Вывод сети',
    TELEMETRY_NET_IO_COUNTERS_PER_NIC: 'Ввод/Вывод по интерфейсам',

    TELEMETRY_PROCESS_CPU_AFFINITY: 'Задействование ядер',
    TELEMETRY_PROCESS_MEM_INFO: 'Использование памяти',
    TELEMETRY_PROCESS_MEM_PERCENT: 'Использование памяти в процентах',

    '1 min': '1 мин',
    '5 min': '5 мин',
    '15 min': '15 мин',

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