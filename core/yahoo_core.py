import yfinance as yf
import pytz
import utils.date_utils as du
import utils.stockstats_utils as ssu
import utils.fun_utils as fun_utils
from functools import lru_cache
from utils.cache_utils import daily_cache_manager

tz = pytz.timezone("America/New_York")
pattern = '%Y-%m-%d'


@daily_cache_manager
@lru_cache(maxsize=10000, typed=True)
@fun_utils.fun_log
def download(code, start_str, end_str=du.now_date_str(pattern)):
    # df = yf.download(code, start=timezone.localize(du.str_to_date(start_str, pattern)),
    #                  end=timezone.localize(du.str_to_date(end_str, pattern)))
    df = yf.download(code, start=start_str, end=end_str, period='1d')
    df = ssu.stockstats_default(df)
    df['code'] = code
    df.sort_values(by=['Date'], ascending=True, inplace=True)

    return df


def download_codes(code_arr, start_str, end_str=du.now_date_str(pattern), timezone=tz):
    df_arr = []
    for code in code_arr:
        df = download(code, start_str, end_str)
        df_arr.append(df)
    return df_arr


def download_codes_json(codes, start_str, end_str=du.now_date_str(pattern), timezone=tz):
    df_arr = download_codes(codes, start_str, end_str)
    json_arr = []
    for df in df_arr:
        json_str = df.to_json(orient='records')
        if json_str != '[]':
            code = df['code'][0].replace('.', '').replace('^', '')
            json_arr.append('\"' + code + '\":' + json_str + '')
    return '{' + ','.join(json_arr) + '}'
