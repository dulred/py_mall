from . import db
import uuid

from datetime import datetime
import pytz
def get_current_utc_time():
    return datetime.now()

class Review(db.Model):
    __tablename__ = 'reviews'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    goodsId = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer,nullable=False)
    rating = db.Column(db.Numeric(3, 2), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    createdAt = db.Column(db.DateTime, default=get_current_utc_time)

    def __repr__(self):
        return f"<Review {self.id}>"
