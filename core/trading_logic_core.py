import requests
from functools import lru_cache
from utils.cache_utils import daily_cache_manager
import json
import utils.date_utils as date_utils
from datetime import datetime
import utils.fun_utils as fun_utils

date_str_pattern = '%Y-%m-%d'


@daily_cache_manager
@lru_cache(maxsize=1, typed=True)
@fun_utils.fun_log
def breath_list_json_str():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    }
    url = "https://www.trading-logic.com/index.html"
    res_text = requests.get(url, headers=headers).text
    res_text = res_text.split("<script type=\"application/json\" data-for=\"river\">")[1].split("</script>")[0]
    res_text = res_text.split("\"data\":")[1].split("}]")[0]
    return res_text


@daily_cache_manager
@lru_cache(maxsize=1, typed=True)
@fun_utils.fun_log
def query_breath(start_date, end_date=date_utils.today()):
    obj = {}
    for lis in json.loads(breath_list_json_str()):
        if lis[2] not in obj:
            obj[lis[2]] = []
        breath_date = date_utils.str_to_date(lis[0], date_str_pattern)
        if start_date <= breath_date <= end_date:
            obj[lis[2]].append({'date': int(datetime.timestamp(breath_date) * 1000), 'value': lis[1]})
    return obj


@daily_cache_manager
@lru_cache(maxsize=1, typed=True)
@fun_utils.fun_log
def query_breath_json(start_date, end_date=date_utils.today()):
    return json.dumps(query_breath(start_date, end_date))
