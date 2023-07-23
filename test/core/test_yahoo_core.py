# import socket
# import socks
import core.yahoo_core as yahoo
import yfinance as yf
import utils.proxy_utils as pu
# from datetime import datetime as dt
# import pytz
# import utils.date_utils as du
#
# socks.setdefaultproxy(socks.SOCKS5, "localhost", 10808)
# socket.socket = socks.socksocket
# tz = pytz.timezone("Asia/Shanghai")
# start = tz.localize(dt(2013, 1, 1))
# end = tz.localize(dt.today())
#
# res = yahoo.download_codes(['SPY'], start_str=du.last_n_days_str(10, yahoo.pattern), interval='60m')
# print(res)
#
#
# # res = yf.download('SPY', start=du.last_n_days_str(10, yahoo.pattern), period='1d', interval='1h')
# # print(res)

# pu.proxy()

# data = yahoo.download_codes_json_batch2gpt(codes=['AAPL'], start_str='2023-7-01')

# print(data)

import utils.proxy_utils as pu

pu.proxy()

import core.yahoo_core as yh
import core.number_regular as reg

df_arr = yh.download_codes_batch_by_codes_str(codes_str='QQQ,SPY', start_str='2000-01-01')

for df in df_arr:
    arr = df[['open', 'close', 'high', 'low']].values
    print(df.iloc[2]['date'])

# reg.find_similar_sequences( , ,0.1)


# print(df)
