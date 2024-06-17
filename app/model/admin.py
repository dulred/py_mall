
from . import db

class Admin(db.Model):

	__tablename__ = "admin"
	__table_args__ = {'mysql_collate':'utf8_general_ci'}
	_id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(30))
	account = db.Column(db.String(11))
	password = db.Column(db.String(64))
	createTime = db.Column(db.DateTime)
	loginTime = db.Column(db.DateTime)
	logoutTime = db.Column(db.DateTime)
	level = db.Column(db.Integer,default=0)

	def __repr__(self):
		return "Admin:%s"%self.name 