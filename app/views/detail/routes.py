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
			thumb = db.session.query(Thumb_img).filter_by(goodsId=id).order_by(desc(Thumb_img.rank)).all()
			thumb_list = [{'pictureUrl':item.pictureUrl} for item in thumb]
			for thumb in thumb_list:
				goodsResult["mainPictures"].append(thumb["pictureUrl"])
			# 查询详细页图
			detail = db.session.query(Deatil_img).filter_by(goodsId=id).order_by(desc(Deatil_img.rank)).all()
			detail_list = [{'pictureUrl':item.pictureUrl} for item in detail]
			for detail in detail_list:
				goodsResult["details"]["pictures"].append(detail["pictureUrl"])

			# 查询属性值图
			goodsStyle = db.session.query(GoodsStyle).filter_by(goods_id=id).all()
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
