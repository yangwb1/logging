# import logging
# from flask_ckeditor import CKEditorField
# from . import bp
# from database_operations import log_query_to_db
# from log_processing import log_file_exists, get_log_lines, paginate_logs_by_size, save_logs_to_file, LOG_FILE_PATH
# from flask import Blueprint, render_template, redirect, url_for, request, flash,request, render_template, redirect, url_for, flash, Blueprint
# # from forms import AssetFormf
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField


# import os


# from flask import Blueprint, render_template, redirect, url_for, request, flash
# from elasticsearch import Elasticsearch, exceptions as es_exceptions
# from datetime import datetime, timedelta
# from pygrok import Grok
# # from . import bp
# from models import db, Asset, EditLogsForm, AssetForm

# bp = Blueprint('routes', __name__)


# GROK_PATTERN = '%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:loglevel} %{GREEDYDATA:message}'


# # Elasticsearch连接配置
# es = Elasticsearch(
#     ['https://localhost:9200'],
#     http_auth=('elastic', 'wsayCf-c644HMSqDZUR7'), # 替换为你的用户名和密码
#     # scheme="https",
#     # port=9200,
#     verify_certs=True,
#     ca_certs="D:\\Program Files\\elasticsearch-8.14.1\\elastic-stack-ca.p12"
# )
# logger = logging.getLogger(__name__)



# def paginate_logs_by_size(log_lines, page, rows_per_page=20):
#     start_index = (page - 1) * rows_per_page
#     end_index = start_index + rows_per_page
#     paginated_lines = log_lines[start_index:end_index]
#     total_pages = (len(log_lines) + rows_per_page - 1) // rows_per_page
#     return paginated_lines, total_pages

# # @bp.route('/grok_logs')
# # def index():
# #     return render_template('grok_logs.html')

# @bp.route('/grok_upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return redirect(request.url)
#         file = request.files['file']
#         if file.filename == '':
#             return redirect(request.url)
#         if file:
#             logs = file.read().decode('utf-8').splitlines()
#             parsed_logs = parse_logs(logs)
#             return render_template('grok_upload.html', logs=parsed_logs)
#     return render_template('grok_upload.html')

# def parse_logs(logs):
#     grok = Grok(GROK_PATTERN)
#     parsed_logs = []
#     for line in logs:
#         match = grok.match(line)
#         if match:
#             parsed_logs.append(match)
#     return parsed_logs

# @bp.route('/logs', methods=['GET', 'POST'])
# def index():
#     page = request.args.get('page', 1, type=int)
#     logs_per_page = 15
#     logs = []
#     date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
#     try:
#         start_date = datetime.strptime(date, '%Y-%m-%d')
#         end_date = start_date + timedelta(days=1)
#         result = es.search(
#             index='winlogbeat-*',
#             body={
#                 'query': {
#                     'range': {
#                         '@timestamp': {
#                             'gte': start_date.isoformat(),
#                             'lt': end_date.isoformat()
#                         }
#                     }
#                 },
#                 'sort': {'@timestamp': {'order': 'desc'}},
#                 'size': logs_per_page,
#                 'from': (page - 1) * logs_per_page
#             }
#         )
#         hits = result['hits']['hits']
#         for hit in hits:
#             log = hit['_source']
#             log['full_content'] = hit['_source']
#             logs.append(log)
#         logs = [{'sequence': (page - 1) * logs_per_page + i + 1, 'content': hit['_source']} for i, hit in enumerate(hits)]
#         total = result['hits']['total']['value']
#         total_pages = (total + logs_per_page - 1) // logs_per_page
#         print(f"Successfully retrieved {len(logs)} logs from Elasticsearch")
#     except es_exceptions.ConnectionError as ce:
#         print(f"Error connecting to Elasticsearch: {ce}")
#         logs = []
#     except es_exceptions.AuthorizationException as ae:
#         print(f"Authorization failed: {ae}")
#         logs = []
#     except Exception as e:
#         print(f"Error retrieving logs from Elasticsearch: {e}")
#         logs = []

#     return render_template('logs.html', logs=logs, page=page, total_pages=total_pages, date=date)
# @bp.route('/assets', methods=['GET'])
# def list_assets():
#     assets = Asset.query.all()
#     return render_template('asset_list.html', assets=assets)


# @bp.route('/assets/<int:asset_id>/edit', methods=['GET', 'POST'])
# def edit_asset(asset_id):
#     asset = Asset.query.get_or_404(asset_id)
#     form = AssetForm(obj=asset)

#     if form.validate_on_submit():
#         form.populate_obj(asset)
#         db.session.commit()
#         flash('Asset updated successfully.', 'success')
#         return redirect(url_for('routes.list_assets'))

#     return render_template('asset_form.html', form=form, asset=asset)


# @bp.route('/assets/new', methods=['GET', 'POST'])
# def new_asset():
#     form = AssetForm()

#     if form.validate_on_submit():
#         asset = Asset()
#         form.populate_obj(asset)
#         db.session.add(asset)
#         db.session.commit()
#         flash('Asset created successfully.', 'success')
#         return redirect(url_for('routes.list_assets'))

#     return render_template('asset_form.html', form=form, asset=None)


# @bp.route('/assets/<int:asset_id>/logs', methods=['GET'])
# def view_asset_logs(asset_id):
#     asset = Asset.query.get_or_404(asset_id)

#     # 获取资产相关的日志，可以根据需要调整获取日志的逻辑
#     keyword = asset.ip_address
#     date = request.args.get('date', '')
#     start_time = request.args.get('start_time', '')
#     end_time = request.args.get('end_time', '')
#     page = int(request.args.get('page', 1))

#     if not log_file_exists():
#         return "Log file not found", 404

#     matched_lines = get_log_lines(keyword, date, '', start_time, end_time)
#     paginated_lines, total_pages = paginate_logs_by_size(matched_lines, page)

#     cleaned_lines = [line.strip() for line in paginated_lines]

#     return render_template('view_asset_logs.html',
#                            asset=asset,
#                            log_content=cleaned_lines,
#                            current_page=page,
#                            total_pages=total_pages,
#                            date=date,
#                            start_time=start_time,
#                            end_time=end_time)


# @bp.route('/search_logs', methods=['GET'])
# def search_logs():
#     keyword = request.args.get('keyword', '')
#     date = request.args.get('date', '')
#     ip = request.args.get('ip', '')
#     start_time_str = request.args.get('start_time', '')
#     end_time_str = request.args.get('end_time', '')
#     page = int(request.args.get('page', 1))

#     if not log_file_exists():
#         return render_template('search_logs.html', error="Log file not found")

#     matched_lines = get_log_lines(keyword, date, ip, start_time_str, end_time_str)
#     paginated_lines, total_pages = paginate_logs_by_size(matched_lines, page)

#     log_query_to_db(keyword, date, ip, start_time_str, end_time_str)

#     logger.info(f'Search logs with keyword={keyword}, date={date}, ip={ip}, start_time={start_time_str}, end_time={end_time_str}, page={page}')

#     return render_template('search_logs.html',
#                            matched_lines=paginated_lines,
#                            total_pages=total_pages,
#                            current_page=page)


# @bp.route('/view_logs', methods=['GET'])
# def view_logs():
#     keyword = request.args.get('keyword', '')
#     date = request.args.get('date', '')
#     ip = request.args.get('ip', '')
#     start_time = request.args.get('start_time', '')
#     end_time = request.args.get('end_time', '')
#     page = int(request.args.get('page', 1))

#     if not log_file_exists():
#         return "Log file not found", 404

#     matched_lines = get_log_lines(keyword, date, ip, start_time, end_time)
#     paginated_lines, total_pages = paginate_logs_by_size(matched_lines, page)

#     cleaned_lines = [line.strip() for line in paginated_lines]

#     return render_template('view_logs.html',
#                            log_content=cleaned_lines,
#                            current_page=page,
#                            total_pages=total_pages,
#                            keyword=keyword,
#                            date=date,
#                            start_time=start_time,
#                            end_time=end_time,
#                            ip=ip)

# @bp.route('/edit_logs', methods=['GET', 'POST'])
# def edit_logs():
#     form = EditLogsForm()

#     if request.method == 'GET':
#         if not log_file_exists():
#             return "日志文件未找到", 404

#         with open(LOG_FILE_PATH, 'r', encoding='utf-8', errors='ignore') as log_file:
#             log_content = log_file.read()

#         form.log_content.data = log_content

#         page = int(request.args.get('page', 1))
#         log_lines = log_content.splitlines()

#         paginated_lines, total_pages = paginate_logs_by_size(log_lines, page)

#         return render_template('edit_logs.html', form=form, log_lines=paginated_lines, current_page=page,
#                                total_pages=total_pages)

#     elif request.method == 'POST' and form.validate_on_submit():
#         new_content = form.log_content.data

#         try:
#             save_logs_to_file(new_content)
#             flash('日志已成功保存', 'success')
#         except Exception as e:
#             flash(f'保存日志出错: {str(e)}', 'error')

#         return redirect(url_for('routes.edit_logs'))

#     return render_template('edit_logs.html', form=form)

# @bp.route('/save_logs', methods=['POST'])
# def save_logs():
#     new_content = request.form.get('log_content')

#     if not log_file_exists():
#         return "Log file not found", 404

#     # 打印调试信息
#     print(f"Before saving: '{new_content}'")

#     # 保存日志内容前进行 strip 操作，并使用 os.linesep 处理换行符
#     new_content = new_content.strip()
#     new_content = new_content.replace('\r\n', os.linesep).replace('\n', os.linesep)

#     try:
#         with open(LOG_FILE_PATH, 'w', encoding='utf-8') as log_file:
#             log_file.write(new_content)
#     except Exception as e:
#         print(f"Error saving logs: {e}")
#         return "Error saving logs", 500

#     logger.info(f'Logs edited and saved')

#     # 打印保存后的内容
#     print(f"After saving: '{new_content}'")

#     return redirect(url_for('routes.view_logs'))


