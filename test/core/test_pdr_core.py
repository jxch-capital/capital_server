import core.pdr_core as pdr_core
import utils.date_utils as date_utils

res = pdr_core.data_reader_codes_json(['10USY.B'], date_utils.str_to_date("2020-01-01", "%Y-%m-%d"))

print(res)
