from sqlalchemy import create_engine, text
from time import perf_counter
from settings import db_postgres, tasks, ans, attempts
from sqlalchemy.orm import sessionmaker

def sqlalchemy_get_time():
    engine = create_engine(db_postgres)
    session = sessionmaker(bind=engine)()
    for query_ind in range(4):
        for attempt in range(attempts):  
            start_time = perf_counter()
            session.execute(text(tasks[query_ind]))
            end_time = perf_counter()
            ans[query_ind] += end_time - start_time
        ans[query_ind] = float('{:.3f}'.format((ans[query_ind]) / attempts))
    session.close()
    engine.dispose()
    return ans