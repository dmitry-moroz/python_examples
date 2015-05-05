#!/usr/bin/env python2
import json
import urllib2


def key_parser(data, keys, res=None):
    """Parses data with json format, finds dictionary
    with specified keys and appends it to result list.
    data: target data with json format
    keys: keys for finding
    res: variable with accumulated result
    return: res variable with accumulated result
    """
    if res is None:
        res = []
    if isinstance(data, dict):
        if all(map(lambda k: k in data, keys)):
            res.append(dict(map(lambda k: (k, data[k]), keys)))
        for j in map(lambda key: data[key], data.keys()):
            key_parser(j, keys, res)
    elif isinstance(data, (tuple, list)):
        for j in data:
            key_parser(j, keys, res)
    return res


def reddit(addr):
    """Provides generator over titles from specified URL.
    addr: target URL
    return: generator over titles from target URL
    """
    response = urllib2.urlopen(addr)
    if response:
        def func(likes=0):
            """Generator over titles from response variable
            @ups: minimum count of likes for title
            return: sorted by likes count titles
            """
            result = json.load(response)
            topics = filter(lambda x: x['ups'] >= likes,
                            key_parser(result, ['title', 'ups']))
            topics = sorted(topics, key=lambda x: x['ups'])
            for t in topics:
                yield u'[{0}] {1}'.format(t['ups'], t['title'])
        return func
    else:
        return False

# USING
if __name__ == '__main__':
    python = reddit("http://www.reddit.com/r/python.json")
    if python:
        for title in python():
            print title
    else:
        print 'Unable to open URL'
