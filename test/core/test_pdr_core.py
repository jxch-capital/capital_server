import core.pdr_core as pdr_core
import datetime
import logging

logging.basicConfig(level=logging.INFO)

df = pdr_core.data_reader_codes_json(["PG"], datetime.datetime(2022, 1, 1))

print(df)