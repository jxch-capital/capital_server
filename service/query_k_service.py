from abc import ABCMeta, abstractmethod
from enum import Enum
import core.bs_core as bs_core
import core.pdr_core as pdr_core
import core.yahoo_core as yahoo_core
import utils.date_utils as date_utils
import service.stock_pool_service as sps
from utils.cache_utils import daily_cache_manager
from functools import lru_cache
import json

date_str_pattern = '%Y-%m-%d'


class QueryKServices(Enum):
    BS = 'bs'
    PDR = 'pdr'
    YAHOO = 'yf'


def convert_pattern(date_str, new_pattern):
    return date_utils.new_date_str_pattern(date_str, date_str_pattern, new_pattern)


class QueryKService(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def support(service_code, interval) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def query_k(service_code, codes, start_date_str, end_date_str) -> list:
        pass

    @staticmethod
    @abstractmethod
    def query_k_json(service_code, codes, start_date_str, end_date_str, interval=None) -> str:
        pass


class BSQueryKService(QueryKService):
    @staticmethod
    def support(service_code, interval) -> bool:
        return service_code == QueryKServices.BS.value and interval in bs_core.interval_support

    @staticmethod
    def query_k(service_code, codes, start_date_str, end_date_str):
        return bs_core.query_daily_k_by_codes(codes, convert_pattern(start_date_str, bs_core.bs_date_str_pattern),
                                              convert_pattern(end_date_str, bs_core.bs_date_str_pattern))

    @staticmethod
    def query_k_json(service_code, codes, start_date_str, end_date_str, interval="d"):
        return bs_core.query_daily_k_json_by_codes(codes, convert_pattern(start_date_str, bs_core.bs_date_str_pattern),
                                                   convert_pattern(end_date_str, bs_core.bs_date_str_pattern),
                                                   frequency=interval)


class PDRQueryKService(QueryKService):
    _code_split = '-'

    @staticmethod
    def ds(service_code):
        scs = service_code.split(PDRQueryKService._code_split)
        if scs[1]:
            return scs[1]
        else:
            return pdr_core.def_ds

    @staticmethod
    def support(service_code, interval) -> bool:
        return service_code.split(PDRQueryKService._code_split)[0] == QueryKServices.PDR.value and interval is None

    @staticmethod
    def query_k(service_code, codes, start_date_str, end_date_str):
        return pdr_core.data_reader_codes(codes, date_utils.str_to_date(start_date_str, date_str_pattern),
                                          date_utils.str_to_date(end_date_str, date_str_pattern),
                                          data_source=PDRQueryKService.ds(service_code))

    @staticmethod
    def query_k_json(service_code, codes, start_date_str, end_date_str, interval=None):
        return pdr_core.data_reader_codes_json(codes, date_utils.str_to_date(start_date_str, date_str_pattern),
                                               date_utils.str_to_date(end_date_str, date_str_pattern),
                                               data_source=PDRQueryKService.ds(service_code))


class YahooQueryKService(QueryKService):
    @staticmethod
    def support(service_code, interval) -> bool:
        return service_code == QueryKServices.YAHOO.value and interval in yahoo_core.interval_support

    @staticmethod
    def query_k(service_code, codes, start_date_str, end_date_str):
        return yahoo_core.download_codes_json_batch(codes, convert_pattern(start_date_str, yahoo_core.pattern),
                                                    convert_pattern(end_date_str, yahoo_core.pattern))

    @staticmethod
    def query_k_json(service_code, codes, start_date_str, end_date_str, interval="1d"):
        return yahoo_core.download_codes_json_batch(codes, convert_pattern(start_date_str, yahoo_core.pattern),
                                                    convert_pattern(end_date_str, yahoo_core.pattern),
                                                    interval=interval)


def query_k(service_code, codes, start_date, end_date, interval=None):
    for service in QueryKService.__subclasses__():
        if service.support(service_code, interval):
            if interval:
                return service.query_k(service_code, codes, start_date, end_date, interval)
            else:
                return service.query_k(service_code, codes, start_date, end_date)


def query_k_json(service_code, codes, start_date, end_date, interval=None):
    for service in QueryKService.__subclasses__():
        if service.support(service_code, interval):
            if interval:
                return service.query_k_json(service_code, codes, start_date, end_date, interval)
            else:
                return service.query_k_json(service_code, codes, start_date, end_date)


def alias_json_str(json_str, aliases):
    data = json.loads(json_str)
    return json.dumps({alias: data[key] for key, alias in zip(data.keys(), aliases)})


def query_k_json_by_stock_pool(stock_pool, start_date, end_date, interval=None):
    sp = sps.get_stock_pool(stock_pool)
    for service in QueryKService.__subclasses__():
        if service.support(sp['engine'], interval):
            if interval:
                k_json = service.query_k_json(sp['engine'], sp['codes'], start_date, end_date, interval)
            else:
                k_json = service.query_k_json(sp['engine'], sp['codes'], start_date, end_date)
            return alias_json_str(k_json, sp['codes_alias'])
