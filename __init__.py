from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
from models import db
from routes import register_blueprints
import os

def create_app():
    app = Flask(__name__)

    # 设置密钥
    app.config['SECRET_KEY'] = os.urandom(24)

    # 配置 CKEditor
    app.config['CKEDITOR_PKG_TYPE'] = 'full'
    app.config['CKEDITOR_SERVE_LOCAL'] = True
    app.config['CKEDITOR_HEIGHT'] = 400

    # 数据库配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///queries.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化 CSRF 保护
    csrf = CSRFProtect(app)

    # 初始化 CKEditor
    ckeditor = CKEditor(app)

    # 初始化数据库和迁移工具
    db.init_app(app)
    migrate = Migrate(app, db)

    # 注册蓝图
    register_blueprints(app)

    # 初始化数据库
    with app.app_context():
        db.create_all()

    return app
