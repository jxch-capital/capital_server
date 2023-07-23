from config import config
import pandas as pd

table_name = 'stock_pool'


def find_all():
    return pd.read_sql(f'select * from {config.db_schema}.{table_name}', con=config.get_pd2db_engine())


def find_by_name(name):
    return pd.read_sql(f"select * from {config.db_schema}.{table_name} where name=\'{name}\'",
                       con=config.get_pd2db_engine())


def get_all_stock_pool_json():
    return find_all().set_index('name').to_json(orient='index')


def get_stock_pool(name):
    return find_by_name(name).iloc[0]


def get_stock_pool_codes_str(name):
    return ','.join(get_stock_pool(name)['codes'])
