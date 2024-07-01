from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
import os

# 初始化应用
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

# 导入数据库和迁移工具
from models import db
db.init_app(app)
migrate = Migrate(app, db)

# 注册蓝图
from routes.main import bp as main_bp
from routes.auth import bp_auth as auth_bp
app.register_blueprint(main_bp, url_prefix='/main')
app.register_blueprint(auth_bp, url_prefix='/auth')

# 初始化数据库
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
