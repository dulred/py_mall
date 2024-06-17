# models/user.py

from . import db

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    account = db.Column(db.String(11), unique=True)
    password = db.Column(db.String(64))
    avatar = db.Column(db.String(256))
    age = db.Column(db.Integer)
    idCard = db.Column(db.String(18))
    gneder = db.Column(db.String(2))
    createTime = db.Column(db.DateTime)
    loginTime = db.Column(db.DateTime)
    logoutTime = db.Column(db.DateTime)
    balance = db.Column(db.Float(10), default=0)

    vip = db.Column(db.Integer, db.ForeignKey("vip._id"))

    def __repr__(self):
        return "User:%s" % self.name
