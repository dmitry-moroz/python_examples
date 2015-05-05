#!/usr/bin/env python2
from datetime import datetime


class BirthdayField(object):

    def __init__(self, value=None):
        self.birthday = value

    def __get__(self, instance, owner):
        return self.birthday

    def __set__(self, instance, value):
        if type(value) is datetime:
            self.birthday = value
        else:
            raise TypeError('Birthday must be datetime type')


class NameField(object):

    def __init__(self, value=None):
        self.name = value

    def __get__(self, instance, owner):
        return self.name

    def __set__(self, instance, value):
        if type(value) is str:
            self.name = value
        else:
            raise TypeError('Name must be string type')


class PhoneField(object):

    def __init__(self, value=None):
        self.phone = value

    def __get__(self, instance, owner):
        d = self.phone.split(' ')
        return('{0} ({1}) {2}-{3}-{4}'
               .format(d[0], d[1], d[2][:3], d[2][3:5], d[2][5:7]))

    def __set__(self, instance, value):
        if type(value) is not str:
            raise TypeError('Name must be string type')
        if value.replace(' ','').isdigit() and len(value) == 14:
            self.phone = value
        else:
            raise ValueError('Phone must be in format XXX XX XXXXXXX')


class Person(object):
    name = NameField()
    birthday = BirthdayField()
    phone = PhoneField()

# USING
if __name__ == '__main__':
    dima = Person()
    dima.birthday = datetime.strptime("1993-08-09", "%Y-%m-%d")
    print dima.birthday
    dima.name = 'Dmitry Moroz'
    print dima.name
    dima.phone = "375 29 1210008"
    print dima.phone
