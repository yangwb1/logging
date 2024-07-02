from flask import Blueprint, render_template, request, redirect
from pygrok import Grok
from models import db, Asset, AssetForm  # 使用绝对导入


bp = Blueprint('grok_routes', __name__)

GROK_PATTERN = '%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:loglevel} %{GREEDYDATA:message}'

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            logs = file.read().decode('utf-8').splitlines()
            parsed_logs = parse_logs(logs)
            return render_template('grok_upload.html', logs=parsed_logs)
    return render_template('grok_upload.html')

def parse_logs(logs):
    grok = Grok(GROK_PATTERN)
    parsed_logs = []
    for line in logs:
        match = grok.match(line)
        if match:
            parsed_logs.append(match)
    return parsed_logs
