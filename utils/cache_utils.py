from functools import wraps
import logging
import utils.date_utils as date_utils


class TodayCacheManager(object):
    _date_pattern = '%Y-%m-%d'
    _today = date_utils.now_date_str('%Y-%m-%d')

    @staticmethod
    def is_today() -> bool:
        return TodayCacheManager._today == date_utils.now_date_str(TodayCacheManager._date_pattern)

    @staticmethod
    def reset_today():
        TodayCacheManager._today = date_utils.now_date_str(TodayCacheManager._date_pattern)

    @staticmethod
    def clear_cache_if_not_today(func):
        if not TodayCacheManager.is_today():
            func.cache_clear()
            TodayCacheManager.reset_today()
            logging.log(logging.INFO, f'Cache cleared for {func}')


def daily_cache_manager(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        TodayCacheManager.clear_cache_if_not_today(func)
        return func(*args, **kwargs)

    return wrapper
