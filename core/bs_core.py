import logging

import utils.fun_utils as fun_utils
from functools import wraps, lru_cache

import baostock as bs
import pandas as pd

import utils.stockstats_utils as ssu
import utils.date_utils as date_utils
from utils.cache_utils import daily_cache_manager

bs_date_str_pattern = '%Y-%m-%d'


class BSLoginManager(object):
    _is_login = False
    _login_func = None

    @staticmethod
    def login(func):
        if not BSLoginManager._is_login:
            bs.login()
            BSLoginManager._is_login = True
            BSLoginManager._login_func = func

    @staticmethod
    def logout(func):
        if BSLoginManager._is_login and BSLoginManager._login_func == func:
            bs.logout()
            BSLoginManager._is_login = False
            BSLoginManager._login_func = None

    @staticmethod
    def bs_login(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                BSLoginManager.login(func)
                return func(*args, **kwargs)
            finally:
                BSLoginManager.logout(func)

        return wrapper


@lru_cache(maxsize=10000, typed=True)
@BSLoginManager.bs_login
def query_name_by_code(code):
    rs = bs.query_stock_basic(code=code)
    df = rs_to_dataframe(rs)
    if df.empty:
        logging.log(logging.INFO, f'No name for code:{code}')
        return "None"
    return df['code_name'][0]


@lru_cache(maxsize=10000, typed=True)
@BSLoginManager.bs_login
def query_code_by_name(name):
    rs = bs.query_stock_basic(code_name=name)
    df = rs_to_dataframe(rs)
    if df.empty:
        logging.log(logging.INFO, f'No code for name:{name}')
        return "None"
    return df['code'][0]


def query_codes_by_names(names):
    codes = []
    for name in names:
        code = query_code_by_name(name)
        codes.append(code)
    return codes


def rs_to_dataframe(rs):
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    return pd.DataFrame(data_list, columns=rs.fields)


@daily_cache_manager
@lru_cache(maxsize=10000, typed=True)
@fun_utils.fun_log
@BSLoginManager.bs_login
def query_daily_k_by_code(code, start_date_str, end_date_str=date_utils.now_date_str(bs_date_str_pattern)):
    rs = bs.query_history_k_data_plus(code.replace('"', ''),
                                      "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                      start_date=start_date_str, end_date=end_date_str, frequency="d", adjustflag="3")
    df = rs_to_dataframe(rs)
    if df.empty:
        logging.log(logging.INFO, "query_daily_k_by_code: df is empty")
        return df
    df["open"] = pd.to_numeric(df["open"])
    df["high"] = pd.to_numeric(df["high"])
    df["low"] = pd.to_numeric(df["low"])
    df["close"] = pd.to_numeric(df["close"])
    df["preclose"] = pd.to_numeric(df["preclose"])
    df["volume"] = pd.to_numeric(df["volume"])
    df["amount"] = pd.to_numeric(df["amount"])
    df["adjustflag"] = pd.to_numeric(df["adjustflag"])
    df["turn"] = pd.to_numeric(df["turn"])
    df["tradestatus"] = pd.to_numeric(df["tradestatus"])
    df["pctChg"] = pd.to_numeric(df["pctChg"])
    df["isST"] = pd.to_numeric(df["isST"])
    codes = df['code']
    df.drop(columns=['code'])
    df = ssu.stockstats_default(df)
    df['code'] = codes
    df.sort_values(by=['date'], ascending=True, inplace=True)
    return df


@daily_cache_manager
@lru_cache(maxsize=10000, typed=True)
@BSLoginManager.bs_login
def query_daily_k_by_codes_cache(codes_str, start_date_str, end_date_str=date_utils.now_date_str(bs_date_str_pattern)):
    codes = codes_str.replace('"', '').split(',')
    df_arr = []
    for code in codes:
        df = query_daily_k_by_code(code, start_date_str, end_date_str)
        df_arr.append(df)
    return df_arr


def query_daily_k_by_codes(codes, start_date_str, end_date_str=date_utils.now_date_str(bs_date_str_pattern)):
    return query_daily_k_by_codes_cache(','.join(codes), start_date_str, end_date_str)


@daily_cache_manager
@lru_cache(maxsize=10000, typed=True)
@BSLoginManager.bs_login
def query_daily_k_json_by_codes_cache(codes_str, start_date_str,
                                      end_date_str=date_utils.now_date_str(bs_date_str_pattern)):
    codes = codes_str.replace('"', '').split(',')
    df_arr = query_daily_k_by_codes(codes, start_date_str, end_date_str)
    json_arr = []
    for df in df_arr:
        json_str = df.to_json(orient='records')
        if json_str != '[]':
            name = query_name_by_code(df['code'][0])
            json_arr.append('\"' + name + '\":' + json_str + '')
    return '{' + ','.join(json_arr) + '}'


def query_daily_k_json_by_codes(codes, start_date_str, end_date_str=date_utils.now_date_str(bs_date_str_pattern)):
    return query_daily_k_json_by_codes_cache(','.join(codes), start_date_str, end_date_str)


@daily_cache_manager
@lru_cache(maxsize=10000, typed=True)
@BSLoginManager.bs_login
def query_daily_k_json_by_names_cache(names_str, start_date_str,
                                      end_date_str=date_utils.now_date_str(bs_date_str_pattern)):
    names = names_str.replace('"', '').split(',')
    return query_daily_k_json_by_codes(query_codes_by_names(names), start_date_str, end_date_str)


def query_daily_k_json_by_names(names, start_date_str, end_date_str=date_utils.now_date_str(bs_date_str_pattern)):
    return query_daily_k_json_by_names_cache(','.join(names), start_date_str, end_date_str)
