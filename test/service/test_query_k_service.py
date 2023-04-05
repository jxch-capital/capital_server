import service.query_k_service as query_k_service
import utils.date_utils as date_utils

res = query_k_service.query_k_json('pdr-stooq', ['GOOGL.US'],
                                   '2020-01-01', date_utils.now_date_str('%Y-%m-%d'))

print(res)
