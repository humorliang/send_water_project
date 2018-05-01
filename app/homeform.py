from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import EqualTo, ValidationError, DataRequired
from app.models import *
import re


# 用户名不存在验证器
def validate_in_user(form, field):
    data = field.data
    num = Custom.query.filter_by(username=data).count()
    if num == 0:
        raise ValidationError('用户名不存在')


# 用户名存在验证器
def validate_not_in_user(form, field):
    data = field.data
    num = Custom.query.filter_by(username=data).count()
    if num != 0:
        raise ValidationError('用户名已经存在')


# 密码不对验证器
def validate_in_pwd(form, field):
    data = field.data
    username = session.get('user')
    user = Custom.query.filter_by(username=username).first()
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
    customname = StringField(
        validators=[
            DataRequired('姓名不能为空'),

        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '姓名'
        }
    )
    customphone = StringField(
        validators=[
            DataRequired('联系方式不能为空'),
            validate_is_phone
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '联系方式'
        }
    )
    customaddress = StringField(
        validators=[
            DataRequired('地址不能为空')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '地址'
        }
    )
    submit = SubmitField(
        label='注册',
        render_kw={
            'class': 'btn btn-lg btn-primary btn-block'
        }
    )
