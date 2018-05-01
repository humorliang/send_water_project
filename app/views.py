# from app.__init__ import app
from flask import render_template, redirect, flash, session, url_for, request, Blueprint
from app.models import *
from app.exts import db
from app.form import LoginForm, SendForm, ServeForm, StoreForm, OrderForm, CustomForm, RegisterForm, \
    EditPwdForm
# 导入表单库
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired
from app.form import validate_is_num, validate_not_in_custom, \
    validate_not_in_product, validate_not_in_order, validate_is_float_num
from functools import wraps
import re

# 定义蓝图
admin = Blueprint('admin', __name__)


# 定义登陆验证装饰器
def is_login(fun):
    @wraps(fun)
    def check_fun(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin.login'))
        return fun(*args, **kwargs)

    return check_fun


# 检查是否是数字
def is_num(data):
    if re.match(r'^[0-9]+$', data) is None:
        return False
    else:
        return True


# 主界面
@admin.route('/')
@is_login
def index():
    return render_template('admin/index.html')


# 登陆路由
@admin.route('/login', methods=['GET', 'POST'])
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
                return redirect(url_for('admin.index'))
            else:
                flash('密码错误')
                return redirect(url_for('admin.login'))
    return render_template('admin/login.html', form=form)


# 退出
@admin.route('/loginOut')
@is_login
def login_out():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


# 注册
@admin.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            user = Admin(username=data['username'], password=data['pwd'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('admin.login'))
    return render_template('admin/register.html', form=form)


# 修改密码
@admin.route('/editPwd', methods=['GET', "POST"])
@is_login
def edit_pwd():
    form = EditPwdForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            user = Admin.query.filter_by(username=data['username']).update(
                dict(password=data['newpwd']))
            db.session.commit()
            return redirect(url_for('admin.login'))
    return render_template('admin/edit-pwd.html', form=form)


# 客户信息
@admin.route('/customInfo/<int:page>/')
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
        custom = Custom.query.filter_by(
            id=k).update(dict(CustomConsume=v))
        db.session.commit()
    customs = Custom.query.paginate(page=page, per_page=6)
    return render_template('admin/custom-info.html', cdata=customs)


# 查询客户信息
@admin.route('/searchCustom', methods=['GET', 'POST'])
@is_login
def search_custom():
    if request.method == 'POST':
        # return request.form.get('search-info') #获取表单数据
        data = request.form.get('search-info')
        if is_num(data):
            id = int(data)
            c_info = Custom.query.filter_by(id=id).all()
            # print(c_info)
            return render_template('admin/s-custom-info.html', cdata=c_info)
        else:
            c_info = Custom.query.filter_by(CustomName=data).all()
            return render_template('admin/s-custom-info.html', cdata=c_info)


# 添加客户
@admin.route('/addCustom/<int:id>/', methods=['GET', 'POST'])
@is_login
def add_custom(id=None):
    form = CustomForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data  # dict字典
            custom = Custom.query.filter_by(id=id).update(
                dict(CustomAccount=data['customaccount'], CustomType=data['customtype'])
            )
            db.session.commit()
            return redirect(url_for('admin.custom_info', page=1))
        print(id)
    return render_template('admin/add-custom.html', form=form)


# 订单信息
@admin.route('/orderInfo/<int:page>/')
@is_login
def order_info(page=None):
    if page is None:
        page = 1
    orders = db.session.query(Order, Product).paginate(page=page, per_page=6)
    return render_template('admin/order-info.html', odata=orders)


# 查询订单
@admin.route('/searchOrder', methods=['GET', 'POST'])
@is_login
def search_order():
    if request.method == 'POST':
        # return request.form.get('search-info') #获取表单数据
        data = request.form.get('search-info')
        if is_num(data):
            c_info = db.session.query(Order, Product).filter(Order.d == int(data)).all()
            return render_template('admin/s-order-info.html', odata=c_info)
        else:
            c_info = db.session.query(Order, Product).filter(Order.OrderStatus == data).all()
            return render_template('admin/s-order-info.html', odata=c_info)


# 编辑订单
@admin.route('/editOrder/<int:id>/', methods=['GET', 'POST'])
@is_login
def edit_Order(id=None):
    # 订单信息模型
    orders = Order.query.filter_by(id=id).first()

    # 编辑订单信息
    class EditOrderForm(FlaskForm):
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
                dict(OrderStatus=data['Ostatus'])
            )
            db.session.commit()
            return redirect(url_for('admin.order_info', page=1))
    return render_template('admin/edit-order.html', form=form)


# 配送信息
@admin.route('/distributionInfo/<int:page>/')
@is_login
def distribution_info(page=None):
    if page is None:
        page = 1
    sends = Send.query.paginate(page=page, per_page=6)
    return render_template('admin/distribution-info.html', sends=sends)


# 查询配送
@admin.route('/searchSend', methods=['GET', 'POST'])
@is_login
def search_send():
    if request.method == 'POST':
        # return request.form.get('search-info') #获取表单数据
        data = request.form.get('search-info')
        if is_num(data):
            c_info = Send.query.filter_by(OrderId=data).all()
            return render_template('admin/s-distribution-info.html', sends=c_info)
        else:
            c_info = Send.query.filter_by(SendName=data).all()
            return render_template('admin/s-distribution-info.html', sends=c_info)


# 添加配送
@admin.route('/addDistribution', methods=['GET', 'POST'])
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
            return redirect(url_for('admin.distribution_info', page=1))
    return render_template('admin/add-distribution.html', form=form)


# 库存信息
@admin.route('/storeInfo/<int:page>/')
@is_login
def store_info(page=None):
    if page is None:
        page = 1
    stores = Product.query.paginate(page=page, per_page=6)
    return render_template('admin/store-info.html', stdata=stores)


# 查询库存
@admin.route('/searchStore', methods=['GET', 'POST'])
@is_login
def search_store():
    if request.method == 'POST':
        # return request.form.get('search-info') #获取表单数据
        data = request.form.get('search-info')
        if is_num(data):
            c_info = Product.query.filter_by(ProductId=data).all()
            return render_template('admin/s-store-info.html', stdata=c_info)
        else:
            c_info = Product.query.filter_by(ProducerName=data).all()
            return render_template('admin/s-store-info.html', stdata=c_info)


# 添加库存
@admin.route('/addStore', methods=['GET', 'POST'])
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
            return redirect(url_for('admin.store_info', page=1))
    return render_template('admin/add-store.html', form=form)


# 编辑库存
@admin.route('/editStore/<int:id>/', methods=['GET', 'POST'])
@is_login
def edit_store(id=None):
    store = Product.query.filter_by(id=id).first()

    # 库存信息
    class StoreForm(FlaskForm):
        pid = StringField(
            validators=[
                DataRequired('产品编号不能为空'),
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
                DataRequired('产品价格不能为空'),
                validate_is_float_num
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
            return redirect(url_for('admin.store_info', page=1))
    return render_template('admin/edit-store.html', form=form)


# 售后信息
@admin.route('/serveInfo/<int:page>/')
@is_login
def serve_info(page=None):
    if page is None:
        page = 1
    serves = Serve.query.paginate(page=page, per_page=6)
    return render_template('admin/serve-info.html', sedata=serves)


# 查询售后
@admin.route('/searchServe', methods=['GET', 'POST'])
@is_login
def search_serve():
    if request.method == 'POST':
        # return request.form.get('search-info') #获取表单数据
        data = request.form.get('search-info')
        if is_num(data):
            c_info = Serve.query.filter_by(ServeId=data).all()
            return render_template('admin/s-serve-info.html', sedata=c_info)
        else:
            c_info = Serve.query.filter_by(ServeInfo=data).all()
            return render_template('admin/s-serve-info.html', sedata=c_info)


# 添加售后
@admin.route('/addServe', methods=['GET', 'POST'])
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
            return redirect(url_for('admin.serve_info', page=1))
    return render_template('admin/add-serve.html', form=form)
