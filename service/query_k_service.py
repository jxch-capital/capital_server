from abc import ABCMeta, abstractmethod
from enum import Enum
import core.bs_core as bs_core
import core.pdr_core as pdr_core
import utils.date_utils as date_utils
from utils.cache_utils import daily_cache_manager
from functools import lru_cache

date_str_pattern = '%Y-%m-%d'


class QueryKServices(Enum):
    BS = 'bs'
    PDR = 'pdr'


def convert_pattern(date_str, new_pattern):
    return date_utils.new_date_str_pattern(date_str, date_str_pattern, new_pattern)


class QueryKService(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def support(service_code) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def query_k(service_code, codes, start_date_str, end_date_str) -> list:
        pass

    @staticmethod
    @abstractmethod
    def query_k_json(service_code, codes, start_date_str, end_date_str) -> str:
        pass


class BSQueryKService(QueryKService):
    @staticmethod
    def support(service_code) -> bool:
        return service_code == QueryKServices.BS.value

    @staticmethod
    def query_k(service_code, codes, start_date_str, end_date_str):
        return bs_core.query_daily_k_by_codes(codes, convert_pattern(start_date_str, bs_core.bs_date_str_pattern),
                                              convert_pattern(end_date_str, bs_core.bs_date_str_pattern))

    @staticmethod
    def query_k_json(service_code, codes, start_date_str, end_date_str):
        return bs_core.query_daily_k_json_by_codes(codes, convert_pattern(start_date_str, bs_core.bs_date_str_pattern),
                                                   convert_pattern(end_date_str, bs_core.bs_date_str_pattern))


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
    def support(service_code) -> bool:
        return service_code.split(PDRQueryKService._code_split)[0] == QueryKServices.PDR.value

    @staticmethod
    def query_k(service_code, codes, start_date_str, end_date_str):
        return pdr_core.data_reader_codes(codes, date_utils.str_to_date(start_date_str, date_str_pattern),
                                          date_utils.str_to_date(end_date_str, date_str_pattern),
                                          data_source=PDRQueryKService.ds(service_code))

    @staticmethod
    def query_k_json(service_code, codes, start_date_str, end_date_str):
        return pdr_core.data_reader_codes_json(codes, date_utils.str_to_date(start_date_str, date_str_pattern),
                                               date_utils.str_to_date(end_date_str, date_str_pattern),
                                               data_source=PDRQueryKService.ds(service_code))


def query_k(service_code, codes, start_date, end_date):
    for service in QueryKService.__subclasses__():
        if service.support(service_code):
            return service.query_k(service_code, codes, start_date, end_date)


def query_k_json(service_code, codes, start_date, end_date):
    for service in QueryKService.__subclasses__():
        if service.support(service_code):
            return service.query_k_json(service_code, codes, start_date, end_date)
