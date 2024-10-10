from . import db
from datetime import datetime
import pytz
def get_current_utc_time():
    return datetime.now()

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goodsId = db.Column(db.Integer, nullable=True)
    skuId = db.Column(db.Integer, nullable=True)
    cartId = db.Column(db.Integer, nullable=True)
    count = db.Column(db.Integer, nullable=False)
    selected = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime, default=get_current_utc_time)
    updatedAt = db.Column(db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time)


    def __repr__(self):
        return f"<CartItem {self.id}>"
