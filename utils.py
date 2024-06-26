# utils.py

import re
from datetime import datetime

def create_date_pattern(date_str):
    if len(date_str) == 4:  # YYYY
        return re.compile(rf"\b{re.escape(date_str)}\b")
    elif len(date_str) == 7:  # YYYY-MM
        return re.compile(rf"\b{re.escape(date_str)}-\d{{2}}\b")
    elif len(date_str) == 10:  # YYYY-MM-DD
        return re.compile(rf"\b{re.escape(date_str)}\b")
    return re.compile(r"")

def parse_time(time_str):
    if not time_str:
        return None
    try:
        # If time_str contains ':', assume it's in HH:MM format
        if ':' in time_str:
            return datetime.strptime(time_str, '%H:%M')
        # If time_str contains '.', assume it's in HH.MM format
        elif '.' in time_str:
            return datetime.strptime(time_str, '%H.%M')
        else:
            return None
    except ValueError:
        return None
