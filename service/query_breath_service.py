from abc import ABCMeta, abstractmethod
from enum import Enum
import utils.date_utils as date_utils
import core.trading_logic_core as tlc

date_str_pattern = tlc.date_str_pattern


class QueryBreathServices(Enum):
    TL = 'tl'


class QueryBreathService(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def support(service_code) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def query_breath(service_code, start_date_str, end_date_str):
        pass

    @staticmethod
    @abstractmethod
    def query_breath_json(service_code, start_date_str, end_date_str) -> str:
        pass


class TLQueryBreathService(QueryBreathService):
    @staticmethod
    def support(service_code) -> bool:
        return service_code == QueryBreathServices.TL.value

    @staticmethod
    def query_breath(service_code, start_date_str, end_date_str):
        return tlc.query_breath(date_utils.str_to_date(start_date_str, date_str_pattern),
                                date_utils.str_to_date(end_date_str, date_str_pattern))

    @staticmethod
    def query_breath_json(service_code, start_date_str, end_date_str) -> str:
        return tlc.query_breath_json(date_utils.str_to_date(start_date_str, date_str_pattern),
                                     date_utils.str_to_date(end_date_str, date_str_pattern))


def query_breath(service_code, start_date, end_date):
    for service in QueryBreathService.__subclasses__():
        if service.support(service_code):
            return service.query_breath(service_code, start_date, end_date)


def query_breath_json(service_code, start_date, end_date):
    for service in QueryBreathService.__subclasses__():
        if service.support(service_code):
            return service.query_breath_json(service_code, start_date, end_date)
