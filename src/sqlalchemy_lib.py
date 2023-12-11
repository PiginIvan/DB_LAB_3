from sqlalchemy import create_engine, text
from time import perf_counter
from settings import db_postgres, tasks, ans, attempts

def sqlalchemy_get_time():
    engine = create_engine(db_postgres)
    conn = engine.connect()
    for query_ind in range(4):
        for attempt in range(attempts):  
            start_time = perf_counter()
            conn.execute(text(tasks[query_ind]))
            end_time = perf_counter()
            ans[query_ind] += end_time - start_time
        ans[query_ind] = float('{:.3f}'.format((ans[query_ind]) / attempts))
    conn.close()
    engine.dispose()
    return ans