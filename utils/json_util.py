import json
from datetime import datetime, date

from pandas import DataFrame
import functools
from service.query_k_service import date_str_pattern


def json_dumps_default_date(obj, fmt=date_str_pattern):
    if isinstance(obj, datetime):
        return obj.strftime(fmt)
    elif isinstance(obj, date):
        return obj.strftime(fmt)
    else:
        return obj


def to_json(obj, json_date_fmt_func=json_dumps_default_date):
    if type(obj) is str:
        return obj
    if type(obj) is dict or type(obj) is list:
        return json.dumps(obj, ensure_ascii=False, default=json_date_fmt_func)
    if type(obj) is DataFrame:
        return json.dumps(obj.to_dict('records'), ensure_ascii=False, default=json_date_fmt_func)
    raise TypeError("不支持的转JSON类型")


def return_json(func, json_date_fmt_func=json_dumps_default_date):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        res = func(*args, **kw)
        return to_json(res, json_date_fmt_func)

    return wrapper
