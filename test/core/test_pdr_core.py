import core.pdr_core as pdr_core
import datetime
import logging
import pandas_datareader.data as web

logging.basicConfig(level=logging.INFO)

df = pdr_core.data_reader_codes_json(["^CAC"], datetime.datetime(2022, 1, 1))




# df = web.DataReader("^DAX", "stooq", datetime.datetime(2022, 1, 1), datetime.datetime.now())
print(df)