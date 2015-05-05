# Property example
class C(object):
    def __init__(self):
        self.__x = None

    @property
    def x(self):
        print 'get'
        return self.__x

    @x.setter
    def x(self, value):
        print 'set'
        self.__x = value

    @x.deleter
    def x(self):
        del self.__x


c = C()
print c.x
c.x = 10
print c.x
