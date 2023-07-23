import service.dtw as dtw
import utils.proxy_utils as pu
import core.yahoo_core as yh
pu.proxy()


code = yh.download_codes_batch_by_codes_str(codes_str='SPY', start_str='2023-07-01')[0]
code_ref = code[['open', 'close', 'high', 'low']].values
min_dist = dtw.find_pool(code_ref, pool='TEST_POOL')

print(min_dist)
