# import core.trading_logic_core as tlc
# import core.pdr_core as pdr
# import utils.date_utils as date_utils
# import socket
# import socks
# import urllib.request
# import pandas_datareader.data as web
# import yfinance as yf
# import pytz
# from datetime import datetime as dt
# tz = pytz.timezone("America/New_York")
# start = tz.localize(dt(2013,1,1))
# end = tz.localize(dt.today())
#
#
# socks.setdefaultproxy(socks.SOCKS5, "localhost", 10808)
# socket.socket = socks.socksocket
# #
# #
# # # data = urllib.request.urlopen("http://www.youtube.com").read()
# # # df = web.DataReader('GE', 'yahoo', start='2019-09-10', end='2019-10-09')
# # df = yf.download('USDJPY=X', start='2019-09-10', end='2019-10-09')
# # print(df)
#
# df = pdr.data_reader('AAPL.US', '2020-01-01', date_utils.now_date_str('%Y-%m-%d'))
# print(df)

