from abc import ABCMeta, abstractmethod
from enum import Enum
import core.bs_core as bs_core
import utils.date_utils as date_utils

date_str_pattern = '%Y-%m-%d'


class QueryKServices(Enum):
    BS = 'bs'


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
    def query_k(codes, start_date_str, end_date_str):
        pass

    @staticmethod
    @abstractmethod
    def query_k_json(codes, start_date_str, end_date_str):
        pass


class BSQueryKService(QueryKService):
    @staticmethod
    def support(service_code) -> bool:
        return service_code == QueryKServices.BS.value

    @staticmethod
    @bs_core.bs_login
    def query_k(codes, start_date_str, end_date_str):
        return bs_core.query_daily_k_by_codes(codes, convert_pattern(start_date_str, bs_core.bs_date_str_pattern),
                                              convert_pattern(end_date_str, bs_core.bs_date_str_pattern))

    @staticmethod
    @bs_core.bs_login
    def query_k_json(codes, start_date_str, end_date_str):
        return bs_core.query_daily_k_json_by_codes(codes, convert_pattern(start_date_str, bs_core.bs_date_str_pattern),
                                                   convert_pattern(end_date_str, bs_core.bs_date_str_pattern))


def query_k(service_code, codes, start_date, end_date):
    for service in QueryKService.__subclasses__():
        if service.support(service_code):
            return service.query_k(codes, start_date, end_date)


def query_k_json(service_code, codes, start_date, end_date):
    for service in QueryKService.__subclasses__():
        if service.support(service_code):
            return service.query_k_json(codes, start_date, end_date)
