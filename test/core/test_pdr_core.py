import core.pdr_core as pdr_core
import datetime

df = pdr_core.data_reader_codes_json(["PG"], datetime.datetime(2020, 1, 1))

print(df)