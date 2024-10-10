from . import db
from datetime import datetime
import pytz
def get_current_utc_time():
    return datetime.now()

class Order(db.Model):
    __tablename__ = 'orders'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.String(36), primary_key=True)
    userId = db.Column(db.Integer,nullable=False)
    orderState = db.Column(db.Integer, default=1)
    buyerMessage = db.Column(db.String(255), nullable=False)
    deliveryTimeType = db.Column(db.Integer, nullable=False)
    addressId = db.Column(db.String(36), nullable=False)
    payChannel = db.Column(db.Integer, nullable=False)
    payType = db.Column(db.Integer, nullable=False)
    deliveryId = db.Column(db.Integer, nullable=False)
    isDeleted = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime, default=get_current_utc_time)
    updatedAt = db.Column(db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time)

    def __repr__(self):
        return f"<Order {self.id}>"
