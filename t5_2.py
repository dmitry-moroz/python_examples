from datetime import datetime
from t2 import run, get_handler


@get_handler('/date')
def date():
    return datetime.now()

# USING
if __name__ == '__main__':
    run()