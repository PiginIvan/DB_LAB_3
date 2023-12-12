# DB_LAB_3(Benchmark) 

Лабораторная работа заключалась в написании бенчмарка для сравнения 5 различных библиотек языка `python` с использованием 4 различных SQL запросов.

## Информация необходимая для запуска

### 1. Установка библиотек
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

### 2. Клонирование репозитория
Откройте нужную папку и скопируйте репозиторий, исполнив в консоли данную команду.
```
git clone https://github.com/PiginIvan/DB_LAB_3.git
```
### 3. Создание папки и загрузка данных
Создайте папку `data` и загрузите в нее файл формата `.csv`.

### 4. Настройка программы(config)
В файле `settings.py` есть **ИНФОРМАЦИЯ ДЛЯ ЗАПУСКА**:

в словаре `libraries` значение по ключу(названию библиотеки) соответствует `True`, если необходимо получить время для данной библиотеки, `False` - в обратном случае

`cur_db_file` - файл формата '.db', на выбор 'mydb_tiny.db' или 'mydb_big.db'(если его нет, создается автоматически)

`cur_db_name` - название таблицы в базе данных, на выбор 'taxi_tiny' или 'taxi_big'

`cur_db_data` - файл формата '.csv', на выбор 'tiny' или 'big'

`attempts` - количество попыток для запуска каждого запроса

### 5. Запуск программы
Для того, чтобы запустить бенчмарк, нужно запустить файл `main.py` через IDE или прописать в консоли данную команду. Результаты запусков отобразятся в консоли.

```
python main.py
```

## Benchmark

### **Что позволяет определить бенчмарк:**

● **Оценка производительности**: Бенчмарк помогает оценить скорость работы системы программного обеспечения или компонентов.

● **Сравнение систем**: Позволяет сравнивать производительность разных систем или компонентов в одинаковых условиях.

● **Измерение улучшений**: Позволяет оценить эффективность изменений, таких как обновления программного или аппаратного обеспечения.

● **Стандартизированные тесты**: Предоставляет набор стандартизированных тестов для объективного сравнения производительности.

● **Определение базовой производительности**: Служит отправной точкой для понимания производительности системы и ее способности справляться с задачами.

● **Принятие решений**: Помогает принимать обоснованные решения на основе количественных данных о производительности.

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

Некоторые библиотеки предоставляют возможность создания базы данных, однако я использовал `sqlite3 + pandas` для создания .db файла и `sqlalchemy + pandas` для загрузки данных в постгрес один раз перед запуском запросов. В каждой библиотеке обращался к уже созданному файлу .db или постгресу.

### 1. Создание .db файла
```py
from sqlite3 import connect
from pandas import read_csv, to_datetime

conn = connect(cur_db_file) #cur_db_file = 'data\\mydb_big.db' или 'data\\mydb_tiny.db'
df = read_csv(cur_db_data)
df.drop("Airport_fee", axis=1, inplace= True)
df["tpep_pickup_datetime"] = to_datetime(df["tpep_pickup_datetime"])
df.to_sql(cur_db_name, conn, if_exists='replace', index=False, chunksize=1000)
```

Данный файл использовался для `sqlite3` и `duckdb`. Если файл уже создан, то повторное создание в программе производиться не будет.

### 1. Создание таблицы в постгрес

```py
from sqlalchemy import inspect, create_engine
from pandas import read_csv, to_datetime

engine = create_engine(db_postgres) #db_postgres = 'postgresql://postgres:postgres@localhost:5432/postgres'
df = read_csv(cur_db_data)
df.drop("Airport_fee", axis=1, inplace= True)
df["tpep_pickup_datetime"] = to_datetime(df["tpep_pickup_datetime"])
df.to_sql(cur_db_name, engine, if_exists='replace', index=False, chunksize=500)
```

Постгрес использовался для `psycopg2`, `sqlalchemy` и `pandas`. Если таблица уже имеется в постгресе, то повторное создание в программе производиться не будет.

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

## Описание и сравнение библиотек

### 1. Psycopg2

#### Описание библиотеки
**Psycopg2** — это популярная библиотека позволяет разработчикам легко и эффективно работать с PostgreSQL, используя язык программирования Python. Она предоставляет широкий спектр функций и возможностей, таких как поддержка транзакций, создание и выполнение SQL-запросов, чтение и запись данных в таблицы, а также множество других полезных функций.

**Среди плюсов этой библиотеки можно выделить:**

* Распространенность — Psycopg2 использует большинство фреймворков Python.

* Поддержка — Psycopg2 активно развивается и поддерживает основные версии Python.

* Многопоточность — Psycopg2 позволяет нескольким потокам поддерживать одно и то же соединение.

**Среди минусов этой библиотеки можно выделить:**

* Установка - для использования Psycopg2 необходимо установить саму библиотеку и дополнительные зависимости, что может вызвать некоторые сложности для начинающих разработчиков.

#### Функциональность библиотеки

Для начала нужно задать параметры подключения к постгрес через такой словарь.

```py
db = {"dbname" : "postgres", "user" : "postgres", "password" : "postgres", "host": "localhost", "port" : "5432"}
```

```py
from psycopg2 import connect, Error

try:
    conn = connect(**db) #подключение к бд
    cursor = conn.cursor() #создание курсора

    cursor.execute(tasks[query_ind]) #исполнение SQL запроса

    cursor.close() #удаление курсора
    conn.close() #закрытие подключения к бд
    
except Error as e:
    print("Wrong db", e)
```

#### Ощущения

В целом, использование Psycopg2 позволяет эффективно работать с базой данных PostgreSQL, но при этом требует определенных усилий на начальных этапах установки и обновления. Загрузка в постгрес 2гб файла занимает более часа. Присутствует возможность загрузки данных из .csv файла. Psycopg2 полностью соответствует стандарту DB-API 2.0, что делает ее совместимой с другими библиотеками для работы с базами данных в Python. Она поддерживает различные типы данных PostgreSQL, включая числа, строки, бинарные данные и даже массивы. Библиотека также предоставляет возможности обработки исключений, включая подробные сообщения об ошибках и откат транзакций в случае неудачного выполнения запроса. 

#### Оценка производительности

Если обратиться к графикам, то можно увидеть, что скорость выполнения запросов довольно низкая. Время очень близко по значения к `pandas`, быстрее `sqlalchemy`, однако сильно проигрывает `duckdb` и `sqlite3`. Скорее всего это подходит для всех библиотек, которые использовали постгрес(необходимо поднимать через докер), так как им необходимо выполнить подключение по сети, в то время как `sqlite3` и `duckdb` открывают файл и работают с ним. Также используется система “транзакций”, которая сопровождается подтверждением каждой операции при выполнении запросов, что отрицательно влияет на производительность.

### 2. SQLite3

#### Описание библиотеки

**SQLite** — это быстрая и легкая встраиваемая однофайловая СУБД на языке C, которая не имеет сервера и позволяет хранить всю базу локально на одном устройстве. Для работы SQLite не нужны сторонние библиотеки или службы.

**Среди плюсов этой библиотеки можно выделить:**

* Высокая скорость - благодаря особенностям архитектуры SQLite работает быстро, особенно на чтение. Компоненты СУБД встроены в приложение и вызываются в том же процессе. Поэтому доступ к ним быстрее, чем при взаимодействии между разными процессами.

* Хранение данных в одном файле - база данных состоит из табличных записей, связей между ними, индексов и других компонентов. В SQLite они хранятся в едином файле (database file).

* Автономность - система независима от стороннего ПО, библиотек или фреймворков.

**Среди минусов этой библиотеки можно выделить:**

* Ограниченная поддержка типов данных - SQLite поддерживает только четыре типа данных, которые реализованы в SQL: `INTEGER` — целое число; `REAL` — дробное число; `TEXT` — текст; `BLOB` — двоичные данные.

* Ограничения в применении - отсутствие сервера — преимущество и недостаток одновременно. Без сервера возможности СУБД меньше. Например, к одной базе не смогут обращаться несколько разных устройств.

* Отсутствие хранимых процедур - блоки кода на SQL, которые сохраняются в базу данных не поддерживаются SQLite из-за особенностей архитектуры.

#### Функциональность библиотеки

```py
from sqlite3 import connect

conn = connect(cur_db_file) #подключение к бд
cursor = conn.cursor() #создание курсора

cursor.execute(tasks[query_ind]) #исполнение SQL запроса

cursor.close() #удаление курсора
conn.close() #закрытие подключения к бд
```

Так как создание .db файла было приведено выше, то здесь показаны лишь возможности библиотеки по работе с готовым .db файлом.

#### Ощущения

Довольно удобная библиотека, так как создание .db файла происходит гораздо быстрее, чем загрузка данных в постгрес. Ее лучше использовать, когда есть необходимость объединить надежные возможности SQL-запросов и хранения с простотой использования обычного доступа к файловой системе. Однако не стоит применять ее с очень большими файлами. Отсутствует метод автоматической записи данных из файла. Также была необходимость изменить некоторые запросы.

```py
replace('extract(year from "tpep_pickup_datetime")', "strftime('%Y', tpep_pickup_datetime)")
```

#### Оценка производительности

Результаты запусков показывают, что `sqlite3` работает быстрее, чем большинство библиотек, однако не максимально эффективно. Занимает 2-ое место по времени после `duckdb`. Это может быть связано с особенностями архитектуры SQLite, на чтение запросов она работает достаточно быстро. Также чтение данные идет из файла, а не через сервер.

### 3. DuckDB

#### Описание библиотеки

**DuckDB** - это встроенная система управления базами данных SQL OLAP. Функции DuckDB выполняются в самом приложении, а не во внешнем процессе. DuckDB - отличный вариант, если нужна бессерверная система управления базами данных для анализа данных. 

**Среди плюсов этой библиотеки можно выделить:**

* Простота - простота установки и встроенная работа в процессе - вот что выбрали разработчики DuckDB для этой СУБД, увидев успех SQLite благодаря этим функциям. 

* Скорость - высокая скорость обработки достигается за счёт векторизации выполнения запросов (ориентации на столбцы), в то время как другие СУБД обрабатывают каждую строку последовательно.

* Завершённость - duckdb поддерживает сложные запросы в SQL и обеспечивает гарантии транзакций.

**Среди минусов этой библиотеки можно выделить:**

* Хранение записей - в duckdb используется классическое строчное хранение записей.

* Отсутствие параллельной обработки процессов - невозможность записи в одну базу данных из нескольких параллельных процессов и чтения из одной базы данных.

* Ограниченная функциональность - в отличие от некоторых других библиотек, DuckDB может не иметь некоторых функций.

#### Функциональность библиотеки

Имеет возможность работы с файлами формата .db и .duckdb. В моей реализации использовался .db файл, создание которого было приведено ранее. 

```py
from duckdb import connect

conn = connect(cur_db_file) #подключение к бд

conn.execute(tasks[query_ind]) #исполнение SQL запроса

conn.close() #закрытие подключения к бд
```

#### Ощущения

В целом работа с данной библиотека была очень похожа на работу с `sqlite3`. Достаточно удобная, имеется встроенный способ загрузки данных из .csv файла. Лучше всего подходит для интерактивного анализа данных и передовых вычислений. Данная библиотека активно развивается и в данное время. Возникла трудность, так как вылетала ошибка. Пришлось создавать и выполнять отдельный запрос, для загрузки расширения.  

```
Extension "sqlite" is an existing extension. Install it first using "INSTALL sqlite".
```

#### Оценка производительности

Данная библиотека показывает выдающиеся результаты, как на большом, так и на маленьком файле. Она не просто опережает все остальные библиотеки, но и превосходит их по времени в несколько раз. Как уже было упомянуто выше, это связано с векторизацией выполнения запросов (ориентацией на столбцы). Duckdb оптимизирован для выполнения аналитических запросов, что также улучшает его производительность.

### 4. Pandas

#### Описание библиотеки

Pandas — это библиотека Python для обработки и анализа структурированных данных. Это быстрый, мощный, гибкий и простой в использовании инструмент для анализа и обработки данных с открытым исходным кодом, созданный на языке программирования Python. На данный момент библиотека Pandas является ключевой в анализе данных (Data Mining).

**Среди плюсов этой библиотеки можно выделить:**

* Интеллектуальное индексирование, манипулирование и управление столбцами и строками.

* Гибкое изменение форм -  добавление, удаление, присоединение новых или старых данных.

* Использование DataFrame - это быстрый и эффективный инструмент для манипулирования данными со встроенной индексацией. Методы, требующие высокой производительности, написаны на C или Cython.

**Среди минусов этой библиотеки можно выделить:**

* Проблема с работой с большими данными - операции происходят в оперативной памяти, а её не всегда много, а также операции выполняются на одном треде.

* Параллельная обработка - Pandas API предоставляет 600+ функций и их оптимизация очень трудное занятие.

#### Функциональность библиотеки

```py
from pandas import read_sql

engine = create_engine(db_postgres) #подключение к бд

read_sql(tasks[query_ind],con=engine) #исполнение SQL запроса

engine.dispose() #закрытие подключения к бд
```

Также есть возможность писать запросы иначе, используя dataframe, однако для этого требуется загрузка в память. Пример первого запроса приведен ниже.

```py
selected_df = trips[['VendorID']]
grouped_df = selected_df.groupby('VendorID')
final_df = grouped_df.size().reset_index(name='counts')
```

#### Ощущения

Думаю, что это одна из самых интересных библиотек для изучения. С её помощью создавались базы данных, так как чтение .csv файла и запись в sql производились с помощью методов `pandas`. Имеет достаточно обширный функционал. Кроме того, позволяет подключаться к различным базам данным, выступая при этом дополнительным инструментом. 

#### Оценка производительности

На графиках можно увидеть, что результаты данной библиотеки очень близки к результатам `psycopg2`, так как `pandas` также подключалось к постгресу и использовался метод прямого чтения SQL запросов, а не обработка через dataframe. На больших данных может показывать более плохие результаты, из-за описанных выше минусов, однако функциональность делает ее одной из самых удобных и приятных в использовании.

### 5. SQLalchemy

#### Описание библиотеки

SQLAlchemy — это Python-библиотека, которая позволяет работать с реляционными базами данных с помощью ORM. Реляционные базы данных хранят информацию в виде связанных между собой таблиц. ORM позволяет управлять базами данных с помощью методов объектов в коде и при этом не использовать SQL-запросы.

**Среди плюсов этой библиотеки можно выделить:**

* Гибкость - ORM изолирует от особенностей конкретных СУБД, и проект может быть перенесен без изменений с PostgreSQL на MySQL.

* Обработка сложных запросов - достаточно хорошо обрабатывает сложные по структуре запросы.

* Безопасность - параметры запросов экранируются, что делает атаки типа внедрение SQL-кода маловероятными.

**Среди минусов этой библиотеки можно выделить:**

* Скорость - из-за ORM данная библиотека достаточно медленная.

* Ситуативность - ORM нет смысла использовать в 95% случаев. SQLAlchemy — это не только ORM, но еще и построитель запросов. А поскольку часто таблицы простые и несвязанные, то и построителя запросов тоже не требуется.

#### Функциональность библиотеки

```py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

engine = create_engine(db_postgres)  #подключение к бд
session = sessionmaker(bind=engine)() #создание сессии
    
session.execute(text(tasks[query_ind])) #исполнение SQL запроса
            
session.close() #удаление сессии
engine.dispose() #закрытие подключения к бд
```

В моем проекте не использовались ORM возможности данной библиотеки, а запросы обрабатывались напрямую.

#### Ощущения

Невозможно объективно оценить данную библиотеку, так как я не использовал все возможности, которые были предоставлены библиотекой. Однако для простых заданий в этом нет необходимости, поэтому я считаю, что библиотека имеет место быть, но для этого нужны некоторые условия. Также сначала нужно разобраться в ORM системе, чтобы полностью понимать, как работает библиотека.

#### Оценка производительности

По графикам можно заметить, что `sqlalchemy` показала самый слабый результат среди всех рассмотренных библиотек. Предоставляет возможность подключения как к .db файлу, так и к постгресу, я выбрал постгрес, что тоже в значительной степени повлияло на результаты. Главным фактором является ORM, что замедляет выполнение всех запросов. 

## Выводы

В результате данной лабораторной работы был написан бенчмарк для 5 различных библиотек языка `python`. Сравнение результатов времени исполнения запросов показывает, что скорости библиотек сильно разняться. Максимально быстрой и эффективной является `duckdb`, однако она имеет не все возможные функции и её стоит использовать, если необходимо реализовать простые задачи как можно быстрее. Библиотека `sqlalchemy` самая медленная по времени, однако единственная использует технологии ORM(что не является обязательным, но дает такую возможность). ORM изолирует от особенностей СУБД, что может быть важным фактором, если используются различные СУБД, а скоростей не главная цель. Если нужно работать только с `PostgreSQL`, то есть смысл выбрать `psycopg2`. Она достаточно распространенная, обладает многопоточностью, но загрузка данных может занять определенное время. Если предоставляется доступ к базе данных `SQLite`, то стоит обратить внимание на `sqlite3`. Данные хранятся в одном файле и доступ происходит с достаточно быстрой скоростью, однако отсутствие сервера может быть серьезной проблемой при работе.  Оставшаяся библиотека `pandas` дает возможность работать с данными с помощью dataframe. Показывает среднее время, имеет большое количество различных функций и может подключаться к различным базам данных. Можно сделать вывод, что каждая из библиотек имеет как свои плюсы, так и минусы. К каждому проекту нужно подходить по-разному и в зависимости от условий и факторов выбирать, какая библиотека будет максимально удобной в конкретной ситуации!
