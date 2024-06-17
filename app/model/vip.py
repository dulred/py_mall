from . import db
class Vip(db.Model):

	__tablename__ = "vip"
	__table_args__ = {'mysql_collate':'utf8_general_ci'}
	_id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(50))
	level = db.Column(db.Integer,default=0)

	def __repr__(self):
		return "Vip:%s"%self.name 