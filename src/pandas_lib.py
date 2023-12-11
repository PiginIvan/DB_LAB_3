from sqlalchemy import create_engine
from pandas import read_sql
from time import perf_counter
from settings import db_postgres, tasks, ans, attempts

def pandas_get_time():
    engine = create_engine(db_postgres)
    for query_ind in range(4):
        for attempt in range(attempts):  
            start_time = perf_counter()
            read_sql(tasks[query_ind],con=engine)
            end_time = perf_counter()
            ans[query_ind] += end_time - start_time
        ans[query_ind] = float('{:.3f}'.format((ans[query_ind]) / attempts))
    engine.dispose()
    return ans