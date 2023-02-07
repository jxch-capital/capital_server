import json
from datetime import datetime, date

from pandas import DataFrame
import functools
from service.query_k_service import date_str_pattern
import time


def json_dumps_default_date(obj, pattern=date_str_pattern):
    if isinstance(obj, datetime):
        return obj.strftime(pattern)
    elif isinstance(obj, date):
        return obj.strftime(pattern)
    else:
        return obj


def json_dumps_timestamp_date(obj):
    if isinstance(obj, datetime):
        return int(obj.timestamp() * 1000)
    elif isinstance(obj, date):
        return int(time.mktime(obj.timetuple()) * 1000)
    else:
        return obj


def to_json(obj, json_date_fmt_func=json_dumps_default_date, pattern=None):
    if type(obj) is str:
        return obj
    if type(obj) is dict or type(obj) is list:
        return json.dumps(obj, ensure_ascii=False, default=json_date_fmt_func)
    if type(obj) is DataFrame:
        return json.dumps(obj.to_dict('records'), ensure_ascii=False, default=json_date_fmt_func)
    raise TypeError("不支持的转JSON类型")


def return_json(func, json_date_fmt_func=json_dumps_default_date, pattern=None):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        res = func(*args, **kw)
        return to_json(res, json_date_fmt_func, pattern)

    return wrapper
