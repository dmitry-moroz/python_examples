#!/usr/bin/env python2
class API(object):

    def doc_parser(self, obj):
        res = ''
        for key in obj.__dict__:
            if key[:2] == '__' and key[-2:] == '__':
                continue
            if (isinstance(obj.__dict__[key], (int, float, str, list,
                                               dict, tuple, bool)) or
                    not obj.__dict__[key].__doc__):
                res += '%s: %s\n' % (key, str(type(obj.__dict__[key]))[7:-2])
            else:
                res += '%s: %s\n' % (key, obj.__dict__[key].__doc__)
        return res

    def __get__(self, instance, owner):
        result = ''
        result += self.doc_parser(owner)
        if instance:
            result += self.doc_parser(instance)
        return result


class Foo(object):
     __doc__ = API()
     def __init__(self, x):
         self.x = x
     def func1(self, y):
         """Multiplies two values self.x and y."""
         return self.x * y
     def func2(self, y):
         return self.x / y

# USING
if __name__ == '__main__':
    print Foo.__doc__
    foo = Foo(10)
    print foo.__doc__
