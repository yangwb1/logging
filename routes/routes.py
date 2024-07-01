# # routes.py
#
# from flask import Blueprint, request, jsonify, render_template
# import os
# import re
# from datetime import datetime
# from models import db, QueryLog
# from database import log_query_to_db  # 导入 log_query_to_db 函数
# from utils import create_date_pattern, parse_time
#
# import os
#
# # Get the directory path of the current script (app.py)
# current_dir = os.path.dirname(os.path.abspath(__file__))
#
# # Define the path to application.properties relative to the root directory
# LOG_FILE_PATH = r"D:\BaiduNetdiskWorkspace\code\python-flask-logging\demo\spring.log"
#
# LOGS_PER_PAGE = 50  # 每页显示的日志行数
#
# bp = Blueprint('routes', __name__)
#
# @bp.route('/search_logs', methods=['GET'])
# def search_logs():
#     keyword = request.args.get('keyword', '')
#     date = request.args.get('date', '')
#     ip = request.args.get('ip', '')
#     start_time_str = request.args.get('start_time', '')
#     end_time_str = request.args.get('end_time', '')
#     page = int(request.args.get('page', 1))
#
#     if not os.path.exists(LOG_FILE_PATH):
#         return jsonify({"error": f"Log file not found at {LOG_FILE_PATH}"}), 404
#
#     matched_lines = []
#     pattern_keyword = re.compile(re.escape(keyword), re.IGNORECASE)
#     pattern_date = create_date_pattern(date)
#     pattern_ip = re.compile(re.escape(ip))
#     start_time = parse_time(start_time_str)
#     end_time = parse_time(end_time_str)
#
#     with open(LOG_FILE_PATH, 'r', encoding='utf-8', errors='ignore') as log_file:
#         for line in log_file:
#             if pattern_keyword.search(line) and pattern_date.search(line) and pattern_ip.search(line):
#                 if start_time and end_time:
#                     log_time_str = line.split(' ')[1]
#                     log_time = datetime.strptime(log_time_str, '%H:%M:%S')
#                     if start_time <= log_time <= end_time:
#                         matched_lines.append(line.strip())
#                 else:
#                     matched_lines.append(line.strip())
#
#     start = (page - 1) * LOGS_PER_PAGE
#     end = start + LOGS_PER_PAGE
#     paginated_lines = matched_lines[start:end]
#
#     # 调用 log_query_to_db 函数记录查询日志到数据库
#     log_query_to_db(keyword, date, ip, start_time_str, end_time_str)
#
#     return jsonify({
#         "matched_lines": paginated_lines,
#         "total_pages": (len(matched_lines) + LOGS_PER_PAGE - 1) // LOGS_PER_PAGE,
#         "current_page": page
#     }), 200
#
# @bp.route('/view_logs', methods=['GET'])
# def view_logs():
#     page = int(request.args.get('page', 1))
#     keyword = request.args.get('keyword', '')
#     date = request.args.get('date', '')
#     ip = request.args.get('ip', '')
#     start_time = request.args.get('start_time', '')
#     end_time = request.args.get('end_time', '')
#
#     if not os.path.exists(LOG_FILE_PATH):
#         return "Log file not found", 404
#
#     log_lines = []
#     pattern_keyword = re.compile(re.escape(keyword), re.IGNORECASE)
#     pattern_date = create_date_pattern(date)
#     pattern_ip = re.compile(re.escape(ip))
#     start_time = parse_time(start_time)
#     end_time = parse_time(end_time)
#
#     with open(LOG_FILE_PATH, 'r', encoding='utf-8', errors='ignore') as log_file:
#         for line in log_file:
#             if pattern_keyword.search(line) and pattern_date.search(line) and pattern_ip.search(line):
#                 if start_time and end_time:
#                     log_time_str = line.split(' ')[1]
#                     log_time = datetime.strptime(log_time_str, '%H:%M:%S')
#                     if start_time <= log_time <= end_time:
#                         log_lines.append(line.strip())
#                 else:
#                     log_lines.append(line.strip())
#
#     start = (page - 1) * LOGS_PER_PAGE
#     end = start + LOGS_PER_PAGE
#     paginated_lines = log_lines[start:end]
#
#     # 调用 log_query_to_db 函数记录查询日志到数据库
#     log_query_to_db(keyword, date, ip, start_time, end_time)
#
#     return render_template('view_logs.html',
#                            log_content='\n'.join(paginated_lines),
#                            current_page=page,
#                            total_pages=(len(log_lines) + LOGS_PER_PAGE - 1) // LOGS_PER_PAGE,
#                            keyword=keyword,
#                            date=date,
#                            start_time=start_time,
#                            end_time=end_time,
#                            ip=ip)
