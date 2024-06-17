from . import db
goodsCourt = db.Table("goodsCourt",
	db.Column("goods_id",db.Integer,db.ForeignKey("goods._id")),
	db.Column("court_id",db.Integer,db.ForeignKey("court._id"))
	)