# from flask import Blueprint, render_template, request
# from ..log_processing import log_file_exists, get_log_lines, paginate_logs_by_size, log_query_to_db
from flask import Blueprint, render_template, redirect, url_for, request, flash
# from log_processing import log_file_exists, get_log_lines, paginate_logs_by_size, log_query_to_db  # 使用绝对导入
import logging
from models import db, Asset, AssetForm  # 使用绝对导入


bp = Blueprint('search_routes', __name__)
logger = logging.getLogger(__name__)

@bp.route('/', methods=['GET'])
def search_logs():
    keyword = request.args.get('keyword', '')
    date = request.args.get('date', '')
    ip = request.args.get('ip', '')
    start_time_str = request.args.get('start_time', '')
    end_time_str = request.args.get('end_time', '')
    page = int(request.args.get('page', 1))

    if not log_file_exists():
        return render_template('search_logs.html', error="Log file not found")

    matched_lines = get_log_lines(keyword, date, ip, start_time_str, end_time_str)
    paginated_lines, total_pages = paginate_logs_by_size(matched_lines, page)

    log_query_to_db(keyword, date, ip, start_time_str, end_time_str)

    logger.info(f'Search logs with keyword={keyword}, date={date}, ip={ip}, start_time={start_time_str}, end_time={end_time_str}, page={page}')

    return render_template('search_logs.html',
                           matched_lines=paginated_lines,
                           total_pages=total_pages,
                           current_page=page)
