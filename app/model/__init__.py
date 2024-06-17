# models/__init__.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .ad import Ad
from .address import Address
from .admin import Admin
from .court import Court
from .goods import Goods
from .goodsType import GoodsType
from .receipt import *
from .vip import Vip

# 其他模型导入
