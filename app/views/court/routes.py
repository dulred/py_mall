from flask import request
from app.model.goods import *
from app.model.address import *
from app.model.goodsType import *
from app.utils.utils import *
from app.views.comments import bp
import os

#获取自己购物车和商品信息
@bp.route("/api/self/court")
def self_court():
	if request.method == "GET":
		sId = session.get("_id")
		court = Court.query.filter_by(user_id=sId).first()
		if court.number == 0:
			return result(200,{"goods":[]})
		goods = court.goods.all()
		data = dict()
		data["data"] = []
		for good in goods:
			dic = good.__dict__
			data["data"].append({
				"_id":good._id,
				"name":good.name,
				"originPrice":good.originPrice,
				"sellPrice":good.sellPrice,
				"image":good.image,
				"lookTimes":good.lookTimes,
				"likeTimes":good.likeTimes,
				"buyTimes":good.buyTimes,
				})

		return result(200,data)

#添加商品到购物车
@bp.route("/api/add/goods/2/court",methods=["POST"])
def add_goods_2_court():
	if request.method == "POST":
		goodsId = request.form["goodsId"]
		sId = session["_id"]
		court = Court.query.filter_by(user_id=sId).first()
		court.number = court.number + 1
		goods = Goods.query.get(goodsId)
		goods.likeTimes = goods.likeTimes + 1
		court.goods.append(goods)
		db.session.commit()
		return result(200)

#移除购物车商品信息
@bp.route("/api/remove/goods/from/court",methods=["POST"])
def remove_goods_from_court():
	if request.method == "POST":
		goodsId = request.form["goodsId"]
		sId = session["_id"]
		court = Court.query.filter_by(user_id=sId).first()
		goods = Goods.query.get(goodsId)
		if goods.likeTimes > 0:
			goods.likeTimes = goods.likeTimes - 1
		court.goods.remove(goods)
		db.session.commit()
		return result()