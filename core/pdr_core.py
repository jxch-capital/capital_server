import pandas_datareader.data as web
import utils.stockstats_utils as ssu
import datetime
import utils.fun_utils as fun_utils
from functools import lru_cache
from utils.cache_utils import daily_cache_manager

def_ds = 'stooq'


@daily_cache_manager
@lru_cache(maxsize=10000, typed=True)
@fun_utils.fun_log
def data_reader(code, start_date, end_date=datetime.datetime.now(), data_source=def_ds):
    df = web.DataReader(code, data_source, start_date, end_date)
    df = ssu.stockstats_default(df)
    df['code'] = code
    return df


def data_reader_codes(codes, start_date, end_date=datetime.datetime.now(), data_source=def_ds):
    df_arr = []
    for code in codes:
        df = data_reader(code, start_date, end_date, data_source)
        df_arr.append(df)
    return df_arr


def data_reader_codes_json(codes, start_date, end_date=datetime.datetime.now(), data_source=def_ds):
    df_arr = data_reader_codes(codes, start_date, end_date, data_source)
    json_arr = []
    for df in df_arr:
        json_str = df.to_json(orient='records')
        if json_str != '[]':
            code = df['code'][0].replace('.', '').replace('^', '')
            json_arr.append('\"' + code + '\":' + json_str + '')
    return '{' + ','.join(json_arr) + '}'
