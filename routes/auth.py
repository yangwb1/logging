from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import db, Asset

bp_auth = Blueprint('auth', __name__)

@bp_auth.route('/login')
def auth_login():
    # 登录视图逻辑
    return render_template('login.html')

@bp_auth.route('/register')
def auth_register():
    # 注册视图逻辑
    return render_template('register.html')
