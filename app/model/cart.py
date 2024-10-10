from . import db
from datetime import datetime
import pytz
def get_current_utc_time():
    return datetime.now()

class Cart(db.Model):
    __tablename__ = 'carts'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=get_current_utc_time)

    def __repr__(self):
        return f"<Cart {self.id}>"
