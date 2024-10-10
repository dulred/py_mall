from . import db
from datetime import datetime

def get_current_utc_time():
    return datetime.now()
class Goods_config(db.Model):
    __tablename__ = 'goods_config'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    config_type = db.Column(db.Integer,nullable=False,comment="0->新品速览,1->精品推荐,2->人气Top") 
    config_value = db.Column(db.String(255), nullable=False,comment="goodsId集合例如-> 1,2,3 ")
    isDeleted = db.Column(db.Boolean, default=False)
    createdBy = db.Column(db.String(255), nullable=True)
    updatedBy = db.Column(db.String(255), nullable=True)
    createdAt = db.Column(db.DateTime, default=get_current_utc_time)
    updatedAt = db.Column(db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time)

    def __repr__(self):
        return f"<Goods {self.name}>"