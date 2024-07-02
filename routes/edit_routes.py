from flask import Blueprint, render_template, request, redirect, url_for, flash
# from ..log_processing import log_file_exists, get_log_lines, paginate_logs_by_size, save_logs_to_file, LOG_FILE_PATH
# from forms import EditLogsForm
import os
import logging
from models import db, Asset, AssetForm  # 使用绝对导入


bp = Blueprint('edit_routes', __name__)
logger = logging.getLogger(__name__)

@bp.route('/logs', methods=['GET'])
def view_logs():
    keyword = request.args.get('keyword', '')
    date = request.args.get('date', '')
    ip = request.args.get('ip', '')
    start_time = request.args.get('start_time', '')
    end_time = request.args.get('end_time', '')
    page = int(request.args.get('page', 1))

    if not log_file_exists():
        return "Log file not found", 404

    matched_lines = get_log_lines(keyword, date, ip, start_time, end_time)
    paginated_lines, total_pages = paginate_logs_by_size(matched_lines, page)

    cleaned_lines = [line.strip() for line in paginated_lines]

    return render_template('view_logs.html',
                           log_content=cleaned_lines,
                           current_page=page,
                           total_pages=total_pages,
                           keyword=keyword,
                           date=date,
                           start_time=start_time,
                           end_time=end_time,
                           ip=ip)

@bp.route('/edit', methods=['GET', 'POST'])
def edit_logs():
    form = EditLogsForm()

    if request.method == 'GET':
        if not log_file_exists():
            return "日志文件未找到", 404

        with open(LOG_FILE_PATH, 'r', encoding='utf-8', errors='ignore') as log_file:
            log_content = log_file.read()

        form.log_content.data = log_content

        page = int(request.args.get('page', 1))
        log_lines = log_content.splitlines()

        paginated_lines, total_pages = paginate_logs_by_size(log_lines, page)

        return render_template('edit_logs.html', form=form, log_lines=paginated_lines, current_page=page,
                               total_pages=total_pages)

    elif request.method == 'POST' and form.validate_on_submit():
        new_content = form.log_content.data

        try:
            save_logs_to_file(new_content)
            flash('日志已成功保存', 'success')
        except Exception as e:
            flash(f'保存日志出错: {str(e)}', 'error')

        return redirect(url_for('edit_routes.edit_logs'))

    return render_template('edit_logs.html', form=form)

@bp.route('/save', methods=['POST'])
def save_logs():
    new_content = request.form.get('log_content')

    if not log_file_exists():
        return "Log file not found", 404

    new_content = new_content.strip()
    new_content = new_content.replace('\r\n', os.linesep).replace('\n', os.linesep)

    try:
        with open(LOG_FILE_PATH, 'w', encoding='utf-8') as log_file:
            log_file.write(new_content)
    except Exception as e:
        print(f"Error saving logs: {e}")
        return "Error saving logs", 500

    logger.info('Logs edited and saved')

    return redirect(url_for('edit_routes.view_logs'))
