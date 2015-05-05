import functools
import operator


def add_factory1(n):
    def func(m):
        return m+n
    return func


def add_factory2(n):
    return lambda m: m + n


def add_factory3(n):
    func = functools.partial(operator.add, n)
    return func


def decorator(m):
    def new_func(func):
        def wraped(*args, **kwargs):
            return func(*args, **kwargs) + m
        return wraped
    return new_func


def add_factory4(m):
    @decorator(m)
    def add(n):
        return n
    return add


class add_factory5(object):
    def __init__(self, m):
        self.m = m

    def __call__(self, n):
        return n + self.m


# USING
if __name__ == '__main__':
    N = 5
    M = 10
    factories = [add_factory1, add_factory2, add_factory3, add_factory4,
                 add_factory5]
    add = map(lambda f: f(N), factories)
    print map(lambda a: a(M), add)
