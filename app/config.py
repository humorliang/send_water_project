# coding:utf-8
import os

DEBUG = True  # 调试模式

SECRET_KEY = os.urandom(24)  # session的密钥

# 数据库连接设置
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'sendcms'
USERNAME = 'root'
PASSWORD = '123456'
DB_URL = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URL

SQLALCHEMY_TRACK_MODIFICATIONS = True

