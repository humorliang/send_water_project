from flask import Blueprint

# 生成页面蓝图
home = Blueprint('home', __name__)


# 页面使用视图函数
@home.route('/')
def index():
    return 'hello home'
