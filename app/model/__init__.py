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

from .users import User
from .tags import Tag
from .addresses import Address
from .suppliers import Supplier
from .logistic import Logistic
from .delivery import Delivery
from .reviews import Review
from .returns import Return
from .orders import Order
from .orderItems import OrderItem
from .goodsTags import GoodsTag
from .categories import Category
from .cartItems import CartItem
from .cart import Cart
from .brands import Brand
from .addresses import Address
from .goods import Goods
from .sw import SW
from .carousel import Carousel
from .detail_img import Deatil_img
from .thumb_img import Thumb_img
from .goodsStyle import GoodsStyle
from .sku import Sku
from .specs import Specs
from .goods_config import Goods_config
from .admin_user import AdminUser
# 其他模型导入
