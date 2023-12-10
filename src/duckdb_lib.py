from duckdb import connect
from time import perf_counter
from settings import cur_db_file, tasks, ans, attempts

def duckdb_get_time():
    conn = connect(cur_db_file)
    for query_ind in range(4):
        for attempt in range(attempts):  
            start_time = perf_counter()
            conn.execute(tasks[query_ind])
            end_time = perf_counter()
        ans[query_ind] = float('{:.3f}'.format((end_time - start_time) / attempts))
    conn.close()
    return ans