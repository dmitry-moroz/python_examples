#!/usr/bin/env python2
import urllib2
import re
from pprint import pprint
from multiprocessing import Manager, Process


def parser(url, d):
    """Parses http links from specified URL
    and adds it to dictionary.
    url: target URL
    d: dictionary for collecting links
    """
    try:
        response = urllib2.urlopen(url).read()
        links = re.findall('"http(s?://.*?)"', response)
        d[url] = map(lambda l: 'http' + l, links)
    except:
        d[url] = 'Error'


def links_finder(urls):
    """Parses http links from URLs specified in list.
    urls: list with target URLs
    return: dictionary with http links
    """
    d = Manager().dict()
    processes = []
    for url in urls:
        p = Process(target=parser, args=(url, d))
        p.start()
        processes.append(p)
    map(lambda p: p.join(), processes)
    return dict(d.items())


# USING
if __name__ == '__main__':
    links = links_finder(["http://www.goole.com", "http://www.github.com"])
    pprint(links)
