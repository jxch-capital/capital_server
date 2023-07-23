import service.stock_pool_service as sps
import core.yahoo_core as yh
import core.number_regular as reg
from concurrent.futures import ThreadPoolExecutor, as_completed


def process_df(df, col, k_arr, th):
    arr = df[col].values
    res = reg.find_similar_sequences(arr, k_arr, th)
    dist = [{
        'code': df['code'][0],
        'dist': item['dist'],
        'start': df.iloc[item['index']]['date'],
        'end': df.iloc[item['index'] + len(k_arr)]['date'],
        'len': len(k_arr),
        'k': item['k'],
    } for item in res]
    print(f"code: {df['code'][0]}")
    return dist


def find_pool(k_arr, pool='ALL', start_str='2000-01-01', end_str=None, th=0.1):
    return find(k_arr, sps.get_stock_pool_codes_str(pool), start_str, end_str, th=th)


def find(k_arr, code_str=None, start_str='2000-01-01', end_str=None, col=None, th=0.1):
    if code_str is None:
        code_str = ["SPY", "XLI", "XLE", "XLY", "XLP", "XLF", "XLV", "XLC", "XLB", "XLRE", "XLK", "XLU"]
    if col is None:
        col = ['open', 'close', 'high', 'low']
    df_arr = yh.download_codes_batch_by_codes_str(codes_str=code_str, start_str=start_str, end_str=end_str)

    dists = []
    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(process_df, df, col, k_arr, th) for df in df_arr]
        for future in as_completed(futures):
            dists.extend(future.result())

    dists.sort(key=lambda p: p['dist'])
    return dists
