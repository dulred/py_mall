from . import db

class Comment(db.Model):

	__tablename__ = "comment"
	__table_args__ = {'mysql_collate':'utf8_general_ci'}
	_id = db.Column(db.Integer,primary_key=True)
	createTime = db.Column(db.DateTime)
	content = db.Column(db.String(500))
	points = db.Column(db.Integer,default=5)
	screenCut = db.Column(db.String(256))
	user = db.Column(db.Integer,db.ForeignKey("user._id"))
	good = db.Column(db.Integer,db.ForeignKey("goods._id"))

	def __repr__(self):
		return "Comment:%s"%self.content