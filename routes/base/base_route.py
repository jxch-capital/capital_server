from flask import Blueprint, request
from pre_request import pre, Rule
from utils.flask_util import param_list, param
from utils.date_utils import new_date_str_pattern as convert_pattern
import service.query_k_service as query_k_service
import service.query_breath_service as query_breath_service
import service.stock_pool_service as stock_pool_service

base_route = Blueprint('base_route', __name__)

date_str_pattern = '%Y-%m-%d'

fields_query_k_json = {
    "service_code": Rule(type=str, required=True, dest="service_code"),
    "start": Rule(type=str, required=True, dest="start"),
    "end": Rule(type=str, required=True, dest="end"),
    "interval": Rule(type=str, required=False, dest="interval"),
}

fields_query_k_json_by_stock_pool = {
    "stock_pool": Rule(type=str, required=True, dest="stock_pool"),
    "start": Rule(type=str, required=True, dest="start"),
    "end": Rule(type=str, required=True, dest="end"),
    "interval": Rule(type=str, required=False, dest="interval"),
}

fields_query_breath_json = {
    "service_code": Rule(type=str, required=True, dest="service_code"),
    "start": Rule(type=str, required=True, dest="start"),
    "end": Rule(type=str, required=True, dest="end"),
}


@base_route.route("/base/query_k_json", methods=["post", "get"])
@pre.catch(fields_query_k_json)
def query_k_json():
    service_code = param("service_code", request)
    interval = param("interval", request)
    codes = param_list("codes", request)
    start = convert_pattern(param("start", request), date_str_pattern, query_k_service.date_str_pattern)
    end = convert_pattern(param("end", request), date_str_pattern, query_k_service.date_str_pattern)
    return query_k_service.query_k_json(service_code, codes, start, end, interval)


@base_route.route("/base/query_stock_pool", methods=["post", "get"])
def query_stock_pool():
    return stock_pool_service.get_all_stock_pool_json()


@base_route.route("/base/query_k_json_by_stock_pool", methods=["post", "get"])
@pre.catch(fields_query_k_json_by_stock_pool)
def query_k_json_by_stock_pool():
    interval = param("interval", request)
    stock_pool = param("stock_pool", request)
    start = convert_pattern(param("start", request), date_str_pattern, query_k_service.date_str_pattern)
    end = convert_pattern(param("end", request), date_str_pattern, query_k_service.date_str_pattern)
    return query_k_service.query_k_json_by_stock_pool(stock_pool, start, end, interval)


@base_route.route("/base/query_breath_json", methods=["post", "get"])
@pre.catch(fields_query_breath_json)
def query_breath_json():
    service_code = param("service_code", request)
    start = convert_pattern(param("start", request), date_str_pattern, query_breath_service.date_str_pattern)
    end = convert_pattern(param("end", request), date_str_pattern, query_breath_service.date_str_pattern)
    return query_breath_service.query_breath_json(service_code, start, end)
