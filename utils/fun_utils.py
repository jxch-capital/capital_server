from functools import wraps
import logging


def fun_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.log(logging.INFO, f"{func.__name__} called. args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)

    return wrapper
