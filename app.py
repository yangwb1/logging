from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_ckeditor import CKEditor
from routes import bp  # 导入蓝图
import os
from flask_migrate import Migrate

app = Flask(__name__)

# 设置密钥
app.config['SECRET_KEY'] = os.urandom(24)

# 配置 CKEditor
app.config['CKEDITOR_PKG_TYPE'] = 'full'
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 400
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///queries.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 确保这行代码存在

# 初始化 CSRF 保护
csrf = CSRFProtect(app)

# 初始化 CKEditor
ckeditor = CKEditor(app)

from models import db
db.init_app(app)

migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(bp)

# 初始化数据库
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)