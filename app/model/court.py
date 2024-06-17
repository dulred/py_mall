from . import db
from .common import goodsCourt
class Court(db.Model):

	__tablename__ = "court"
	__table_args__ = {'mysql_collate':'utf8_general_ci'}
	_id = db.Column(db.Integer,primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user._id'))
	number = db.Column(db.Integer,default=0)#记录商品种类
	goods = db.relationship("Goods",secondary=goodsCourt,backref=db.backref("court",lazy="dynamic"),lazy="dynamic")