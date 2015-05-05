#!/usr/bin/env python2
import re
from pprint import pprint
from multiprocessing import Manager, Pool


def parser(line, reg, i, arr):
    """Produces search in a line using regular expression.
    line: target line
    reg: regular expression for search
    i: line number
    arr: list for collecting results
    """
    p = re.compile(reg)
    if p.search(line) is not None:
        arr.append((i, line))


def grep(reg, name):
    """Produces search in a file using regular expression.
    reg: regular expression for search
    name: target file name
    """
    f = open(name, 'r')
    p = Pool(8)
    arr = Manager().list()
    for i, line in enumerate(f):
        p.apply_async(parser, (line, reg, i, arr))
    p.close()
    p.join()
    return arr[:]


# USING
if __name__ == '__main__':
    lines = grep(r"Error", "/var/log/messages")
    pprint(lines)
