from . import db
from datetime import datetime
import pytz
def get_current_utc_time():
    return datetime.now()
class GoodsStyle(db.Model):
    __tablename__ = 'goods_styles'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goods_id = db.Column(db.Integer, nullable=True)
    style_key = db.Column(db.String(50), nullable=True)  # e.g., 'style_type'
    style_value = db.Column(db.String(100), nullable=True)  # e.g., 'New Chinese'
    isDeleted = db.Column(db.Boolean, default=False)
    createdBy = db.Column(db.String(255), nullable=True)
    updatedBy = db.Column(db.String(255), nullable=True)
    createdAt = db.Column(db.DateTime, default=get_current_utc_time)
    updatedAt = db.Column(db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time)