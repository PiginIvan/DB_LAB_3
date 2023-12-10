from sqlite3 import connect
from sqlalchemy import inspect, create_engine
from pandas import read_csv, to_datetime
from settings import libraries, cur_db_file, cur_db_data, cur_db_name, db_postgres
from os import path
from psycopg2_lib import psycopg2_get_time
from sqlalchemy_lib import sqlalchemy_get_time
from sqlite3_lib import sqlite3_get_time
from duckdb_lib import duckdb_get_time
from pandas_lib import pandas_get_time

if not path.exists(cur_db_file):
    conn = connect(cur_db_file)
    df = read_csv(cur_db_data)
    df["tpep_pickup_datetime"] = to_datetime(df["tpep_pickup_datetime"])
    df.to_sql(cur_db_name, conn, if_exists='replace', index=False, chunksize=1000)
engine = create_engine(db_postgres)
inspector = inspect(engine)
if not cur_db_name in inspector.get_table_names():
    df = read_csv(cur_db_data)
    df["tpep_pickup_datetime"] = to_datetime(df["tpep_pickup_datetime"])
    df.to_sql(cur_db_name, engine, if_exists='replace', index=False, chunksize=500)

print("Library_name Query_1 Query_2 Query_3 Query_4")
for library in libraries:
    if libraries[library] == True:
        request = library + '_get_time'
        print(library + ': ', end='')
        print(*eval(request)())