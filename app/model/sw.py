from . import db
from datetime import datetime
import pytz
def get_current_utc_time():
    return datetime.now()
class SW(db.Model):
    __tablename__ = 'sw'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pictureUrl = db.Column(db.String(255), nullable=False)
    imgType = db.Column(db.Boolean, default=False)  # 0 为首图， 1 为尾图   (尺寸比例 和 size大小有限制 以及格式)
    isSelected = db.Column(db.Boolean, default=False) # 是否为选中的图
    isDeleted = db.Column(db.Boolean, default=False)
    createdBy = db.Column(db.String(255), nullable=True)
    updatedBy = db.Column(db.String(255), nullable=True)
    createdAt = db.Column(db.DateTime, default=get_current_utc_time)
    updatedAt = db.Column(db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time)

    def __repr__(self):
        return f"<Home {self.id}>"
