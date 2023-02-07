import core.trading_logic_core as tlc
import utils.date_utils as date_utils

res = tlc.query_breath(date_utils.str_to_date("2020-01-01", "%Y-%m-%d"))

print(res)
