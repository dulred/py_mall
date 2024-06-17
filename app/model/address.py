from . import db

class Address(db.Model):

	__tablename__ = "address"
	__table_args__ = {'mysql_collate':'utf8_general_ci'}
	_id = db.Column(db.Integer,primary_key=True)
	province = db.Column(db.String(18))
	town = db.Column(db.String(18))
	county = db.Column(db.String(18))
	detail = db.Column(db.String(200))
	user_id = db.Column(db.Integer,db.ForeignKey("user._id"))

	def __repr__(self):
		return "Address:%s"%self.detail