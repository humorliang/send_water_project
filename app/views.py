from app.__init__ import app
from flask import render_template, redirect, session, url_for, request
from app.models import *
from app.exts import db


# 主界面
@app.route('/')
def index():
    # test = Test(username='zhang')
    # db.session.add(test)
    # db.session.commit()
    # print('-----------')
    return render_template('index.html')


# 登陆路由
@app.route('/login')
def login():
    return render_template('login.html')


# 退出
@app.route('/loginOut')
def login_out():
    return render_template('login.html')


# 注册
@app.route('/register')
def register():
    return render_template('register.html')


# 修改密码
@app.route('/editPwd')
def edit_pwd():
    return render_template('edit-pwd.html')


# 客户信息
@app.route('/customInfo/<int:page>/')
def custom_info(page=None):
    if page is None:
        page = 1
    return render_template('custom-info.html')


# 添加客户
@app.route('/addCustom/')
def add_custom():
    return render_template('add-custom.html')


# 订单信息
@app.route('/orderInfo/<int:page>/')
def order_info(page=None):
    if page is None:
        page = 1
    return render_template('order-info.html')


# 添加订单
@app.route('/addOrder')
def add_order():
    return render_template('add-order.html')


# 配送信息
@app.route('/distributionInfo/<int:page>/')
def distribution_info(page=None):
    if page is None:
        page = 1
    return render_template('distribution-info.html')


# 添加配送
@app.route('/addDistribution')
def add_distribution():
    return render_template('add-distribution.html')


# 库存信息
@app.route('/storeInfo/<int:page>/')
def store_info(page=None):
    if page is None:
        page = 1
    return render_template('store-info.html')


# 添加库存
@app.route('/addStore')
def add_store():
    return render_template('add-store.html')


# 售后信息
@app.route('/serveInfo/<int:page>/')
def serve_info(page=None):
    if page is None:
        page = 1
    return render_template('serve-info.html')


# 添加售后
@app.route('/addServe')
def add_serve():
    return render_template('add-serve.html')
