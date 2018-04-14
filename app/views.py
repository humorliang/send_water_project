from app.__init__ import app
from flask import render_template, redirect, flash, session, url_for, request
from app.models import *
from app.exts import db
from app.form import LoginForm, SendForm, ServeForm, StoreForm, OrderForm, CustomForm, RegisterForm, \
    EditPwdForm
# 导入表单库
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired
from app.form import validate_is_num, validate_not_in_custom, \
    validate_not_in_product, validate_not_in_order
from functools import wraps

# 导入字典类
from collections import defaultdict


# 定义登陆验证装饰器
def is_login(fun):
    @wraps(fun)
    def check_fun(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('login'))
        return fun(*args, **kwargs)

    return check_fun


# 主界面
@app.route('/')
@is_login
def index():
    return render_template('index.html')


# 登陆路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            user = Admin.query.filter_by(username=data['username']).first()
            if user.check_pwd(data['password']):
                session['admin'] = data['username']
                if data['remember']:
                    session.permanent = True
                return redirect(url_for('index'))
            else:
                flash('密码错误')
                return redirect(url_for('login'))
    return render_template('login.html', form=form)


# 退出
@app.route('/loginOut')
@is_login
def login_out():
    session.pop('admin', None)
    return redirect(url_for('login'))


# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            user = Admin(username=data['username'], password=data['pwd'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


# 修改密码
@app.route('/editPwd', methods=['GET', "POST"])
@is_login
def edit_pwd():
    form = EditPwdForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            user = Admin.query.filter_by(username=data['username']).update(dict(password=data['newpwd']))
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('edit-pwd.html', form=form)


# 客户信息
@app.route('/customInfo/<int:page>/')
@is_login
def custom_info(page=None):
    if page is None:
        page = 1
    # 数据为可迭代模型list
    data = Order.query.filter_by(OrderStatus='已完成').all()
    # 订单总消费金额字典
    num = {}
    for v in data:
        if v.CustomId in num.keys():
            num[v.CustomId] += int(v.OrderMoney)
        else:
            num[v.CustomId] = int(v.OrderMoney)

    for k, v in num.items():
        custom = Custom.query.filter_by(CustomId=k).update(dict(CustomConsume=v))
        db.session.commit()
    customs = Custom.query.paginate(page=page, per_page=2)
    return render_template('custom-info.html', cdata=customs)


# 添加客户
@app.route('/addCustom', methods=['GET', 'POST'])
@is_login
def add_custom():
    form = CustomForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data  # dict字典
            custom = Custom(CustomId=data['customid'], CustomName=data['customname'],
                            CustomAccount=data['customaccount'], CustomPhone=data['customphone'],
                            CustomAddress=data['customaddress'], CustomType=data['customtype'])
            db.session.add(custom)
            db.session.commit()
            return redirect(url_for('custom_info', page=1))
    return render_template('add-custom.html', form=form)


# 订单信息
@app.route('/orderInfo/<int:page>/')
@is_login
def order_info(page=None):
    if page is None:
        page = 1
    orders = Order.query.paginate(page=page, per_page=2)
    return render_template('order-info.html', odata=orders)


# 添加订单
@app.route('/addOrder', methods=['GET', 'POST'])
@is_login
def add_order():
    form = OrderForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            order = Order(OrderId=data['Oid'], CustomId=data['Cid'],
                          ProductId=data['Pid'], OrderNum=data['Onum'],
                          OrderDate=data['Odate'], OrderStatus=data['Ostatus'],
                          OrderMoney=data['Omoney'])
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('order_info', page=1))
    return render_template('add-order.html', form=form)


# 编辑订单
@app.route('/editOrder/<int:id>/', methods=['GET', 'POST'])
@is_login
def edit_Order(id=None):
    # 订单信息模型
    orders = Order.query.filter_by(id=id).first()

    # 编辑订单信息
    class EditOrderForm(FlaskForm):
        Cid = StringField(
            validators=[
                DataRequired('客户编号不能为空'),
                validate_not_in_custom
            ],
            render_kw={
                'class': 'form-control',
                'placeholder': '客户编号',
                'value': orders.CustomId
            }
        )
        Oid = StringField(
            validators=[
                DataRequired('订单编号不能为空'),
                validate_not_in_order,
                validate_is_num
            ],
            render_kw={
                'class': 'form-control',
                'placeholder': '订单编号',
                'value': orders.OrderId
            }
        )
        Pid = StringField(
            validators=[
                DataRequired('商品编号不能为空'),
                validate_not_in_product,
                validate_is_num
            ],
            render_kw={
                'class': 'form-control',
                'placeholder': '商品编号',
                'value': orders.ProductId
            }
        )
        Onum = StringField(
            validators=[
                DataRequired('订单数量不能为空'),
                validate_is_num
            ],
            render_kw={
                'class': 'form-control',
                'placeholder': '订单数量',
                'value': orders.OrderNum
            }
        )
        Ostatus = SelectField(
            choices=[
                ('未完成', '未完成'),
                ('已完成', '已完成'),
                ('配送中', '配送中')
            ],
            render_kw={
                'class': 'form-control',
                'placeholder': '订单状态'
            }
        )
        Odate = DateField(
            validators=[
                DataRequired('订单日期不能为空')
            ],
            render_kw={
                'class': 'form-control',
                'placeholder': '年-月-日',
                'value': orders.OrderDate
            }
        )
        Omoney = StringField(
            validators=[
                DataRequired('总金额不能为空')
            ],
            render_kw={
                'class': 'form-control',
                'placeholder': '总金额',
                'value': orders.OrderMoney
            }
        )
        submit = SubmitField(
            label='保存',
            render_kw={
                'class': 'btn btn-primary'
            }
        )

    form = EditOrderForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            orders_ = Order.query.filter_by(id=id).update(
                dict(OrderId=data['Oid'], CustomId=data['Cid'],
                     ProductId=data['Pid'], OrderNum=data['Onum'],
                     OrderDate=data['Odate'], OrderStatus=data['Ostatus'],
                     OrderMoney=data['Omoney'])
            )
            db.session.commit()
            return redirect(url_for('order_info', page=1))
    return render_template('edit-order.html', form=form)


# 配送信息
@app.route('/distributionInfo/<int:page>/')
@is_login
def distribution_info(page=None):
    if page is None:
        page = 1
    sends = Send.query.paginate(page=page, per_page=2)
    return render_template('distribution-info.html', sends=sends)


# 添加配送
@app.route('/addDistribution', methods=['GET', 'POST'])
@is_login
def add_distribution():
    form = SendForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            sends = Send(OrderId=data['Oid'], ProductName=data['Pname'],
                         SendName=data['Sname'], SendDate=data['Sdate'],
                         SendPhone=data['Sphone'], SendAddress=data['Saddress'])
            db.session.add(sends)
            db.session.commit()
            return redirect(url_for('distribution_info', page=1))
    return render_template('add-distribution.html', form=form)


# 库存信息
@app.route('/storeInfo/<int:page>/')
@is_login
def store_info(page=None):
    if page is None:
        page = 1
    stores = Product.query.paginate(page=page, per_page=2)
    return render_template('store-info.html', stdata=stores)


# 添加库存
@app.route('/addStore', methods=['GET', 'POST'])
@is_login
def add_store():
    form = StoreForm()
    if request.method == "POST":
        if form.validate_on_submit():
            data = form.data
            product = Product(ProductId=data['pid'], ProductName=data['pname'],
                              ProducerName=data['producer'], ProductDate=data['pdate'],
                              ProductType=data['ptype'], ProductPrice=data['price'],
                              ProductNum=data['pnum'])
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('store_info', page=1))
    return render_template('add-store.html', form=form)


# 编辑库存
@app.route('/editStore/<int:id>/', methods=['GET', 'POST'])
@is_login
def edit_store(id=None):
    store = Product.query.filter_by(id=id).first()

    # 库存信息
    class StoreForm(FlaskForm):
        pid = StringField(
            validators=[
                DataRequired('产品编号不能为空'),
                validate_not_in_product
            ],
            render_kw={
                'class': 'form-control',
                'placeholder': '产品编号',
                'value': store.ProductId
            }
        )
        pname = StringField(
            validators=[
                DataRequired('产品名称不能为空')
            ],
            render_kw={
                'class': 'form-control',
                'placeholder': '产品名称',
                'value': store.ProductName
            }
        )
        producer = StringField(
            validators=[
                DataRequired('生产商不能为空')
            ],
            render_kw={
                'class': 'form-control',
                'placeholder': '生产商',
                'value': store.ProducerName
            }
        )
        pdate = DateField(
            validators=[
                DataRequired('产品日期不能为空')
            ],
            render_kw={
                'class': 'form-control',
                'placeholder': '年-月-日',
                'value': store.ProductDate
            }
        )
        ptype = StringField(
            validators=[
                DataRequired('产品类型不能为空')
            ],
            render_kw={
                'class': 'form-control',
                'placeholder': '产品类型',
                'value': store.ProductType
            }
        )
        price = StringField(
            validators=[
                DataRequired('产品价格不能为空')
            ],
            render_kw={
                'class': 'form-control',
                'placeholder': '产品价格',
                'value': store.ProductPrice
            }
        )
        pnum = StringField(
            validators=[
                DataRequired('库存数量不能为空'),
                validate_is_num
            ],
            render_kw={
                'class': 'form-control',
                'placeholder': '库存数量',
                'value': store.ProductNum
            }
        )
        submit = SubmitField(
            label='保存',
            render_kw={
                'class': 'btn btn-primary'
            }
        )

    form = StoreForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            store_ = Product.query.filter_by(id=id).update(
                dict(ProductId=data['pid'], ProductName=data['pname'],
                     ProducerName=data['producer'], ProductDate=data['pdate'],
                     ProductType=data['ptype'], ProductPrice=data['price'],
                     ProductNum=data['pnum'])
            )
            db.session.commit()
            return redirect(url_for('store_info', page=1))
    return render_template('edit-store.html', form=form)


# 售后信息
@app.route('/serveInfo/<int:page>/')
@is_login
def serve_info(page=None):
    if page is None:
        page = 1
    serves = Serve.query.paginate(page=page, per_page=2)
    return render_template('serve-info.html', sedata=serves)


# 添加售后
@app.route('/addServe', methods=['GET', 'POST'])
@is_login
def add_serve():
    form = ServeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            print(data)
            serves = Serve(ServeId=data['Seid'], CustomId=data['Cid'],
                           ServeDate=data['Sedate'], ServeInfo=data['Seinfo'])
            db.session.add(serves)
            db.session.commit()
            return redirect(url_for('serve_info', page=1))
    return render_template('add-serve.html', form=form)
