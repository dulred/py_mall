from flask import request
from app.model.goods import *
from app.model.address import *
from app.model.goodsType import *
from app.utils.utils import *
from app.views.goods import bp
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

#根据分类获取商品信息 分页
@bp.route("/api/by/tag/goods",methods=["POST"])
def by_tag_goods():
	if request.method == "POST":
		tagId = request.form["tagId"]
		goods = Goods.query.filter_by(goodsType_id=tagId)
		data = dict()
		data["data"] = []
		for good in goods:
			data["data"].append({
				"id":good._id,
				"name":good.name,
				"originPrice":good.originPrice,
				"sellPrice":good.sellPrice,
				"image":good.image,
				"intro":good.intro
				})
		return result(200,data)


#用户搜索商品信息 最多返回50条
@bp.route("/api/goods/search",methods=["POST"])
def goods_search():
	if request.method=="POST":
		keyWord = request.form["keyWord"]
		goods = Goods.query.filter_by(Goods.name.contains(keyWord)).limit(50)
		data = dict()
		data["data"] = []
		for good in goods:
			data["data"].append({
				"id":good._id,
				"name":good.name,
				"originPrice":good.originPrice,
				"sellPrice":good.sellPrice,
				"image":good.image,
				"lookTimes":good.lookTimes,
				"likeTimes":good.likeTimes,
				"buyTimes":good.buyTimes,
				})
		return result(200,data)
#热销的商品推荐 buyTimes 推荐
@bp.route("/api/goods/recommend/buytimes")
def goods_recommend_buytime():
	if request.method=="GET":
		goods = Goods.query.order_by(db.desc(Goods.buyTimes)).limit(50)
		data = dict()
		data["data"] = []
		for good in goods:
			data["data"].append({
				"id":good._id,
				"name":good.name,
				"originPrice":good.originPrice,
				"sellPrice":good.sellPrice,
				"image":good.image,
				"lookTimes":good.lookTimes,
				"likeTimes":good.likeTimes,
				"buyTimes":good.buyTimes,
				})
		return result(200,data)
#添加购物车多的商品 likeTimes 推荐
@bp.route("/api/goods/recommend/liketimes")
def goods_recommend_liketimes():
	if request.method=="GET":
		goods = Goods.query.order_by(db.desc(Goods.likeTimes)).limit(50)
		data = dict()
		data["data"] = []
		for good in goods:
			data["data"].append({
				"id":good._id,
				"name":good.name,
				"originPrice":good.originPrice,
				"sellPrice":good.sellPrice,
				"image":good.image,
				"lookTimes":good.lookTimes,
				"likeTimes":good.likeTimes,
				"buyTimes":good.buyTimes,
				})
		return result(200,data)
	
#获取商品的详细信息 更新 lookTimes 浏览次数
@bp.route("/api/goods/detail/<int:goodsId>")
def goods_detail(goodsId):
	if request.method=="GET":
		goods = Goods.query.get(goodsId)
		goods.lookTimes = goods.lookTimes + 1
		db.session.commit()
		goods = Goods.query.get(goodsId)
		data= goods.__dict__
		del data["_sa_instance_state"]
		data['produceTime']=data['produceTime'].strftime("%Y-%m-%d")
		data['expireTime']=data['expireTime'].strftime("%Y-%m-%d")
		data['createTime']=data['createTime'].strftime("%Y-%m-%d")
		data["goodsType_id"] = GoodsType.query.get(data["goodsType_id"]).name 
		createAddress = Address.query.get(data["createAddress_id"])
		data["createAddress_id"] = createAddress.province+createAddress.town + createAddress.county+createAddress.detail
		sendAddress = Address.query.get(data["sendAddress_id"])
		data["sendAddress_id"] = sendAddress.province+sendAddress.town + sendAddress.county+createAddress.detail
			
		return result(200,data)
