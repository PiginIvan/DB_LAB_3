from psycopg2 import connect, Error
from time import perf_counter
from settings import db, tasks, ans, attempts

def psycopg2_get_time():
    try:
        conn = connect(**db)
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
        return ans
    except Error as e:
        print("Wrong db", e)