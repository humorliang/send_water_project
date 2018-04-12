# 导入对象
from app.exts import db


# 管理员表
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    passworld = db.Column(db.String(30), nullable=False)


# 客户表
class Custom(db.Model):
    __tablename__ = 'custom'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    CustomId = db.Column(db.String(30), nullable=False, unique=True)
    CustomName = db.Column(db.String(30))
    CustomPhone = db.Column(db.String(30))
    CustomAddress = db.Column(db.String(100))
    CustomAccount = db.Column(db.String(30))
    CustomType = db.Column(db.String(30))
    orders = db.relationship('Order', backref='custom')  # 一个顾客多个订单
    serves = db.relationship('Serve', backref='custom')


# 订单表
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    OrderId = db.Column(db.String(30))
    CustomId = db.Column(db.String(30), db.ForeignKey('custom.CustomId'))
    ProductId = db.Column(db.String(30), db.ForeignKey('send.ProductId'), unique=True)
    OrderName = db.Column(db.String(30))
    OrderDate = db.Column(db.Date)
    OrderStatus = db.Column(db.String(30))
    OrderMoney = db.Column(db.String(30))

    products = db.relationship('Product', backref='order')


# 配送表
class Send(db.Model):
    __tablename__ = 'send'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    ProductId = db.Column(db.String(30), nullable=False, unique=True)
    ProductName = db.Column(db.String(30))
    SendName = db.Column(db.String(30))
    SendDate = db.Column(db.Date)
    SendPhone = db.Column(db.String(30))
    SendAddress = db.Column(db.String(100))
    orders = db.relationship('Order', backref='send')


# 产品表
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    ProductId = db.Column(db.String(30), db.ForeignKey('order.ProductId'), nullable=False)
    ProductName = db.Column(db.String(30))
    ProducerName = db.Column(db.String(30))
    ProductDate = db.Column(db.Date)
    ProductType = db.Column(db.String(30))
    ProductPrice = db.Column(db.String(30))


# 售后表
class Serve(db.Model):
    __tablename__ = 'serve'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    ServeId = db.Column(db.String(30))
    CustomId = db.Column(db.String(30), db.ForeignKey('custom.CustomId'), nullable=False)
    ServeDate = db.Column(db.Date)
    ServeInfo = db.Column(db.String(100))
