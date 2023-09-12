import functools
import operator


def functools_reduce_iconcat(lst):
    return functools.reduce(operator.iconcat, lst, [])

def get_error(name, value):
    return {'error': f'Invalid {name}: {value}'}