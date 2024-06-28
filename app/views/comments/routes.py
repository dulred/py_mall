from flask import request
from app.model.goods import *
from app.model.address import *
from app.model.goodsType import *
from app.utils.utils import *
from app.views.comments import bp
import os
#商品添加接口
@bp.route("/api/goods/add",methods=["POST"])
def goods_add():
	if request.method == "POST":

		form = request.form
		image = request.files["image"]
		save_path =os.path.join('./static/goods/', getOrderNum() + image.filename)
		image.save(save_path)
		data  = {
			"name":form["name"],
			"goodsType_id":form["goodsType"],
			"originPrice":form["originPrice"],
			"sellPrice":form["sellPrice"],
			"contains":form["contains"],
			"produceTime":form["produceTime"],
			"expireTime":form["expireTime"],
			"createTime":getNowDataTime(),
			"image":save_path,
			"createAddress_id":form["createAddress"],
			"sendAddress_id":form["sendAddress"],
			"intro":form["intro"]
		}
		goods = Goods(**data)
		db.session.add(goods)
		db.session.commit()
		return result(200)

#获取所有商品信息
@bp.route("/api/goods",methods=["POST","GET"])
def goods():
	if request.method == "GET":

		nums = Goods.query.count()
		return result(200,{"nums":nums})

	if request.method == "POST":
		start = request.form["start"]
		nums = request.form["nums"]
		goods = Goods.query.offset(start).limit(nums)
		data = dict()
		data["data"] = []
		for good in goods:
			dic = good.__dict__
			del dic["_sa_instance_state"]
			dic['produceTime']=dic['produceTime'].strftime("%Y-%m-%d")
			dic['expireTime']=dic['expireTime'].strftime("%Y-%m-%d")
			dic['createTime']=dic['createTime'].strftime("%Y-%m-%d")
			dic["goodsType_id"] = GoodsType.query.get(dic["goodsType_id"]).name 
			createAddress = Address.query.get(dic["createAddress_id"])
			dic["createAddress_id"] = createAddress.province+createAddress.town + createAddress.county+createAddress.detail
			sendAddress = Address.query.get(dic["sendAddress_id"])
			dic["sendAddress_id"] = sendAddress.province+sendAddress.town + sendAddress.county+createAddress.detail
			
			data["data"].append(dic)
		return result(200,data)


#商品的删除
@bp.route("/api/goods/delete",methods=["DELETE"])
def goods_delete():
	if request.method=="DELETE":

		_id = request.form["id"]
		Goods.query.filter_by(_id=_id).delete()
		return result(200)

