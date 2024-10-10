from . import db
from datetime import datetime
import pytz
def get_current_utc_time():
    return datetime.now()
class Supplier(db.Model):
    __tablename__ = 'suppliers'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    contactInfo = db.Column(db.Text, nullable=True)
    isDeleted = db.Column(db.Boolean, default=False)
    createdBy = db.Column(db.String(255), nullable=True)
    updatedBy = db.Column(db.String(255), nullable=True)
    createdAt = db.Column(db.DateTime, default=get_current_utc_time)
    updatedAt = db.Column(db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time)
    def __repr__(self):
        return f"<Supplier {self.name}>"
