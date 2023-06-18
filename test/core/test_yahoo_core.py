# import socket
# import socks
# import core.yahoo_core as yahoo
# import yfinance as yf
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
