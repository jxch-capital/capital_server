import core.bs_core as bs_core
import logging

logging.basicConfig(level=logging.INFO)

bs_core.login()
df = bs_core.query_daily_k_json_by_codes(['sh.600000', 'sz.000001'], '2022-01-01')
print(df)
bs_core.logout()
