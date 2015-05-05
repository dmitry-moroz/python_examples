import types


class LinterMeta(type):

    def __new__(mcs, name, bases, dct):
        for name in dct:
            if name.startswith('__') and name.endswith('__'):
                continue
            if any(map(lambda c: c.isupper(), list(name))):
                raise AttributeError("'{0}' has no snake-case style."
                                     .format(name))
            if isinstance(dct[name], types.FunctionType):
                if not dct[name].__doc__:
                    raise AttributeError("'{0}' has no documentation string."
                                         .format(name))
                elif '  ' in dct[name].__doc__:
                    raise AttributeError("'{0}' has more than one space "
                                         "delimiter between words in "
                                         "documentation string."
                                         .format(name))
        return super(LinterMeta, mcs).__new__(mcs, name, bases, dct)


class Creature(object):

    __metaclass__ = LinterMeta

    def __init__(self, genus):
        self.genus = genus

    def sound_func(self, msg):
        """sound func"""
        print "{0}: {1}".format(self.genus, msg)


# USING
if __name__ == '__main__':
    man = Creature("man")
