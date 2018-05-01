from flask import render_template, redirect, flash, session, url_for, request, Blueprint
from app.models import *
from app.exts import db
from app.homeform import LoginForm, RegisterForm
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import EqualTo, ValidationError, DataRequired
import re

# 生成页面蓝图
home = Blueprint('home', __name__)


# 数字验证器
def validate_is_num(form, field):
    data = field.data
    if re.match(r'[0-9]+$', data) is None:
        raise ValidationError('请填写正确的数字')


# 定义登陆验证装饰器
def u_is_login(fun):
    @wraps(fun)
    def check_fun(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('home.login'))
        return fun(*args, **kwargs)

    return check_fun


# 主界面
@home.route('/')
@u_is_login
def index():
    return render_template('home/index.html')


# 登陆路由
@home.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            user = Custom.query.filter_by(username=data['username']).first()
            if user.check_pwd(data['password']):
                session['user'] = data['username']
                if data['remember']:
                    session.permanent = True
                return redirect(url_for('home.index'))
            else:
                flash('密码错误')
                return redirect(url_for('home.login'))
    return render_template('home/login.html', form=form)


# 退出
@home.route('/loginOut')
@u_is_login
def login_out():
    session.pop('user', None)
    return redirect(url_for('home.login'))


# 注册
@home.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            user = Custom(username=data['username'], password=data['pwd'], CustomName=data['customname'],
                          CustomPhone=data['customphone'], CustomAddress=data['customaddress'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home.login'))
    return render_template('home/register.html', form=form)


# 查询订单
@home.route('/searchOrder')
@u_is_login
def search_order():
    username = session.get('user')
    custom = Custom.query.filter_by(username=username).first()
    c_info = db.session.query(Order, Product).filter(Order.CustomId == custom.id,
                                                     Order.ProductId == Product.ProductId).all()
    return render_template('home/order-info.html', odata=c_info)


# 查询配送
@home.route('/searchSend', methods=['GET', 'POST'])
@u_is_login
def search_send():
    username = session.get('user')
    custom = Custom.query.filter_by(username=username).first()
    c_info = db.session.query(Order, Send).filter(Order.CustomId == custom.id,
                                                  Order.id == Send.OrderId).all()
    return render_template('home/send-info.html', sends=c_info)


# 售后信息
@home.route('/searchServe', methods=['GET', 'POST'])
@u_is_login
def search_serve():
    username = session.get('user')
    custom = Custom.query.filter_by(username=username).first()
    c_info = Serve.query.filter_by(CustomId=custom.id).all()
    return render_template('home/serve-info.html', sedata=c_info)


# 添加订单
@home.route('/addOrder', methods=['GET', 'POST'])
@u_is_login
def add_order():
    # 产品种类
    list = []
    proName = Product.query.all()
    for v in proName:
        list.append((v.ProductName, v.ProductName))
    # 客户编号
    username = session.get('user')
    custom = Custom.query.filter_by(username=username).first()
    id=custom.id
    # print(list)
    class OrderForm(FlaskForm):
        Onum = StringField(
            validators=[
                DataRequired('订单数量不能为空'),
                validate_is_num
            ],
            render_kw={
                'class': 'form-control',
                'placeholder': '订单数量'
            }
        )
        Pna = SelectField(
            choices=list,  # 可迭代对象
            render_kw={
                'class': 'form-control',
            }
        )
        Odate = DateField(
            validators=[
                DataRequired('订单日期不能为空')
            ],
            render_kw={
                'class': 'form-control',
                'placeholder': '年-月-日'
            }
        )
        submit = SubmitField(
            label='添加',
            render_kw={
                'class': 'btn btn-primary'
            }
        )

    form = OrderForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            product = Product.query.filter_by(ProductName=data['Pna']).first()

            if int(product.ProductNum) < int(data['Onum']):
                flash('该产品库存数量不足')
                return redirect(url_for('home.add_order', form=form))
            else:
                order = Order(CustomId=id,
                              ProductId=product.ProductId, OrderNum=data['Onum'],
                              OrderDate=data['Odate'], OrderStatus='未完成',
                              OrderMoney=int(data['Onum']) * int(product.ProductPrice))
                db.session.add(order)
                db.session.commit()
                products = Product.query.filter_by(ProductName=data['Pna']).update(
                    dict(ProductNum=int(product.ProductNum) - int(data['Onum'])))
                db.session.commit()
                return redirect(url_for('home.search_order'))
    return render_template('home/add-order.html', form=form)
