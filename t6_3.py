import types
from time import sleep
from multiprocessing import Process, Manager


class CacheMeta(type):

    timeout = 10
    cache = Manager().dict()
    cache_cleaner = None

    def __new__(mcs, name, bases, dct):
        if CacheMeta.cache_cleaner is None:
            CacheMeta.cache_cleaner = Process(
                target=CacheMeta.cleaner,
                args=(CacheMeta.cache, CacheMeta.timeout)
            )
            CacheMeta.cache_cleaner.start()

        dct['cache'] = CacheMeta.cache
        for name in dct:
            if name.startswith('__') and name.endswith('__'):
                continue
            if isinstance(dct[name], types.FunctionType):
                dct[name] = CacheMeta.cache_func(dct[name])

        return super(CacheMeta, mcs).__new__(mcs, name, bases, dct)

    @staticmethod
    def cache_func(func):
        def cached(self, *args, **kwargs):
            key = self.__repr__() + args.__repr__() + kwargs.__repr__()
            if key in self.cache.keys():
                return self.cache.get(key)
            else:
                result = func(self, *args, **kwargs)
                self.cache.update({key: result})
                return result
        return cached

    @staticmethod
    def cleaner(cache, t):
        while True:
            try:
                for i in xrange(t*2):
                    if not hasattr(cache, 'clear'):
                        raise AttributeError
                    sleep(0.5)
                cache.clear()
            except (AttributeError, IOError):
                break


class Foo(object):

    __metaclass__ = CacheMeta

    def __init__(self, x):
        self.x = x

    def mul(self, y):
        # There is very long processing/calculation
        sleep(2)
        return self.x * y


# USING
if __name__ == '__main__':
    foo = Foo(100)
    bar = Foo(200)
    print foo.mul(10)
    print foo.mul(10)
    print bar.mul(10)
    print bar.mul(10)
    print 'Wait for 11s to be sure that cache is clear ...'
    sleep(11)
    print 'Sleep finished.'
    print foo.mul(10)
    print foo.mul(10)
    print bar.mul(10)
    print bar.mul(10)
