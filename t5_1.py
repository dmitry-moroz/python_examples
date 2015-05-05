from datetime import datetime
from t2 import run, MyHandler


class Date(MyHandler):

    __url__ = '/date'

    @staticmethod
    def get_handler():
        return datetime.now()

# USING
if __name__ == '__main__':
    run()