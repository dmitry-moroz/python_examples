# Descriptor example
class Celsius(object):
    def __get__(self, instance, owner):
        print "Celsius __get__"
        return 9 * (instance.fahrenheit + 32) / 5.0

    def __set__(self, instance, value):
        print "Celsius __set__"
        instance.fahrenheit = 32 + 5 * value / 9.0

    def __delete__(self, instance):
        print "Celsius __delete__"
        instance.__dict__.pop("celsius")


class Temperature(object):
    celsius = Celsius()
    def __init__(self, initial_f):
        self.fahrenheit = initial_f


tmprt = Temperature(212)
print tmprt.celsius
tmprt.celsius = 0
print tmprt.fahrenheit
del tmprt.celsius
print tmprt.celsius
