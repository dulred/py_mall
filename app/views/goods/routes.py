import math
import shutil
from flask import request
from app.model.detail_img import Deatil_img
from app.model.goods import *
from app.model.addresses import *
from app.model.goodsStyle import GoodsStyle
from app.model.goodsTags import *
from app.model.goods_config import Goods_config
from app.model.sku import Sku
from app.model.specs import Specs
from app.model.thumb_img import Thumb_img
from app.utils.utils import *
from app.views.goods import bp
from config import GOODS_MAIN_TMP_FOLDER_URL,GOODS_MAIN_FOLDER_URL,GOODS_MAIN_HTTP_URL
import os
import threading
from sqlalchemy import desc
from datetime import datetime
import pytz


#商品添加接口
@bp.route("/api/goods",methods=["POST"])
def goods_add():
	if request.method == "POST":
		try:
			form = request.get_json()
			# 移动文件，并替换入库的图片路径为实际路径
			file_path = form.get("pictureUrl")
			threading.Thread(target=moveFile, args=(file_path,GOODS_MAIN_TMP_FOLDER_URL,GOODS_MAIN_FOLDER_URL)).start()

			# 入库数据的准备
			data  = {
				"categoryId": form['categoryId'],
				"rank":form["rank"],
				"name":form["name"],
				"description":form["description"],
				"price":form["price"],
				"discount":form["discount"],
				"brandId":form["brandId"],
				"supplierId":form["supplierId"],
				"isDiscontinued":form["isDiscontinued"],
				"pictureUrl": f"{GOODS_MAIN_HTTP_URL}{os.path.basename(file_path)}",
			}

			if form['isDiscontinued'] == 0:
				data["listedAt"] = datetime.now()

			goods = Goods(**data)

			try:
				db.session.add(goods)
				db.session.commit()
			except Exception as e:
				return result(200,str(e))
			
			return result(200,"add goods success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")



#添加商品配置
@bp.route("/api/goods/config",methods=["POST"])
def goods_config_add():
	if request.method == "POST":
		try:
			data = request.get_json()
			_data = {
				"config_type":data.get("config_type"),
				"config_value":data.get("config_value")
			}
			goods_config = Goods_config(**_data)

			try:
				db.session.add(goods_config)
				db.session.commit()
				return result(200,"add goodsConfig success")
			except Exception as e:
				return result(200,str(e))
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")


#修改商品配置
@bp.route("/api/goods/config",methods=["PUT"])
def goods_config_update():
	if request.method == "PUT":
		try:
			data = request.get_json()
			goods_config = db.session.query(Goods_config).filter_by(config_type=data.get('config_type'),isDeleted = 0).first()
			goods_config.config_value = data.get('config_value')
			try:
				db.session.commit()
				return result(200,"update goodsConfig success")
			except Exception as e:
				return result(200,str(e))
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use PUT method")

#商品修改接口
@bp.route("/api/goods",methods=["PUT"])
def goods_update():
	if request.method == "PUT":
		try:
			
			data =  request.get_json()
			_id = data.get("id")
			_name = data.get('name')
			_categoryId = data.get('categoryId')
			_price = data.get('price')
			_pictureUrl = data.get('pictureUrl')
			_brandId = data.get('brandId')
			_supplierId = data.get('supplierId')
			_isDiscontinued = data.get('isDiscontinued')
			_rank = data.get('rank')
			_discount = data.get('discount')
			_description = data.get('description')

			goods = db.session.query(Goods).filter_by(id=_id).first()
			goods.name = _name
			goods.categoryId = _categoryId
			goods.price = _price
			goods.pictureUrl = _pictureUrl
			goods.brandId = _brandId
			goods.supplierId = _supplierId
			goods.isDiscontinued = _isDiscontinued
			goods.rank = _rank
			goods.discount = _discount
			goods.description = _description

			db.session.commit()
			
			return result(200,"update goods success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use PUT method")



#商品删除接口
@bp.route("/api/goods/<id>",methods=["DELETE"])
def goods_delete(id):
	if request.method == "DELETE":
		try:
			goods = db.session.query(Goods).filter_by(id=id,isDeleted = 0).first()
			goods.isDeleted = True
			db.session.commit()
			
			return result(200,"delete goods success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use DELETE method")



#分页获取所有商品信息
@bp.route("/api/goods/all",methods=["POST"])
def goods_all():
	if request.method == "POST":
		try:
			data = request.get_json()
			page = data.get('page')
			pageSize = data.get('pageSize')
			# 计算偏移量
			offset = (page - 1) * pageSize
			total_count = db.session.query(Goods).filter_by(isDeleted = 0).count()
			goods_list =  db.session.query(Goods).filter_by(isDeleted = 0).offset(offset).limit(pageSize).all()
			item_list = [{'id':item.id,'description':item.description,'name':item.name,'price':item.price,'discount':item.discount,'pictureUrl': item.pictureUrl,'rank':item.rank,'categoryId':item.categoryId,"brandId":item.brandId,"supplierId":item.supplierId,"rating":item.rating,"isDiscontinued":item.isDiscontinued,"listedAt":gmt_to_Shanghai(item.listedAt)} for item in goods_list]
			list_result = {
				"total": total_count,
				"pages": math.ceil(total_count / pageSize),
				"page": page,
				"pageSize": pageSize,
				"items": item_list,
			}
			return result(200,"查询成功",list_result)
		except Exception as e:
			return result(400,str(e))
	return result(400,"please use POST method")


#分页获取所有商品信息
@bp.route("/api/goods/<id>",methods=["GET"])
def goods_byId(id):
	if request.method == "GET":
		try:
			goods =  db.session.query(Goods).filter_by(id=id).first()
			goods_result = {
				'id':goods.id,
				'description':goods.description,
				'name':goods.name,
				'price':goods.price,
				'discount':goods.discount,
				'pictureUrl': goods.pictureUrl,
				'rank':goods.rank,
				'categoryId':goods.categoryId,
				"brandId":goods.brandId,
				"supplierId":goods.supplierId,
				"rating":goods.rating,
				"isDiscontinued":goods.isDiscontinued,
				"listedAt":gmt_to_Shanghai(goods.listedAt)
			}
			return result(200,"查询成功",goods_result)
		except Exception as e:
			return result(400,str(e))

	return result(400,"please use GET method")

#获取指定分类下的商品
@bp.route("/api/goods/categoryType/<id>",methods=["GET"])
def goods_byType(id):
	if request.method == "GET":
		try:
			goods =  db.session.query(Goods).filter_by(categoryId=id).all()
			goods_list = [{
				'id':item.id,
				'description':item.description,
				'name':item.name,
				'price':item.price,
				'discount':item.discount,
				'pictureUrl': item.pictureUrl,
				'rank':item.rank,
				'categoryId':item.categoryId,
				"brandId":item.brandId,
				"supplierId":item.supplierId,
				"rating":item.rating,
				"isDiscontinued":item.isDiscontinued,
				"listedAt":gmt_to_Shanghai(item.listedAt)
			} for item in goods]
			return result(200,"查询成功",goods_list)
		except Exception as e:
			return result(400,str(e))

	return result(400,"please use GET method")


# 新品速览
@bp.route("/api/ntk/goods/new",methods=["GET"])
def newGoods():
	if request.method == "GET":
		try:
			goods_config = db.session.query(Goods_config).filter_by(config_type = 0,isDeleted = 0).first()
			goods_config_value = goods_config.config_value.split(',')  # 按逗号分割
			goods_list = {"items":[],"ids":[]}
			for item in goods_config_value:
				good =  db.session.query(Goods).filter_by(id = item,isDeleted = 0 ).first()
				goods_obj  = {'id':good.id,'description':good.description,'name':good.name,'price':good.price,'discount':good.discount,'pictureUrl': good.pictureUrl,'orderNum':good.orderNum}
				goods_list["items"].append(goods_obj)
				goods_list["ids"].append(good.id)
			
			return result(200,"get new goods success",goods_list)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")


# 精品推荐
@bp.route("/api/ntk/goods/jinpin",methods=["GET"])
def jinpin():
	if request.method == "GET":
		try:
			goods_config = db.session.query(Goods_config).filter_by(config_type = 1,isDeleted = 0).first()
			goods_config_value = goods_config.config_value.split(',')  # 按逗号分割
			goods_list = {"items":[],"ids":[]}
			for item in goods_config_value:
				good =  db.session.query(Goods).filter_by(id = item,isDeleted = 0 ).first()
				goods_obj  = {'id':good.id,'description':good.description,'name':good.name,'price':good.price,'discount':good.discount,'pictureUrl': good.pictureUrl,'orderNum':good.orderNum}
				goods_list["items"].append(goods_obj)
				goods_list["ids"].append(good.id)
			
			return result(200,"get new goods success",goods_list)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")



# 人气TOP排行榜 
@bp.route("/api/ntk/goods/top",methods=["GET"])
def top():
	if request.method == "GET":
		try:
			goods_config = db.session.query(Goods_config).filter_by(config_type = 2,isDeleted = 0).first()
			goods_config_value = goods_config.config_value.split(',')  # 按逗号分割
			goods_list = {"items":[],"ids":[]}
			for item in goods_config_value:
				good =  db.session.query(Goods).filter_by(id = item,isDeleted = 0 ).first()
				goods_obj  = {'id':good.id,'description':good.description,'name':good.name,'price':good.price,'discount':good.discount,'pictureUrl': good.pictureUrl,'orderNum':good.orderNum}
				goods_list["items"].append(goods_obj)
				goods_list["ids"].append(good.id)
			
			return result(200,"get new goods success",goods_list)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")


# 更多精选商品 
@bp.route("/api/ntk/goods/guessLike",methods=["GET"])
def guessLikes():
	if request.method == "GET":
		try:
			page = request.args.get('page',type=int)
			pageSize = request.args.get('pageSize',type=int)
			# 计算偏移量
			offset = (page - 1) * pageSize
			total_count = db.session.query(Goods).count()
			goods_list =  db.session.query(Goods).order_by(desc(Goods.rank)).offset(offset).limit(pageSize).all()
			item_list = [{'id':item.id,'description':item.description,'name':item.name,'price':item.price,'discount':item.price,'pictureUrl': item.pictureUrl,'orderNum':item.orderNum} for item in goods_list]
			list_result = {
				"counts": total_count,
				"items": item_list,         
				"page": page,
				"pageSize": pageSize,
				"pages": math.ceil(total_count / pageSize)  # 向上取整
			}
			
			return result(200,"get guessLike goods success",list_result)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")



# 同类商品 （按照类别查询）
@bp.route("/api/ntk/goods/similar",methods=["GET"])
def similar():
	if request.method == "GET":
		try:
			page = request.args.get('page',type=int)
			pageSize = request.args.get('pageSize',type=int)
			# 计算偏移量
			offset = (page - 1) * pageSize
			total_count = db.session.query(Goods).count()
			goods_list =  db.session.query(Goods).order_by(desc(Goods.rank)).offset(offset).limit(pageSize).all()
			item_list = [{'id':item.id,'description':item.description,'name':item.name,'price':item.price,'discount':item.price,'pictureUrl': item.pictureUrl,'orderNum':item.orderNum} for item in goods_list]
			list_result = {
				"counts": total_count,
				"items": item_list,         
				"page": page,
				"pageSize": pageSize,
				"pages": math.ceil(total_count / pageSize)  # 向上取整
			}
			
			return result(200,"get similar goods success",list_result)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")

# 按照标签查询 


# 按照名称查询
 

# 搜索商品 
@bp.route("/api/ntk/goods/search",methods=["POST"])
def searchGood():
	if request.method == "POST":
		try:
			data = request.get_json()
			page = data['page']
			pageSize = data['pageSize']
			val = data['val']
			# 计算偏移量
			offset = (page - 1) * pageSize
			total_count = db.session.query(Goods).count()
			goods_list =  db.session.query(Goods).order_by(desc(Goods.rank)).offset(offset).limit(pageSize).all()
			item_list = [{'id':item.id,'description':item.description,'name':item.name,'price':item.price,'discount':item.price,'pictureUrl': item.pictureUrl,'orderNum':item.orderNum} for item in goods_list]
			list_result = {
				"counts": total_count,
				"items": item_list,         
				"page": page,
				"pageSize": pageSize,
				"pages": math.ceil(total_count / pageSize)  # 向上取整
			}
			
			return result(200,"serach goods success",list_result)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")


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
