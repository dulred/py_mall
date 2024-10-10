from . import db
from datetime import datetime
import pytz
def get_current_utc_time():
    return datetime.now()

class Return(db.Model):
    __tablename__ = 'returns'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderId = db.Column(db.Integer, nullable=False)
    returnDate = db.Column(db.DateTime, default=get_current_utc_time)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # e.g., 'pending', 'approved', 'rejected'
    createdBy = db.Column(db.String(255), nullable=True)
    updatedBy = db.Column(db.String(255), nullable=True)
    createdAt = db.Column(db.DateTime, default=get_current_utc_time)
    updatedAt = db.Column(db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time)

    def __repr__(self):
        return f"<Return {self.id}>"
