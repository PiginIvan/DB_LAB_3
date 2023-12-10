#базы данных
db_file_tiny = 'data\\mydb_tiny.db'
db_file_big = 'data\\mydb_big.db'

#путь для постгрес
db_postgres = 'postgresql://postgres:postgres@localhost:5432/postgres'
db = {"dbname" : "postgres", "user" : "postgres", "password" : "postgres", "host": "localhost", "port" : "5432"}

#названия таблиц в БД
db_name_tiny = 'taxi_tiny'
db_name_big = 'taxi_big'

#csv файлы с данными 
tiny = 'data\\nyc_yellow_tiny.csv'
big = 'data\\nyc_yellow_big.csv'

#массив для замеров времени
ans = [0, 0, 0, 0]

#ИНФОРМАЦИЯ ДЛЯ ЗАПУСКА(True - чтобы получить время для данной библиотеки, False - не получать)
#cur_db_file - файл формата '.db', на выбор 'mydb_tiny.db' или 'mydb_big.db'
#cur_db_name - название таблицы в базе данных, на выбор 'taxi_tiny' или 'taxi_big'
#cur_db_data - файл формата '.csv', на выбор 'tiny' или 'big'
#attempts - количество попыток для запуска каждого запроса
libraries = {'psycopg2' : True, 'sqlalchemy' : True, 'sqlite3' : True, 'duckdb' : True, 'pandas' : True}
cur_db_file = db_file_tiny
cur_db_name = db_name_tiny
cur_db_data = tiny
attempts = 1

#запросы
query1 = f"""SELECT "VendorID", count(*) FROM "{cur_db_name}" GROUP BY 1;"""
query2 = f"""SELECT "passenger_count", avg("total_amount") FROM "{cur_db_name}" GROUP BY 1;"""
query3 = f"""SELECT "passenger_count", extract(year from "tpep_pickup_datetime"), count(*) FROM "{cur_db_name}" GROUP BY 1, 2;"""
query4 = f"""SELECT "passenger_count", extract(year from "tpep_pickup_datetime"), round("trip_distance"), count(*) FROM "{cur_db_name}" GROUP BY 1, 2, 3 ORDER BY 2, 4 desc;"""
tasks = [query1, query2, query3, query4]