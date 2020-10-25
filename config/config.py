# coding: utf-8

# DB部分
DIALECT ='mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = '' # 数据库密码
HOST = 'localhost'
PORT = '3306'
DATABSE = '' # 数据库名
SQLALCHEMY_DATABASE_URI ="{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABSE)

SQLALCHEMY_ECHO = False # 是否显示执行SQL信息

SQLALCHEMY_POOL_SIZE = 10 # 默认为5
SQLALCHEMY_POOL_TIMEOUT = 5 # 默认为10
SQLALCHEMY_POOL_RECYCLE = 7200 # 默认7200

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Server部分
SERVER_PORT = 5000

# 数据交互
JSON_AS_ASCII = False # jsonify()方法让编码不显示ascii
SESSION_COOKIE_HTTPONLY = False

import os
SECRET_KEY = os.urandom(24)
from datetime import timedelta
PERMANENT_SESSION_LIFETIME = timedelta(days=1) # 一天后失效