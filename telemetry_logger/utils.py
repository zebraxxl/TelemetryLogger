__author__ = 'zebraxxl'


def try_to_int(string):
    try:
        return int(string)
    except ValueError:
        return None


def check_dict_for_key(d, key, default_ctor):
    if key not in d:
        d[key] = default_ctor()
