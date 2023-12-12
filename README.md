# DB_LAB_3(Benchmark) 

Лабораторная работа заключалась в написании бенчмарка для сравнения 5 различных библиотек языка `python` с использованием 4 различных SQL запросов.

## Информация необходимая для запуска

### 1) Установка библиотек
Для работы с проектом в консоли необходимо прописать команды для установки библиотек.
```
pip install psycopg2
```
```
pip install duckdb
```
```
pip install pandas
```
```
pip install sqlalchemy
```

### 2) Клонирование репозитория
Откройте нужную папку и скопируйте репозиторий, исполнив в консоли данную команду.
```
git clone https://github.com/PiginIvan/DB_LAB_3.git
```
### 3) Создание папки и загрузка данных
Создайте папку `data` и загрузите в нее файл формата `.csv`.

### 4) Настройка программы(config)
В файле `settings.py` есть **ИНФОРМАЦИЯ ДЛЯ ЗАПУСКА**:

в словаре `libraries` значение по ключу(названию библиотеки) соответствует `True`, если необходимо получить время для данной библиотеки, `False` - в обратном случае

`cur_db_file` - файл формата '.db', на выбор 'mydb_tiny.db' или 'mydb_big.db'(если его нет, создается автоматически)

`cur_db_name` - название таблицы в базе данных, на выбор 'taxi_tiny' или 'taxi_big'

`cur_db_data` - файл формата '.csv', на выбор 'tiny' или 'big'

`attempts` - количество попыток для запуска каждого запроса

### 5) Запуск программы
Для того, чтобы запустить бенчмарк, нужно запустить файл `main.py` через IDE или прописать в консоли данную команду. Результаты запусков отобразятся в консоли.

```
python main.py
```

## Benchmark

### **Что позволяет определить бенчмарк:**

● **Оценка производительности**: Бенчмарк помогает 
оценить скорость работы системы, программного 
обеспечения или компонентов.

● **Сравнение систем**: Позволяет сравнивать 
производительность разных систем или компонентов 
в одинаковых условиях.

● **Измерение улучшений**: Позволяет оценить 
эффективность изменений, таких как обновления 
программного или аппаратного обеспечения.

● **Стандартизированные тесты**: Предоставляет набор 
стандартизированных тестов для объективного 
сравнения производительности.

● **Определение базовой производительности**: Служит 
отправной точкой для понимания 
производительности системы и ее способности 
справляться с задачами.

● **Принятие решений**: Помогает принимать 
обоснованные решения на основе количественных 
данных о производительности.

## 4 queries

### 1 query

```SQL
SELECT "VendorID", COUNT(*) FROM "trips" GROUP BY 1;
```

Этот запрос выполняет подсчёт кол-ва записей в таблице `trips` для каждого уникального значения столбца `VendorID` и группирует результаты по типу такси `VendorID`.

### 2 query

```SQL
SELECT "passenger_count", AVG("total_amount") FROM "trips" GROUP BY 1;
```

Этот запрос выполняет вычисление среднего значения стоимости поездки `total_amount` для каждого уникального значения числа пассажиров `passenger_count` в таблице `trips`.

### 3 query

```SQL
SELECT "passenger_count", EXTRACT(year FROM "tpep_pickup_datetime"), COUNT(*)
FROM "trips" GROUP BY 1, 2;
```

Этот запрос извлекает информацию из таблицы trips о кол-ве пассажиров `passenger_count`, годе по времени взятия такси `tpep_pickup_datetime`, и подсчитывает кол-во записей, соответствующих каждому уникальному значению комбинации числа пассажиров и года взятия такси.

### 4 query

```SQL
SELECT "passenger_count", EXTRACT(year FROM "tpep_pickup_datetime"), ROUND("trip_distance"),
COUNT(*) FROM "trips" GROUP BY 1, 2, 3 ORDER BY 2, 4 DESC;
```

Этот запрос извлекает информацию из таблицы trips о кол-ве пассажирор `passenger_count`, годе по времени взятия такси `tpep_pickup_datetime`, округлённой дистанции поездки `trip_distance` и подсчитывает кол-во записей для каждой уникальной комбинации этих параметров. Результаты сортируются по году взятия такси в порядке возрастания, а кол-во записей в каждой группе упорядочивается по убыванию.

## Загрузка данных и создание БД

Некоторые библиотеки предоставляют возможность создания базы данных, однако я использовал `sqlite3 / pandas` для создания .db файла и `sqlalchemy / pandas` для загрузки данных в постгрес один раз перед запуском запросов. В каждой библиотеке обращался к уже созданному файлу .db или постгресу.

### Создание .db файла
```py
from sqlite3 import connect
from pandas import read_csv, to_datetime
conn = connect(cur_db_file) #cur_db_file = 'data\\mydb_big.db' или 'data\\mydb_tiny.db'
df = read_csv(cur_db_data)
df.drop("Airport_fee", axis=1, inplace= True)
df["tpep_pickup_datetime"] = to_datetime(df["tpep_pickup_datetime"])
df.to_sql(cur_db_name, conn, if_exists='replace', index=False, chunksize=1000)
```

Данный файл использовался для `sqlite3` и `duckdb`.

### Создание таблицы в постгрес

```py
from sqlalchemy import inspect, create_engine
from pandas import read_csv, to_datetime
engine = create_engine(db_postgres) #db_postgres = 'postgresql://postgres:postgres@localhost:5432/postgres'
df = read_csv(cur_db_data)
df.drop("Airport_fee", axis=1, inplace= True)
df["tpep_pickup_datetime"] = to_datetime(df["tpep_pickup_datetime"])
df.to_sql(cur_db_name, engine, if_exists='replace', index=False, chunksize=500)
```

Постгрес использовался для `psycopg2`, `sqlalchemy` и `pandas`.

### Рассмотренные библиотеки




## Сравнительные графики

### 1. Файл tiny

#### Результаты запусков

![](https://github.com/PiginIvan/DB_LAB_3/blob/main/resources/tiny_res.png)

#### Графики

![](https://github.com/PiginIvan/DB_LAB_3/blob/main/resources/tiny_graph.png)

### 2. Файл big

#### Результаты запусков

![](https://github.com/PiginIvan/DB_LAB_3/blob/main/resources/big_res.png)

#### Графики

![](https://github.com/PiginIvan/DB_LAB_3/blob/main/resources/big_graph.png)

