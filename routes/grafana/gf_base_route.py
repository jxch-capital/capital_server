from flask import Blueprint

gf_base_route = Blueprint('gf_base_route', __name__)


@gf_base_route.route("/grafana/", methods=["get"])
def grafana_root():
    return '{"status":"success"}'
