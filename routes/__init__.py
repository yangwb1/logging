from flask import Blueprint

bp = Blueprint('routes', __name__)

# 导入其他模块，确保它们的路由被注册
from . import main, auth
