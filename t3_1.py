#!/usr/bin/env python2
class Fake(object):

    def __call__(self, *args, **kwargs):
        return Fake()

    def __getitem__(self, item):
        return Fake()

    def __getattr__(self, item):
        return Fake()


if __name__ == '__main__':
    fake = Fake()
    fake.non_existing_method('asdfa')
    fake.attribute
    fake[4]
    fake['non existing key']
    fake2 = fake.blablabla()
    fake2.some_name()
    fake2.whatever.again_whatever().and_again['yury'][1]