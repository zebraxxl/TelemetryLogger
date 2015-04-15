import json
import re

__author__ = 'zebraxxl'
javascript_expression_extract = re.compile(ur'\"\{\{unquote(?P<expression>[\S\s]+)unquote\}\}\"')


class GraphIdCounter():
    __next_value = 0

    def __init__(self):
        pass

    def get_next_value(self):
        result = self.__next_value
        self.__next_value += 1
        return 'graph_' + str(result)

    def mark_position(self):
        return self.__next_value

    def get_generated_ids(self, marked_position):
        return ['graph_' + str(i) for i in xrange(marked_position, self.__next_value)]


class JavaScriptInJsonExpression():
    def __init__(self, expression):
        self.expression = expression


def try_to_int(string):
    try:
        return int(string)
    except ValueError:
        return None


def check_dict_for_key(d, key, default_ctor):
    if key not in d:
        d[key] = default_ctor()


def dump_javascript(obj):
    def __default(obj):
        if isinstance(obj, JavaScriptInJsonExpression):
            return '{{{{unquote{0}unquote}}}}'.format(obj.expression)
        else:
            raise TypeError()

    def replace(m):
        return m.group('expression')

    result = json.dumps(obj, default=__default)
    return javascript_expression_extract.sub(replace, result)

