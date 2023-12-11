from sqlite3 import connect
from time import perf_counter
from settings import cur_db_file, tasks, ans, attempts

def replace_queries(direction):
    if direction == 'forward':
        tasks[2] = tasks[2].replace('extract(year from "tpep_pickup_datetime")', "strftime('%Y', tpep_pickup_datetime)")
        tasks[3] = tasks[3].replace('extract(year from "tpep_pickup_datetime")', "strftime('%Y', tpep_pickup_datetime)")
    elif direction == 'back':
        tasks[2] = tasks[2].replace("strftime('%Y', tpep_pickup_datetime)", 'extract(year from "tpep_pickup_datetime")')
        tasks[3] = tasks[3].replace("strftime('%Y', tpep_pickup_datetime)", 'extract(year from "tpep_pickup_datetime")')

def sqlite3_get_time():
    replace_queries('forward')
    conn = connect(cur_db_file)
    cursor = conn.cursor()
    for query_ind in range(4):
        for attempt in range(attempts):  
            start_time = perf_counter()
            cursor.execute(tasks[query_ind])
            end_time = perf_counter()
            ans[query_ind] += end_time - start_time
        ans[query_ind] = float('{:.3f}'.format((ans[query_ind]) / attempts))
    cursor.close()
    conn.close()
    replace_queries('back')
    return ans