from . import db
class Goods(db.Model):

	__tablename__ = "goods"
	__table_args__ = {'mysql_collate':'utf8_general_ci'}
	_id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(100))
	goodsType_id = db.Column(db.Integer,db.ForeignKey("goodsType._id"))
	originPrice = db.Column(db.Float(10))
	sellPrice = db.Column(db.Float(10))
	contains = db.Column(db.Integer,default=0)
	produceTime = db.Column(db.DateTime)
	expireTime = db.Column(db.DateTime)
	createTime = db.Column(db.DateTime)
	image = db.Column(db.String(256))
	createAddress_id = db.Column(db.Integer,db.ForeignKey("address._id"))
	sendAddress_id = db.Column(db.Integer,db.ForeignKey("address._id"))
	intro = db.Column(db.String(500))
	lookTimes = db.Column(db.Integer,default=0)
	buyTimes = db.Column(db.Integer,default=0)
	likeTimes = db.Column(db.Integer,default=0)

	def __repr__(self):
		return "Goods:%s"%self.name