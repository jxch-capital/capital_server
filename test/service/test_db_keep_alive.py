import cx_Oracle
import sys
import os

try:
    lib_dir = r"C:\Programs\instantclient_19_19"
    cx_Oracle.init_oracle_client(lib_dir=lib_dir)
except Exception as err:
    print("Whoops!")
    print(err)
    sys.exit(1)