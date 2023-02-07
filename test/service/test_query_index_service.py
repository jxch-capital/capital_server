import service.query_index_service as query_index_service
import utils.date_utils as date_utils

res = query_index_service.query_index_json("ak",
                                           start=int(
                                               date_utils.str_to_date('2022-05-01', '%Y-%m-%d').timestamp()),
                                           end=int(date_utils.str_to_date('2022-08-01', '%Y-%m-%d').timestamp()),
                                           index_name="macro_china_xfzxx", old_date_column_name="月份",
                                           date_pattern='%Y年%m月份')

print(res)
