import functools
import operator

def functools_reduce_iconcat(lst):
    return functools.reduce(operator.iconcat, lst, [])