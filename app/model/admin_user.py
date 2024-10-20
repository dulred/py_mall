# models/user.py

import uuid
from . import db
from datetime import datetime
import pytz
def get_current_utc_time():
    return datetime.now()
class AdminUser(db.Model):
    __tablename__ = 'admin_user'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    # id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_type = db.Column(db.String(50),default="admin")
    nickname = db.Column(db.String(50),default="未命名")
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(64))
    roleId = db.Column(db.Integer)
    mobile = db.Column(db.String(15), unique=True)
    avatar = db.Column(db.String(256))
    gender = db.Column(db.String(2))
    birthday = db.Column(db.Date)
    provinceCode = db.Column(db.Integer)
    cityCode = db.Column(db.Integer)
    countyCode = db.Column(db.Integer)
    remark = db.Column(db.String(255))
    loginTime = db.Column(db.DateTime)
    logoutTime = db.Column(db.DateTime)
    isActive = db.Column(db.Boolean, default=True)
    isDeleted = db.Column(db.Boolean, default=False)
    createdBy = db.Column(db.String(255), nullable=True)
    updatedBy = db.Column(db.String(255), nullable=True)
    createdAt = db.Column(db.DateTime, default=get_current_utc_time)
    updatedAt = db.Column(db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time)

    def __repr__(self):
        return "User:%s" % self.name

