# database.py

from models import db, QueryLog
from datetime import datetime

def log_query_to_db(keyword, date, ip, start_time, end_time):
    query_log = QueryLog(keyword=keyword, date=date, ip=ip, start_time=start_time, end_time=end_time)
    db.session.add(query_log)
    db.session.commit()
