import datetime
import random
import string

import pytz


def timestamp_now():
    ukraine_timezone = pytz.timezone('Europe/Kiev')
    current_time = datetime.datetime.now(ukraine_timezone)
    return int(current_time.timestamp())


def datetime_now():
    ukraine_timezone = pytz.timezone('Europe/Kiev')
    return datetime.datetime.utcnow()


def random_string(N):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(N))
