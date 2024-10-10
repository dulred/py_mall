from . import db
from datetime import datetime
import pytz
def get_current_utc_time():
    return datetime.now()
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    categoryName = db.Column(db.String(255), nullable=False)         # 分类名称
    categoryLevel = db.Column(db.Integer, nullable=False)             # 分类层级
    parentId = db.Column(db.Integer, default=0)  # 父分类ID
    categoryRank = db.Column(db.Integer, default=0)                   # 排序值
    isDeleted = db.Column(db.Boolean, default=False)
    createdBy = db.Column(db.String(255), nullable=True)
    updatedBy = db.Column(db.String(255), nullable=True)
    createdAt = db.Column(db.DateTime, default=get_current_utc_time)
    updatedAt = db.Column(db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time)
