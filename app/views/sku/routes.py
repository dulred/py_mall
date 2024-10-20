from flask import request, jsonify
import os
from app.model.goods import Goods
from app.views.sku import bp
from app.model.sku import *
from config import GOODS_SKU_FOLDER_URL,GOODS_SKU_TMP_FOLDER_URL,GOODS_SKU_HTTP_URL
from app.utils.utils import *
import threading

#sku添加接口
@bp.route("/api/sku",methods=["POST"])
def sku_add():
	if request.method == "POST":
		try:
			form = request.get_json()
			# 移动文件，并替换入库的图片路径为实际路径
			file_path = form["picture"]
			threading.Thread(target=moveFile, args=(file_path,GOODS_SKU_TMP_FOLDER_URL,GOODS_SKU_FOLDER_URL)).start()

			# 入库数据的准备
			data  = {
				"picture": f"{GOODS_SKU_HTTP_URL}{os.path.basename(file_path)}",
				"goodsId": form['goodsId'],
				"inventory":form["inventory"],
				"price": form["price"],
				"specs": form["specs"],
			}
			sku = Sku(**data)
			try:
				db.session.add(sku)
				db.session.commit()
			except Exception as e:  
				return result(200,str(e))
			
			return result(200,"add sku success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")


#根据分类Id 查询对应goods里面的sku
@bp.route("/api/goods/sku",methods=["POST"])
def sku_byCategoryId():
	if request.method == "POST":
		try:
			json_data = request.get_json()
			_page = json_data.get('page')
			_pageSize = json_data.get('pageSize')
			offset = (_page - 1) * _pageSize
			_goods_count = db.session.query(Goods).filter_by(categoryId = json_data.get("categoryId"),isDeleted = 0).count()
			_goods = db.session.query(Goods).filter_by(categoryId = json_data.get("categoryId"),isDeleted = 0).offset(offset).limit(_pageSize).all()
			item_list = [{"id":item.id,"description":item.description,"name":item.name,"pictureUrl": item.pictureUrl,"isDiscontinued":item.isDiscontinued,"skus":[]} for item in _goods]
			for item in item_list:
				_skus = db.session.query(Sku).filter_by(goodsId = item["id"]).all()
				_skus_list = [{"id":s.id,"inventory":s.inventory,"price":s.price,"specs":s.specs,"picture":s.picture} for s in _skus]
				item["skus"] = _skus_list

			return pageResult(200,"get goods_sku success",item_list,_page,_pageSize,_goods_count)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")


#修改sku数据
@bp.route("/api/sku",methods=["PUT"])
def sku_update():
	if request.method == "PUT":
		try:
		
			json_data = request.get_json()
			file_path = json_data.get("picture")
			spec = db.session.query(Sku).filter_by(id=json_data["id"],isDeleted = 0).first()
			if spec.picture != file_path:
				threading.Thread(target=moveFile, args=(file_path,GOODS_SKU_TMP_FOLDER_URL,GOODS_SKU_FOLDER_URL)).start()
			spec.inventory = json_data.get("inventory")
			spec.price = json_data.get("price")
			spec.picture = f"{GOODS_SKU_HTTP_URL}{os.path.basename(file_path)}"
			db.session.commit()
			return result(200,"update sku success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use PUT method")	



