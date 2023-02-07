from abc import ABCMeta, abstractmethod
from enum import Enum
import core.ak_core as ak_core


class QueryIndexServices(Enum):
    AK = 'ak'


class QueryIndexService(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def support(service_code) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def query_index(service_code, start, end, index_name, old_date_column_name, date_pattern, new_columns,
                    new_date_column_name):
        pass

    @staticmethod
    @abstractmethod
    def query_index_json(service_code, start, end, index_name, old_date_column_name, date_pattern, new_columns,
                         new_date_column_name) -> str:
        pass


class AKQueryIndexService(QueryIndexService):
    @staticmethod
    def support(service_code) -> bool:
        return service_code == QueryIndexServices.AK.value

    @staticmethod
    def query_index(service_code, start, end, index_name, old_date_column_name, date_pattern, new_columns,
                    new_date_column_name):
        return ak_core.base_index(index_name, old_date_column_name, date_pattern, new_columns, new_date_column_name,
                                  start, end)

    @staticmethod
    def query_index_json(service_code, start, end, index_name, old_date_column_name, date_pattern, new_columns,
                         new_date_column_name) -> str:
        return ak_core.base_index_json(index_name, old_date_column_name, date_pattern, new_columns,
                                       new_date_column_name, start, end)


def query_index(service_code, start, end, index_name, old_date_column_name, date_pattern, new_columns=None,
                new_date_column_name=ak_core.def_date_col_name):
    for service in QueryIndexService.__subclasses__():
        if service.support(service_code):
            return service.query_index(service_code, start, end, index_name, old_date_column_name, date_pattern,
                                       new_columns, new_date_column_name)


def query_index_json(service_code, start, end, index_name, old_date_column_name, date_pattern, new_columns=None,
                     new_date_column_name=ak_core.def_date_col_name):
    for service in QueryIndexService.__subclasses__():
        if service.support(service_code):
            return service.query_index_json(service_code, start, end, index_name, old_date_column_name, date_pattern,
                                            new_columns, new_date_column_name)
