import core.bs_core as bs_core
import logging
import baostock as bs

logging.basicConfig(level=logging.INFO)

bs_core.login()
# df = bs_core.query_daily_k_json_by_codes(['sh.600000', 'sz.000001'], '2022-01-01')
# "sh.000090", "sh.000933", "sz.399997","sh.000932","sz.399808","sz.399928","sh.000934","sz.399935"
# df = bs_core.query_code_by_name("流通")
# df = bs_core.query_name_by_code("sh.000090")
rs = bs.query_stock_basic(code_name="消费指数")
# rs = bs.query_stock_basic(code="sh.000090")
df = bs_core.rs_to_dataframe(rs)
print(df)
bs_core.logout()
