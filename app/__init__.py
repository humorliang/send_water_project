from flask import Flask
# 导入配置对象
import app.config as config

# 导入数据库映射实力
from app.exts import db

# 让app接收到views模块 要让views在上面,影响
# 管理器接收到views
import app.views

# 创建flask实例
app = Flask(__name__)

# 将配置文件导入app
app.config.from_object(config)

# 注册蓝图
from app.mainView import home as home_b

app.register_blueprint(home_b)
from app.views import admin as admin_b

app.register_blueprint(admin_b, url_prefix='/admin')

# 将app导入db示例中
db.init_app(app)
