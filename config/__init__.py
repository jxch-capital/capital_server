import psycopg2
from sqlalchemy import create_engine
from concurrent.futures import ThreadPoolExecutor
import logging
import multiprocessing


class Config(object):
    encoding = 'utf8'
    db_engine = None
    db_connection = None
    db_host = None
    db_port = None
    db_database = 'capital'
    db_schema = 'public'
    db_user = 'capital'
    db_password = 'capital'
    thread_pool_size = multiprocessing.cpu_count()
    db_conn = None
    pd2db_engine = None
    thread_pool = None

    def get_db_conn(self):
        self.db_conn = self.db_conn or self.creat_db_conn()
        return self.db_conn

    def creat_db_conn(self):
        raise BaseException('请创建数据库链接')

    def close_db_conn(self):
        self.db_conn.close()

    def get_pd2db_engine(self):
        self.pd2db_engine = self.pd2db_engine or self.create_pd2db_engine()
        return self.pd2db_engine

    def close_pd2db_engine(self):
        self.pd2db_engine.dispose()

    def create_pd2db_engine(self):
        return create_engine(
            f'{self.db_engine}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_database}')

    def get_thread_pool(self):
        self.thread_pool = self.thread_pool or self.create_thread_pool()
        return self.thread_pool

    def create_thread_pool(self):
        return ThreadPoolExecutor(max_workers=self.thread_pool_size)

    def close_thread_pool(self):
        self.thread_pool.shutdown()

    def close(self):
        self.close_db_conn() if self.db_conn else None
        self.close_pd2db_engine() if self.pd2db_engine else None
        self.close_thread_pool() if self.thread_pool else None
        logging.info(f'已关闭数据连接和线程池')


class DefaultConfigWinLocal(Config):
    db_engine = 'postgresql+psycopg2'
    db_host = 'jiangxicheng.site'
    db_port = '15432'

    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    def creat_db_conn(self):
        return psycopg2.connect(database=self.db_database, user=self.db_user, password=self.db_password,
                                host=self.db_host, port=self.db_port)


config = DefaultConfigWinLocal()
