# 定义项目管理器

from app.__init__ import app
# flask脚本管理器
from flask_script import Manager

# flask数据库迁移
from flask_migrate import Migrate, MigrateCommand

# 导入数据库关系映射实例
from app.exts import db

# 定义数据库迁移
db.init_app(app)

migrate = Migrate(app, db)
# 定义管理器
manager = Manager(app)
# 定义命令
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
