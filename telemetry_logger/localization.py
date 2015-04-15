__author__ = 'zebraxxl'

UNKNOWN_TELEMETRY_TYPE = 'UNKNOWN_TELEMETRY_TYPE'

__LOCALIZED_STRINGS = {

}


def get_string(str_id):
    if str_id in __LOCALIZED_STRINGS:
        return __LOCALIZED_STRINGS[str_id]
    else:
        return str_id