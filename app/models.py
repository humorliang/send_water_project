# 导入对象
from app.exts import db


# 管理员表
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def check_pwd(self, pwd):
        if self.password == pwd:
            return True
        else:
            return False


# 客户表
class Custom(db.Model):
    __tablename__ = 'custom'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)  # 客户的id
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    # CustomId = db.Column(db.String(30), unique=True)
    CustomName = db.Column(db.String(30), default='无')
    CustomPhone = db.Column(db.String(30), default='无')
    CustomAddress = db.Column(db.String(100), default='无')
    CustomAccount = db.Column(db.String(30), default='无')
    CustomType = db.Column(db.String(30), default='无')
    CustomConsume = db.Column(db.String(30), default=0)
    orders = db.relationship('Order', backref='custom')  # 一个顾客多个订单
    serves = db.relationship('Serve', backref='custom')

    def check_pwd(self, pwd):
        if self.password == pwd:
            return True
        else:
            return False

    def __repr__(self):
        return self.CustomConsume, self.CustomAccount


# 辅助表db.Table声明由sqlalchemy进行管理
# 要放在两个模型上面不然会出现错误，有个模型要用到po名称
po = db.Table('po',
              db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
              db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
              )


# 订单表
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    CustomId = db.Column(db.Integer, db.ForeignKey('custom.id'))
    ProductId = db.Column(db.String(30))
    OrderNum = db.Column(db.String(30))
    OrderDate = db.Column(db.Date)
    OrderStatus = db.Column(db.String(30))
    OrderMoney = db.Column(db.String(30))
    products = db.relationship('Product', secondary=po, backref=db.backref('order'))
    sends = db.relationship('Send', backref='order', uselist=False)

    def __repr__(self):
        return self.OrderId, self.CustomId, self.ProductId, self.OrderNum, \
               self.OrderDate, self.OrderStatus, self.OrderMoney


# 产品表
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    ProductId = db.Column(db.String(30), unique=True)
    ProductName = db.Column(db.String(30))
    ProducerName = db.Column(db.String(30))
    ProductDate = db.Column(db.Date)
    ProductType = db.Column(db.String(30))
    ProductPrice = db.Column(db.String(30))
    ProductNum = db.Column(db.String(30))

    def __repr__(self):
        return self.ProductId, self.ProducerName, self.ProductDate, self.ProductName, \
               self.ProductType, self.ProductPrice, self.ProductNum


# 配送表
class Send(db.Model):
    __tablename__ = 'send'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    OrderId = db.Column(db.Integer, db.ForeignKey('order.id'))
    ProductName = db.Column(db.String(30))
    SendName = db.Column(db.String(30))
    SendDate = db.Column(db.Date)
    SendPhone = db.Column(db.String(30))
    SendAddress = db.Column(db.String(100))


# 售后表
class Serve(db.Model):
    __tablename__ = 'serve'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    ServeId = db.Column(db.String(30))
    CustomId = db.Column(db.Integer, db.ForeignKey('custom.id'), nullable=False)
    ServeDate = db.Column(db.Date)
    ServeInfo = db.Column(db.String(100))
