from . import db
class Receipt(db.Model):

	__tablename__ = "receipt"
	__table_args__ = {'mysql_collate':'utf8_general_ci'}
	_id = db.Column(db.Integer,primary_key=True)
	orderNum = db.Column(db.String(30))
	createTime = db.Column(db.DateTime)
	payValue = db.Column(db.Float(10))
	cutoffValue = db.Column(db.Float(10))
	user_id = db.Column(db.Integer,db.ForeignKey("user._id"))
	itemId = db.Column(db.String(100),default="[]")

	def get_goods_id_list(self):
		idStrList = self.itemId[1:-1].split(',')
		idList = []
		for item in idStrList:
			idList.append(int(item))
		return idList

	def __repr__(self):
		return "Receipt:%s"%self.orderNum
	
class VipReceipt(db.Model): 
	__tablename__ = "vip_receipt"
	__table_args__ = {'mysql_collate':'utf8_general_ci'}
	_id = db.Column(db.Integer,primary_key=True)
	orderNum = db.Column(db.String(30))
	createTime = db.Column(db.DateTime)
	payValue = db.Column(db.Float(10))
	cutoffValue = db.Column(db.Float(10))
	user_id = db.Column(db.Integer,db.ForeignKey("user._id"))
	vipId = db.Column(db.Integer)

	def __repr__(self):
		return "VipReceipt:%s"%self.orderNum

class ReceiptItem(db.Model):

	__tablename__ = "receipt_item"
	__table_args__ = {'mysql_collate':'utf8_general_ci'}
	_id = db.Column(db.Integer,primary_key=True)
	goodsId = db.Column(db.Integer)
	number = db.Column(db.Integer,default=0)
	