import datetime
import random
import string


def timestamp_now():
    return int(datetime.datetime.utcnow().timestamp())


def datetime_now():
    return datetime.datetime.utcnow()


def random_string(N):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(N))
