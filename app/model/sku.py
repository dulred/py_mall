from . import db
from datetime import datetime
import pytz
def get_current_utc_time():
    return datetime.now()

class Sku(db.Model):
    __tablename__ = 'sku'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goodsId = db.Column(db.Integer, nullable=False)
    inventory = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    picture = db.Column(db.String(255), nullable=False)
    specs = db.Column(db.String(255), nullable=False)
    isDeleted = db.Column(db.Boolean, default=False)
    createdBy = db.Column(db.String(255), nullable=True)
    updatedBy = db.Column(db.String(255), nullable=True)
    createdAt = db.Column(db.DateTime, default=get_current_utc_time)
    updatedAt = db.Column(db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time)