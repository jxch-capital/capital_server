import core.bs_core as bs_core

bs_core.login()
df = bs_core.query_daily_k_json_by_codes(['sh.600000', 'sz.000001'], '2010-01-01')
print(df)
bs_core.logout()
