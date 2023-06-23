import yfinance as yf
import pytz
import utils.date_utils as du
import utils.stockstats_utils as ssu
import utils.fun_utils as fun_utils
from functools import lru_cache
from utils.cache_utils import daily_cache_manager
import pandas as pd

tz = pytz.timezone("America/New_York")
pattern = '%Y-%m-%d'
interval_support = [None, '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']


@daily_cache_manager
@lru_cache(maxsize=10000, typed=True)
@fun_utils.fun_log
def download(code, start_str, end_str=du.now_date_str(pattern), interval='1d', use_index=True):
    try:
        df = yf.download(code, start=start_str, end=end_str, period='1d', interval=interval)
    except BaseException:
        df = yf.download(code, start=start_str, end=end_str, period='max', interval=interval)

    if 'Datetime' == df.index.name:
        df['Date'] = df.index

    if use_index:
        df = ssu.stockstats_default(df)
    df['code'] = code

    # df.sort_values(by=['Date'], ascending=True, inplace=True)

    return df


def download_codes(code_arr, start_str, end_str=du.now_date_str(pattern), interval='1d', timezone=tz):
    df_arr = []
    for code in code_arr:
        try:
            df = download(code, start_str, end_str, interval=interval)
            df_arr.append(df)
        except BaseException:
            df_arr.append(pd.DataFrame.from_records([{'code': code}]))
    return df_arr


def df_arr2json(df_arr):
    json_arr = []
    for df in df_arr:
        json_str = df.to_json(orient='records')
        if json_str != '[]':
            code = df['code'][0].replace('.', '').replace('^', '')
            json_arr.append('\"' + code + '\":' + json_str + '')
    return '{' + ','.join(json_arr) + '}'


def download_codes_json(codes, start_str, end_str=du.now_date_str(pattern), interval='1d', timezone=tz):
    df_arr = download_codes(codes, start_str, end_str, interval=interval)
    return df_arr2json(df_arr)


def download_codes_batch(code_arr, start_str, end_str=du.now_date_str(pattern), interval='1d', timezone=tz,
                         use_index=False):
    data = yf.download(tickers=code_arr, start=start_str, end=end_str, interval=interval)
    df_arr = []
    for code in code_arr:
        df = data.xs(key=code, level=1, axis=1).copy()
        df.dropna(inplace=True)
        if 'Datetime' == df.index.name:
            df['Date'] = df.index
        if use_index:
            df = ssu.stockstats_default(df)
        df['code'] = code
        df.columns = df.columns.str.lower()
        df_arr.append(df)
    return df_arr


@daily_cache_manager
@lru_cache(maxsize=10000, typed=True)
@fun_utils.fun_log
def download_codes_batch_by_codes_str(codes_str, start_str, end_str=du.now_date_str(pattern), interval='1d',
                                      timezone=tz):
    return download_codes_batch(codes_str.split(','), start_str, end_str, interval, timezone)


def download_codes_json_batch(codes, start_str, end_str=du.now_date_str(pattern), interval='1d', timezone=tz):
    df_arr = download_codes_batch_by_codes_str(','.join(codes), start_str, end_str, interval=interval)
    return df_arr2json(df_arr)
