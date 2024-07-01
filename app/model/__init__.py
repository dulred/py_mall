'''
Author: yzs dulred@qq.com
Date: 2024-06-13 09:04:38
LastEditors: yzs dulred@qq.com
LastEditTime: 2024-07-01 10:40:19
FilePath: \py_mall\app\model\__init__.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE

'''
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
from .comment import Comment
# 其他模型导入
