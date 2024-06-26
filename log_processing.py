import os
import re
from datetime import datetime
from utils import create_date_pattern, parse_time

LOG_FILE_PATH = r"D:\BaiduNetdiskWorkspace\code\python-flask-logging\demo\application.properties"
LOGS_PER_PAGE = 50

def log_file_exists():
    return os.path.exists(LOG_FILE_PATH)

def get_log_lines(keyword, date, ip, start_time_str, end_time_str):
    matched_lines = []
    pattern_keyword = re.compile(re.escape(keyword), re.IGNORECASE)
    pattern_date = create_date_pattern(date)
    pattern_ip = re.compile(re.escape(ip))
    start_time = parse_time(start_time_str)
    end_time = parse_time(end_time_str)

    with open(LOG_FILE_PATH, 'r', encoding='utf-8', errors='ignore') as log_file:
        for line in log_file:
            if pattern_keyword.search(line) and pattern_date.search(line) and pattern_ip.search(line):
                if start_time and end_time:
                    log_time_str = line.split(' ')[1]
                    log_time = datetime.strptime(log_time_str, '%H:%M:%S')
                    if start_time <= log_time <= end_time:
                        matched_lines.append(line.strip())
                else:
                    matched_lines.append(line.strip())
    return matched_lines

# def paginate_logs(matched_lines, page):
#     start = (page - 1) * LOGS_PER_PAGE
#     end = start + LOGS_PER_PAGE
#     paginated_lines = matched_lines[start:end]
#     total_pages = (len(matched_lines) + LOGS_PER_PAGE - 1) // LOGS_PER_PAGE
#     return paginated_lines, total_pages

def paginate_logs_by_size(log_lines, page_number, page_size=20):
    """
    分页处理日志内容。

    Args:
        log_lines (list): 包含所有日志行的列表。
        page_number (int): 当前页面数。
        page_size (int): 每页显示的行数，默认为20。

    Returns:
        tuple: 包含当前页面的日志行列表和总页面数。
    """
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    paginated_lines = log_lines[start_index:end_index]
    total_pages = (len(log_lines) + page_size - 1) // page_size  # 向上取整获取总页数

    return paginated_lines, total_pages

def save_logs_to_file(log_content):
    with open(LOG_FILE_PATH, 'w', encoding='utf-8', errors='ignore') as log_file:
        log_file.write(log_content.rstrip('\n'))


