from . import db
class GoodsType(db.Model):

	__tablename__ = "goodsType"
	__table_args__ = {'mysql_collate':'utf8_general_ci'}
	_id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(50))
	number = db.Column(db.Integer,default=0)

	def __repr__(self):
		return "GoodsType:%s"%self.name