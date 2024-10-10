from . import db
from datetime import datetime
import pytz
def get_current_utc_time():
    return datetime.now()
class Goods(db.Model):
    __tablename__ = 'goods'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    rank = db.Column(db.Integer,default=100)
    pictureUrl = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(5, 2), nullable=True)
    orderNum = db.Column(db.Integer, default=0)
    categoryId = db.Column(db.Integer, nullable=False)
    brandId = db.Column(db.Integer, nullable=True)
    listedAt = db.Column(db.DateTime, nullable=True)
    isDiscontinued = db.Column(db.Boolean, default=False)
    supplierId = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Numeric(3, 2), default=5.0)
    merchantTime = db.Column(db.DateTime, nullable=True)
    isDeleted = db.Column(db.Boolean, default=False)
    createdBy = db.Column(db.String(255), nullable=True)
    updatedBy = db.Column(db.String(255), nullable=True)
    createdAt = db.Column(db.DateTime, default=get_current_utc_time)
    updatedAt = db.Column(db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time)

    def __repr__(self):
        return f"<Goods {self.name}>"