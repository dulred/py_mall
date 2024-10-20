from flask import request, jsonify
import os
from app.model.goods import Goods
from app.views.thumb import bp
from app.model.thumb_img import *
from config import GOODS_THUMB_FOLDER_URL,GOODS_THUMB_TMP_FOLDER_URL,GOODS_THUMB_HTTP_URL
from app.utils.utils import *
import threading

#商品详细图添加接口
@bp.route("/api/thumb",methods=["POST"])
def thumb_add():
	if request.method == "POST":
		try:
			form = request.get_json()
			# 移动文件，并替换入库的图片路径为实际路径
			file_path = form["pictureUrl"]
			threading.Thread(target=moveFile, args=(file_path,GOODS_THUMB_TMP_FOLDER_URL,GOODS_THUMB_FOLDER_URL)).start()
			# 入库数据的准备
			data  = {
				"pictureUrl": f"{GOODS_THUMB_HTTP_URL}{os.path.basename(file_path)}",
				"goodsId": form['goodsId'],
				"rank":form["rank"]
			}
			thumb_img = Thumb_img(**data)
			try:
				db.session.add(thumb_img)
				db.session.commit()
			except Exception as e:  
				return result(200,str(e))
			
			return result(200,"add thumb_img success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")


#thumb
@bp.route("/api/goods/thumb",methods=["POST"])
def goods_spec():
	if request.method == "POST":
		try:
			json_data = request.get_json()
			_page = json_data.get('page')
			_pageSize = json_data.get('pageSize')
			offset = (_page - 1) * _pageSize
			_goods_count = db.session.query(Goods).filter_by(categoryId = json_data.get("categoryId"),isDeleted = 0).count()
			_goods = db.session.query(Goods).filter_by(categoryId = json_data.get("categoryId"),isDeleted = 0).offset(offset).limit(_pageSize).all()
			item_list = [{"id":item.id,"description":item.description,"name":item.name,"pictureUrl": item.pictureUrl,"isDiscontinued":item.isDiscontinued,"thumb":[]} for item in _goods]
			for item in item_list:
				_details = db.session.query(Thumb_img).filter_by(goodsId = item["id"]).all()
				_details_list = [{"id":s.id,"pictureUrl":s.pictureUrl,"rank":s.rank} for s in _details]
				item["thumb"] = _details_list

			return pageResult(200,"get thumbs success",item_list,_page,_pageSize,_goods_count)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")


#根据goodsId 随机添加一行数据
@bp.route("/api/goods/thumb/<goodsId>",methods=["GET"])
def specs_add_random(goodsId):
	if request.method == "GET":
		try:
			data = {
				"goodsId": goodsId,
                "pictureUrl": "https://localhost/uploads/goods/thumb/2024082923250_300deef7_goods.jpg",
				"rank":50
			}	
			db.session.add(Thumb_img(**data))
			db.session.commit()
			return result(200,"random add thumbs success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")	


#删除thumb数据
@bp.route("/api/thumb/<id>",methods=["DELETE"])
def thumb_delete(id):
	if request.method == "DELETE":
		try:
			db.session.query(Thumb_img).filter_by(id=id).delete()
			db.session.commit()
			return result(200,"delete thumbs success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use DELETE method")	


#修改thumb数据
@bp.route("/api/thumb",methods=["PUT"])
def thumb_update():
	if request.method == "PUT":
		try:
			
			json_data = request.get_json()
			_id = json_data.get("id")
			_rank = json_data.get("rank")
			_pictureUrl = json_data.get('pictureUrl')
			thumb_img = db.session.query(Thumb_img).filter_by(id=_id).first()
			if thumb_img.pictureUrl != _pictureUrl:
				threading.Thread(target=moveFile, args=(_pictureUrl,GOODS_THUMB_TMP_FOLDER_URL,GOODS_THUMB_FOLDER_URL)).start()
			thumb_img.rank = _rank
			thumb_img.pictureUrl = f"{GOODS_THUMB_HTTP_URL}{os.path.basename(_pictureUrl)}"

			db.session.commit()
			return result(200,"put thumbs success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use PUT method")	