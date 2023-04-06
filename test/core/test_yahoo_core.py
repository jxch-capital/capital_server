import socket
import socks
import core.yahoo_core as yahoo
import yfinance as yf
from datetime import datetime as dt
import pytz
import utils.date_utils as du

socks.setdefaultproxy(socks.SOCKS5, "localhost", 10808)
socket.socket = socks.socksocket
tz = pytz.timezone("America/New_York")
start = tz.localize(dt(2013, 1, 1))
end = tz.localize(dt.today())

res = yahoo.download_codes_json(['000007.SZ'], start_str=du.last_n_days_str(30, yahoo.pattern))
print(res)
