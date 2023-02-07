import core.ak_core as ak_core

# res = ak_core.ak_base_index('macro_china_xfzxx')

res = ak_core.base_index_json('macro_china_xfzxx', '月份', '%Y年%m月份')

print(res)
