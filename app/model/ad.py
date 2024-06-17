
from . import db

class Ad(db.Model):

	__tablename__ = "ad"
	__table_args__ = {'mysql_collate':'utf8_general_ci'}
	_id = db.Column(db.Integer,primary_key=True)
	content = db.Column(db.String(50))
	createTime = db.Column(db.DateTime)
	displayTime = db.Column(db.DateTime)
	endTime = db.Column(db.DateTime)
	image = db.Column(db.String(256))
	video = db.Column(db.String(256))
	title = db.Column(db.String(100))
	intro = db.Column(db.String(500))

	def __repr__(self):
		return "Ad:%s"%self.content 