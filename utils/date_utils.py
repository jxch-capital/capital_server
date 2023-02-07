from datetime import datetime as dt
import datetime
import time


def date_to_str(date, pattern):
    return date.strftime(pattern)


def str_to_date(date_str, pattern):
    return datetime.datetime.strptime(date_str, pattern)


def today():
    return dt.now()


def now_date_str(pattern):
    return datetime.date.today().strftime(pattern)


def last_n_days(n):
    return dt.now() - datetime.timedelta(days=n)


def last_n_days_str(n, pattern):
    return date_to_str(dt.now() - datetime.timedelta(days=n), pattern)


def s_timestamp_to_str(timestamp, pattern):
    return time.strftime(pattern, time.localtime(timestamp))


def new_date_str_pattern(date_str, old_pattern, new_pattern):
    date = str_to_date(date_str, old_pattern)
    return date_to_str(date, new_pattern)


def timestamp_to_date(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).date()
