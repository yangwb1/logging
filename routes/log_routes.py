from flask import Blueprint, render_template, request
from elasticsearch import Elasticsearch, exceptions as es_exceptions
from datetime import datetime, timedelta
import logging
from models import db, Asset, AssetForm  # 使用绝对导入


bp = Blueprint('log_routes', __name__)
logger = logging.getLogger(__name__)

es = Elasticsearch(
    ['https://localhost:9200'],
    http_auth=('elastic', 'wsayCf-c644HMSqDZUR7'),  # 替换为你的用户名和密码
    verify_certs=True,
    ca_certs="D:\\Program Files\\elasticsearch-8.14.1\\elastic-stack-ca.p12"
)

@bp.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    logs_per_page = 15
    logs = []
    date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
    try:
        start_date = datetime.strptime(date, '%Y-%m-%d')
        end_date = start_date + timedelta(days=1)
        result = es.search(
            index='winlogbeat-*',
            body={
                'query': {
                    'range': {
                        '@timestamp': {
                            'gte': start_date.isoformat(),
                            'lt': end_date.isoformat()
                        }
                    }
                },
                'sort': {'@timestamp': {'order': 'desc'}},
                'size': logs_per_page,
                'from': (page - 1) * logs_per_page
            }
        )
        hits = result['hits']['hits']
        for hit in hits:
            log = hit['_source']
            log['full_content'] = hit['_source']
            logs.append(log)
        logs = [{'sequence': (page - 1) * logs_per_page + i + 1, 'content': hit['_source']} for i, hit in enumerate(hits)]
        total = result['hits']['total']['value']
        total_pages = (total + logs_per_page - 1) // logs_per_page
        print(f"Successfully retrieved {len(logs)} logs from Elasticsearch")
    except es_exceptions.ConnectionError as ce:
        print(f"Error connecting to Elasticsearch: {ce}")
        logs = []
    except es_exceptions.AuthorizationException as ae:
        print(f"Authorization failed: {ae}")
        logs = []
    except Exception as e:
        print(f"Error retrieving logs from Elasticsearch: {e}")
        logs = []

    return render_template('logs.html', logs=logs, page=page, total_pages=total_pages, date=date)
