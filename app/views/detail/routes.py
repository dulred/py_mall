from flask import g, json, request
import os

from sqlalchemy import desc
from app.model.addresses import Address
from app.model.goods import Goods
from app.model.goodsStyle import GoodsStyle
from app.model.sku import Sku
from app.model.specs import Specs
from app.model.thumb_img import Thumb_img
from app.views.detail import bp
from app.model.detail_img import *
from config import GOODS_DETAIL_FOLDER_URL,GOODS_DETAIL_TMP_FOLDER_URL,GOODS_DETAIL_HTTP_URL
from app.utils.utils import *
import threading

#详情页图片添加接口
@bp.route("/api/detail",methods=["POST"])
def detail_add():
	if request.method == "POST":
		try:
			form = request.get_json()
			# 移动文件，并替换入库的图片路径为实际路径
			file_path = form["pictureUrl"]
			threading.Thread(target=moveFile, args=(file_path,GOODS_DETAIL_TMP_FOLDER_URL,GOODS_DETAIL_FOLDER_URL)).start()

			# 入库数据的准备
			data  = {
				"pictureUrl": f"{GOODS_DETAIL_HTTP_URL}{os.path.basename(file_path)}",
				"goodsId": form['goodsId'],
				"rank":form["rank"]
			}
			detail_img = Deatil_img(**data)
			try:
				db.session.add(detail_img)
				db.session.commit()
			except Exception as e:  
				return result(200,str(e))
			
			return result(200,"add detail_img success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")


#详情页返回数据接口
@bp.route("/api/ntk/detail",methods=["GET"])
def detail_page():
	if request.method == "GET":
		try:
			
			id = request.args.get("id")	
			goods_list = db.session.query(Goods).filter_by(id=id).first()
			goodsResult = {
				"id":id,
				"name":goods_list.name,
				"description":goods_list.description,
				"price":goods_list.price,
				"details":{
					"pictures":[],
					"properties":[]
				},
				"mainPictures":[],
				"similarProducts":[],
				"skus":[],
				"specs":[]
			}

			# 查询thumb图
			thumb = db.session.query(Thumb_img).filter_by(goodsId=id,isDeleted = 0).order_by(desc(Thumb_img.rank)).all()
			thumb_list = [{'pictureUrl':item.pictureUrl} for item in thumb]
			for thumb in thumb_list:
				goodsResult["mainPictures"].append(thumb["pictureUrl"])
			# 查询详细页图
			detail = db.session.query(Deatil_img).filter_by(goodsId=id,isDeleted = 0).order_by(desc(Deatil_img.rank)).all()
			detail_list = [{'pictureUrl':item.pictureUrl} for item in detail]
			for detail in detail_list:
				goodsResult["details"]["pictures"].append(detail["pictureUrl"])

			# 查询属性值图
			goodsStyle = db.session.query(GoodsStyle).filter_by(goods_id=id,isDeleted = 0).all()
			goodsStyle_list = [{"name":item.style_key,"value":item.style_value} for item in goodsStyle]
			for goodsStyle in goodsStyle_list:
				goodsResult["details"]["properties"].append(goodsStyle)

			# 同类商品
			similar = db.session.query(Goods).order_by(desc(Goods.rank)).limit(4).all()
			similar_list = [{'id':item.id,'description':item.description,'name':item.name,'price':item.price,'discount':item.price,'pictureUrl': item.pictureUrl,'orderNum':item.orderNum} for item in similar]
			for item in similar_list:
				goodsResult["similarProducts"].append(item)

			# sku
			sku = db.session.query(Sku).filter_by(goodsId = id).all()
			sku_list = [{"id":item.id,"picture":item.picture,"inventory":item.inventory,"price":item.price,"specs":item.specs} for item in sku]
			for item in sku_list:
				item["specs"] = json.loads(item["specs"])
			goodsResult["skus"] = sku_list
			# specs
			specs = db.session.query(Specs).filter_by(goodsId=id).all()
			specs_list = [{"id":item.id,"name":item.name,"values":item.values,"rank":item.rank} for item in specs]
			for item in specs_list:
				data = {"name":item["name"],"values":[]}
				for value in item["values"].split(","):
					data["values"].append({"name":value})
				goodsResult["specs"].append(data)

			return result(200,"select detail_page success",goodsResult)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")



#分页获取分类下商品以及detail信息
@bp.route("/api/goods/detail",methods=["POST"])
def goods_spec():
	if request.method == "POST":
		try:
			json_data = request.get_json()
			_page = json_data.get('page')
			_pageSize = json_data.get('pageSize')
			offset = (_page - 1) * _pageSize
			_goods_count = db.session.query(Goods).filter_by(categoryId = json_data.get("categoryId"),isDeleted = 0).count()
			_goods = db.session.query(Goods).filter_by(categoryId = json_data.get("categoryId"),isDeleted = 0).offset(offset).limit(_pageSize).all()
			item_list = [{"id":item.id,"description":item.description,"name":item.name,"pictureUrl": item.pictureUrl,"isDiscontinued":item.isDiscontinued,"detail":[]} for item in _goods]
			for item in item_list:
				_details = db.session.query(Deatil_img).filter_by(goodsId = item["id"]).all()
				_details_list = [{"id":s.id,"pictureUrl":s.pictureUrl,"rank":s.rank} for s in _details]
				item["detail"] = _details_list

			return pageResult(200,"get goods_specs success",item_list,_page,_pageSize,_goods_count)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")

#根据goodsId 随机添加一行数据
@bp.route("/api/goods/detail/<goodsId>",methods=["GET"])
def specs_add_random(goodsId):
	if request.method == "GET":
		try:
			data = {
				"goodsId": goodsId,
                "pictureUrl": "https://localhost/uploads/goods/detail/2024083000041_c1e675ce_goods.png",
				"rank":50
			}	
			db.session.add(Deatil_img(**data))
			db.session.commit()
			return result(200,"random add detail success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")	



#删除thumb数据
@bp.route("/api/detail/<id>",methods=["DELETE"])
def detail_delete(id):
	if request.method == "DELETE":
		try:
			db.session.query(Deatil_img).filter_by(id=id).delete()
			db.session.commit()
			return result(200,"delete thumbs success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use DELETE method")	



#修改detail数据
@bp.route("/api/detail",methods=["PUT"])
def thumb_update():
	if request.method == "PUT":
		try:
			
			json_data = request.get_json()
			_id = json_data.get("id")
			_rank = json_data.get("rank")
			_pictureUrl = json_data.get('pictureUrl')
			thumb_img = db.session.query(Deatil_img).filter_by(id=_id).first()
			if thumb_img.pictureUrl != _pictureUrl:
				threading.Thread(target=moveFile, args=(_pictureUrl,GOODS_DETAIL_TMP_FOLDER_URL,GOODS_DETAIL_FOLDER_URL)).start()
			thumb_img.rank = _rank
			thumb_img.pictureUrl = f"{GOODS_DETAIL_HTTP_URL}{os.path.basename(_pictureUrl)}"

			db.session.commit()
			return result(200,"put detail success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use PUT method")	