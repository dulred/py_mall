import traceback
from flask import request,session
from app.model.goods import *
from app.model.address import *
from app.model.goodsType import *
from app.model.user import *
from app.model.receipt import *
from app.model.court import *
from app.utils.utils import *
from app.views.orders import bp

#购买商品生成订单
#ps ItemReceipt不能被删除
@bp.route("/api/buy/goods",methods=["POST"])
def buy_goods():
	if request.method == "POST":
		sId = session.get("_id",None)
		form = request.form
		user = User.query.get(sId)
		if user.balance < form["payValue"]:
			return result(204,{"info":"余额不足"})
		user.balance = user.balance - form["payValue"]
		goodsList = request.form["goodsList"]
		itemIdList = [] 
		itemCount = ReceiptItem.query.count()
		#购物车清空
		court = Court.query.filter_by(user_id=sId).first()
		try:
			for goods in goodsList:
				item = ReceiptItem(goodsId=goods["id"],number=goods["number"])
				db.session.add(item)
				goods = Goods.query.get(goods["id"])
				court.goods.remove(goods)
				goods.buyTimes = goods.buyTimes + 1
				goods.contains = goods.contains - 1
				itemCount = itemCount + 1
				itemIdList.append(itemCount)
			data = {
				"orderNum":getOrderNum(),
				"createTime":getNowDataTime(),
				"payValue":form["payValue"],
				"cutoffValue":form["cutoffValue"],
				"user_id":sId,
				"itemId":str(itemIdList)
			}
			receipt = Receipt(**data)
			db.session.add(receipt)
			db.session.commit()
			return result(200)
		except:
			traceback.print_exc()
			return result(502,{"info":"服务器错误"})

#查看个人商品订单情况
@bp.route("/api/self/receipt")
def self_receipt():
	if request.method == "GET":
		sId = session['_id']
		receipts = Receipt.query.filter_by(user_id=sId)
		data = dict()
		data["data"] = []
		try:
			for receipt in receipts:
				goodsIdList = receipt.get_goods_id_list()
				dic = receipt.__dict__
				del dic["_sa_instance_state"]
				dic["createTime"] = dic["createTime"].strftime("%Y-%m-%d")
				dic["goodsList"] = []
				for goodsId in goodsIdList:
					goods = Goods.query.get(goodsId)
					d = {
						"name":goods.name,
						"originPrice":goods.originPrice,
						"sellPrice":goods.sellPrice
					}
					print("="*30)
					print(d)
					print("="*30)
					dic["goodsList"].append(d)
				data["data"].append(dic)
			return result(200,data)
		except:
			traceback.print_exc()
			return result(502,{"info":"服务端错误"})

#查看所有人VIP订单订单情况
@bp.route("/api/admin/vipreceipt/<int:start>/<int:nums>",methods=["POST","GET"])
def admin_vipreceipt(start,nums):
	if request.method == "GET":

		nums = VipReceipt.query.all().count()
		return result(200,{"nums":nums})

	if request.method == "POST":

		receipts = VipReceipt.query.offset(start).limit(nums)
		data = dict()
		data["data"] = []
		for receipt in receipts:
			dic = receipt.__dict__
			del dic["_sa_instance_state"]
			data["data"].append(dic)
		return result(200,data)



#查看所有人商品订单订单情况
@bp.route("/api/admin/receipt/<int:start>/<int:nums>",methods=["POST","GET"])
def admin_receipt(start,nums):
	if request.method == "GET":

		nums = Receipt.query.all().count()
		return result(200,{"nums":nums})

	if request.method == "POST":

		receipts = Receipt.query.offset(start).limit(nums)
		data = dict()
		data["data"] = []
		for receipt in receipts:
			goodsIdList = receipt.get_goods_id_list()
			dic = receipt.__dict__
			del dic["_sa_instance_state"]
			dic["goodsList"] = []
			for goodsId in goodsIdList:
				goods = Goods.query.with_entities(Goods.name,Goods.originPrice,Goods.sellPrice).filter_by(_id=goodsId)
				d = goods.__dict__
				del d["_sa_instance_state"]
				dic["goodsList"].append(d)
			data["data"].append(dic)
		return result(200,data)