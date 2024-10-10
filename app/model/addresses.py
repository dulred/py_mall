from . import db
from datetime import datetime
import pytz
def get_current_utc_time():
    return datetime.now()

class Address(db.Model):
    __tablename__ = 'addresses'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.String(36), primary_key=True)
    userId = db.Column(db.Integer, nullable=False)
    receiver = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    provinceCode = db.Column(db.String(100), nullable=False)
    cityCode = db.Column(db.String(100), nullable=False)
    countyCode = db.Column(db.String(100), nullable=False)
    isDefault = db.Column(db.Boolean, default=False)
    isDeleted = db.Column(db.Boolean, default=False)
    createdBy = db.Column(db.String(255), nullable=True)
    updatedBy = db.Column(db.String(255), nullable=True)
    createdAt = db.Column(db.DateTime, default=get_current_utc_time)
    updatedAt = db.Column(db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time)

    def __repr__(self):
        return f"<Address id={self.id}, recipientName={self.recipientName}, city={self.city}>"
