from . import db
from datetime import datetime
import pytz
def get_current_utc_time():
    return datetime.now()
class OrderItem(db.Model):
    __tablename__ = 'order_items'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderId = db.Column(db.String(36), nullable=False)
    skuId = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    isDeleted = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime, default=get_current_utc_time)
    updatedAt = db.Column(db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time)


    def __repr__(self):
        return f"<OrderItem {self.id}>"
