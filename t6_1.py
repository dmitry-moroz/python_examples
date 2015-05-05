class MetaClass(type):

    def __new__(mcs, name, bases, dct):
        dct['make_with_mixin'] = classmethod(MetaClass.make_with_mixin)
        return super(MetaClass, mcs).__new__(mcs, name, bases, dct)

    @staticmethod
    def make_with_mixin(cls, mixcls):
        if mixcls not in cls.__bases__:
            cls.__bases__ = (mixcls,) + cls.__bases__
        return cls


class Creature(object):

    def __init__(self, genus):
        self.genus = genus

    def sound(self, msg):
        print "{0}: {1}".format(self.genus, msg)


class Man(Creature):

    __metaclass__ = MetaClass

    def __init__(self, name):
        super(Man, self).__init__("man")
        self.name = name


class SingMixin(object):

    def sing(self):
        self.sound("La la li la, la la la")


# USING
if __name__ == '__main__':
    Singner = Man.make_with_mixin(SingMixin)
    dima = Singner("Dima")
    dima.sing()
