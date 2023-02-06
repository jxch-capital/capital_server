from flask import Blueprint, request
from pre_request import pre, Rule
from utils.flask_util import param_list, param
import utils.date_utils as date_utils
import service.query_k_service as query_k_service

gf_base_route = Blueprint('gf_base_route', __name__)

fields = {
    "service_code": Rule(type=str, required=True, dest="service_code"),
    "codes": Rule(type=list, required=True, dest="codes"),
    "start": Rule(type=int, required=True, dest="start"),
    "end": Rule(type=int, required=True, dest="end"),
}


@gf_base_route.route("/grafana/", methods=["get"])
def grafana_root():
    return '{"status":"success"}'


@gf_base_route.route("/grafana/query_k_json", methods=["post", "get"])
@pre.catch(fields)
def query_k_json():
    service_code = param("service_code", request)
    codes = param_list("codes", request)
    start = date_utils.s_timestamp_to_str(int(param("start", request)) // 1000, query_k_service.date_str_pattern)
    end = date_utils.s_timestamp_to_str(int(param("end", request)) // 1000, query_k_service.date_str_pattern)
    return query_k_service.query_k_json(service_code, codes, start, end)
