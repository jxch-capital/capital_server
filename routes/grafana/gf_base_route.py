from flask import Blueprint, request
from pre_request import pre, Rule
from utils.flask_util import param_list, param
import utils.date_utils as date_utils
import service.query_k_service as query_k_service
import service.query_breath_service as query_breath_service
import service.query_index_service as query_index_service

gf_base_route = Blueprint('gf_base_route', __name__)

fields_query_k_json = {
    "service_code": Rule(type=str, required=True, dest="service_code"),
    "codes": Rule(type=list, required=True, dest="codes"),
    "start": Rule(type=int, required=True, dest="start"),
    "end": Rule(type=int, required=True, dest="end"),
}

fields_query_breath_json = {
    "service_code": Rule(type=str, required=True, dest="service_code"),
    "start": Rule(type=int, required=True, dest="start"),
    "end": Rule(type=int, required=True, dest="end"),
}


def start_param(pattern=None):
    timestamp = int(param("start", request)) // 1000
    return date_utils.s_timestamp_to_str(timestamp, pattern) if pattern else timestamp


def end_param(pattern=None):
    timestamp = int(param("end", request)) // 1000
    return date_utils.s_timestamp_to_str(timestamp, pattern) if pattern else timestamp


@gf_base_route.route("/grafana/", methods=["get"])
def grafana_root():
    return '{"status":"success"}'


@gf_base_route.route("/grafana/query_k_json", methods=["post", "get"])
@pre.catch(fields_query_k_json)
def query_k_json():
    service_code = param("service_code", request)
    codes = param_list("codes", request)
    start = start_param(query_k_service.date_str_pattern)
    end = end_param(query_k_service.date_str_pattern)
    return query_k_service.query_k_json(service_code, codes, start, end)


@gf_base_route.route("/grafana/query_breath_json", methods=["post", "get"])
@pre.catch(fields_query_breath_json)
def query_breath_json():
    service_code = param("service_code", request)
    start = start_param(query_breath_service.date_str_pattern)
    end = end_param(query_breath_service.date_str_pattern)
    return query_breath_service.query_breath_json(service_code, start, end)


@gf_base_route.route("/grafana/query_index", methods=["post", "get"])
def query_index():
    service_code = param("service_code", request)
    start = start_param()
    end = end_param()
    index_name = param("index_name", request)
    old_date_column_name = param("old_date_column_name", request)
    date_pattern = param("date_pattern", request)
    new_columns = param_list("new_columns", request)
    new_date_column_name = param("new_date_column_name", request)
    return query_index_service.query_index_json(service_code, start, end, index_name, old_date_column_name, date_pattern, new_columns, new_date_column_name)
