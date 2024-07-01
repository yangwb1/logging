from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField

db = SQLAlchemy()

class QueryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    keyword = db.Column(db.String(200))
    date = db.Column(db.String(10))
    ip = db.Column(db.String(15))
    start_time = db.Column(db.String(5))
    end_time = db.Column(db.String(5))

    def __repr__(self):
        return f'<QueryLog {self.id}>'

# class Asset(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     ip_address = db.Column(db.String(50), unique=True, nullable=False)
#     description = db.Column(db.String(200))


# 示例模型
class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    ip_address = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))

class EditLogsForm(FlaskForm):
    log_content = CKEditorField('Log Content')
    submit = SubmitField('Save')

class AssetForm(FlaskForm):
    ip_address = StringField('IP 地址')
    description = StringField('描述')
    submit = SubmitField('保存')