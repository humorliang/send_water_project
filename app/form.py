from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import EqualTo, ValidationError, DataRequired
from app.models import *
import re


# 自定义验证器
# 数字验证器
def validate_is_num(form, field):
    data = field.data
    if re.match(r'[0-9]+$', data) is None:
        raise ValidationError('请填写正确的数字')


# 自定义验证器
# 数字验证器
def validate_is_float_num(form, field):
    data = field.data
    if re.match(r'([0-9]+$)|([0-9]+\.[0-9]{2}$)', data) is None:
        raise ValidationError('请填写正确的数字或小数请保留两位')


# 客户编号不存在验证器
def validate_not_in_custom(form, field):
    data = field.data
    num = Custom.query.filter(Custom.id == data).count()
    if num == 0:
        raise ValidationError('您输入的客户编号不存在')


# 客户编号存在验证器

def validate_in_custom(form, field):
    data = field.data
    num = Custom.query.filter(Custom.id == data).count()
    if num != 0:
        raise ValidationError('您输入的客户编号已经存在')


# 订单编号不存在验证器
def validate_not_in_order(form, field):
    data = field.data
    num = Order.query.filter(Order.id == data).count()
    if num == 0:
        raise ValidationError('您输入的订单编号不存在')


# 订单编号存在验证器
def validate_in_order(form, field):
    data = field.data
    num = Order.query.filter(Order.id == data).count()
    if num != 0:
        raise ValidationError('您输入的订单编号已经存在')


# 产品编号不存在
def validate_not_in_product(form, field):
    data = field.data
    num = Product.query.filter(Product.ProductId == data).count()
    if num == 0:
        raise ValidationError('您输入的产品编号不存在')


# 产品编号存在
def validate_in_product(form, field):
    data = field.data
    num = Product.query.filter(Product.ProductId == data).count()
    if num != 0:
        raise ValidationError('您输入的产品编号已经存在')


# 用户名不存在验证器
def validate_in_user(form, field):
    data = field.data
    num = Admin.query.filter_by(username=data).count()
    if num == 0:
        raise ValidationError('用户名不存在')


# 用户名存在验证器
def validate_not_in_user(form, field):
    data = field.data
    num = Admin.query.filter_by(username=data).count()
    if num != 0:
        raise ValidationError('用户名已经存在')


# 密码不对验证器
def validate_in_pwd(form, field):
    data = field.data
    username = session.get('admin')
    user = Admin.query.filter_by(username=username).first()
    if not user.check_pwd(data):
        raise ValidationError('您输入的密码不正确')


# 手机号码验证器
def validate_is_phone(form, field):
    phone = field.data
    if re.match(r'^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$', phone) is None:
        raise ValidationError('请输入正确的手机号')


# 登陆表单
class LoginForm(FlaskForm):
    username = StringField(
        validators=[
            DataRequired('用户名不能为空'),
            validate_in_user
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '用户名'
        }
    )
    password = PasswordField(
        validators=[
            DataRequired('密码不能为空'),
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '密码'
        }
    )
    remember = BooleanField(
        label='记住密码'
    )
    submit = SubmitField(
        label='登陆',
        render_kw={
            'class': 'btn btn-md btn-primary btn-block'
        }
    )


# 注册表单
class RegisterForm(FlaskForm):
    username = StringField(
        validators=[
            DataRequired('用户名不能为空'),
            validate_not_in_user
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '用户名'
        }
    )
    pwd = PasswordField(
        validators=[
            DataRequired('密码不能为空'),
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '密码'
        }
    )
    repwd = PasswordField(
        validators=[
            DataRequired('确认密码不能为空'),
            EqualTo('pwd', message='两次密码不一致')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '确认密码'
        }
    )
    submit = SubmitField(
        label='注册',
        render_kw={
            'class': 'btn btn-lg btn-primary btn-block'
        }
    )


# 修改密码
class EditPwdForm(FlaskForm):
    username = StringField(
        validators=[
            DataRequired('用户名不能为空'),
            validate_in_user
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '用户名'
        }
    )
    oldpwd = PasswordField(
        validators=[
            DataRequired('旧密码不能为空'),
            validate_in_pwd
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '旧密码'
        }
    )
    newpwd = PasswordField(
        validators=[
            DataRequired('新密码不能为空'),
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '新密码'
        }
    )
    renewpwd = PasswordField(
        validators=[
            DataRequired('确认新密码不能为空'),
            EqualTo('newpwd', message='两次新密码不一致')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '确认新密码'
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            'class': 'btn btn-lg btn-primary btn-block'
        }
    )


# 客户信息表单
class CustomForm(FlaskForm):
    customaccount = StringField(
        validators=[
            DataRequired('账户金额不能为空'),
            validate_is_num
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '账户金额'
        }
    )
    customtype = StringField(
        validators=[
            DataRequired('客户类型不能为空')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '客户类型'
        }
    )
    submit = SubmitField(
        label='添加',
        render_kw={
            'class': 'btn btn-primary'
        }
    )


# 订单信息表单
class OrderForm(FlaskForm):
    Cid = StringField(
        validators=[
            DataRequired('客户编号不能为空'),
            validate_not_in_custom,
            validate_is_num
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '客户编号'
        }
    )
    Oid = StringField(
        validators=[
            DataRequired('订单编号不能为空'),
            validate_in_order,
            validate_is_num
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '订单编号'
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
            'placeholder': '商品编号'
        }
    )
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
            'placeholder': '年-月-日'
        }
    )
    submit = SubmitField(
        label='添加',
        render_kw={
            'class': 'btn btn-primary'
        }
    )


# 库存信息
class StoreForm(FlaskForm):
    pid = StringField(
        validators=[
            DataRequired('产品编号不能为空'),
            validate_in_product
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '产品编号'
        }
    )
    pname = StringField(
        validators=[
            DataRequired('产品名称不能为空')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '产品名称'
        }
    )
    producer = StringField(
        validators=[
            DataRequired('生产商不能为空')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '生产商'
        }
    )
    pdate = DateField(
        validators=[
            DataRequired('产品日期不能为空')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '年-月-日'
        }
    )
    ptype = StringField(
        validators=[
            DataRequired('产品类型不能为空')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '产品类型'
        }
    )
    price = StringField(
        validators=[
            DataRequired('产品价格不能为空'),
            validate_is_float_num
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '产品价格'
        }
    )
    pnum = StringField(
        validators=[
            DataRequired('库存数量不能为空'),
            validate_is_num
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '库存数量'
        }
    )
    submit = SubmitField(
        label='添加',
        render_kw={
            'class': 'btn btn-primary'
        }
    )


# 配送信息
class SendForm(FlaskForm):
    Oid = StringField(
        validators=[
            DataRequired('订单编号不能为空'),
            validate_not_in_order
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '订单编号'
        }
    )
    Pname = StringField(
        validators=[
            DataRequired('产品名称不能为空')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '产品名称'
        }
    )
    Sname = StringField(
        validators=[
            DataRequired('配送人不能为空')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '配送人'
        }
    )
    Sdate = DateField(
        validators=[
            DataRequired('配送日期不能为空')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '年-月-日'
        }
    )
    Sphone = StringField(
        validators=[
            DataRequired('联系方式不能为空'),
            validate_is_phone
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '联系方式'
        }
    )
    Saddress = StringField(
        validators=[
            DataRequired('配送地址不能为空')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '配送地址'
        }
    )
    submit = SubmitField(
        label='添加',
        render_kw={
            'class': 'btn btn-primary'
        }
    )


# 售后信息
class ServeForm(FlaskForm):
    Seid = StringField(
        validators=[
            DataRequired('售后编号不能为空')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '售后编号'
        }
    )
    Cid = StringField(
        validators=[
            DataRequired('客户编号不能为空'),
            validate_not_in_custom
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '客户编号'
        }
    )
    Sedate = DateField(
        validators=[
            DataRequired('售后日期不能为空')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '年-月-日'
        }
    )
    Seinfo = StringField(
        validators=[
            DataRequired('售后说明不能为空')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '售后说明'
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            'class': 'btn btn-primary'
        }
    )
