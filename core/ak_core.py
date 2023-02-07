import akshare as ak
import pandas as pd
from functools import lru_cache
from utils.cache_utils import daily_cache_manager
import json
import utils.json_util as json_util
from datetime import datetime
import utils.date_utils as date_utils

def_date_col_name = 'date'


@daily_cache_manager
@lru_cache(maxsize=10000, typed=True)
def ak_base_index(index_name):
    return getattr(ak, index_name)()


def base_index(index_name, old_date_column_name=None, date_pattern=None, new_columns=None,
               new_date_column_name=def_date_col_name, start=None, end=datetime.now().timestamp()):
    df = ak_base_index(index_name)
    if new_columns:
        df.columns = new_columns

    if date_pattern and old_date_column_name:
        new_date_column_name = def_date_col_name if new_date_column_name is None else new_date_column_name
        df[new_date_column_name] = pd.to_datetime(df[old_date_column_name], format=date_pattern)
        if start:
            df = df[df[new_date_column_name].dt.date >= date_utils.timestamp_to_date(start)]
            df = df[df[new_date_column_name].dt.date <= date_utils.timestamp_to_date(end)]

    return df


def base_index_json(index_name, old_date_column_name=None, date_pattern=None, new_columns=None,
                    new_date_column_name=def_date_col_name, start=None, end=datetime.now().timestamp()):
    df = base_index(index_name, old_date_column_name, date_pattern, new_columns, new_date_column_name, start, end)
    df_json = json.dumps(df.to_dict('records'), ensure_ascii=False, default=json_util.json_dumps_timestamp_date)
    return '{\"' + index_name + "\":" + df_json + '}'
