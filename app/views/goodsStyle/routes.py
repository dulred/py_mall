from flask import request,jsonify
import os
from app.model.goods import Goods
from app.views.goodsStyle import bp
from app.model.goodsStyle import *
from app.utils.utils import *


#商品详细图添加接口
@bp.route("/api/goodsStyle",methods=["POST"])
def goodsStyle_add():
	if request.method == "POST":
		try:
			goodsId = request.args.get('goodsId')
			# 接收和分解JSON 数据
			data  = request.json
			for item in data:
				db.session.add(GoodsStyle(style_key=item.get('name'),style_value=item.get('value'),goods_id=goodsId))
				db.session.commit()

			return result(200,"add goodsSytle success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")	



#分页获取分类下商品以及goods_style
@bp.route("/api/goods/style/categoryType",methods=["POST"])
def goods_style():
	if request.method == "POST":
		try:
			json_data = request.get_json()
			_page = json_data.get('page')
			_pageSize = json_data.get('pageSize')
			offset = (_page - 1) * _pageSize
			_goods_count = db.session.query(Goods).filter_by(categoryId = json_data.get("categoryId"),isDeleted = 0).count()
			_goods = db.session.query(Goods).filter_by(categoryId = json_data.get("categoryId"),isDeleted = 0).offset(offset).limit(_pageSize).all()
			item_list = [{"id":item.id,"description":item.description,"name":item.name,"pictureUrl": item.pictureUrl,"isDiscontinued":item.isDiscontinued,"styles":[]} for item in _goods]
			for item in item_list:
				_style = db.session.query(GoodsStyle).filter_by(goods_id = item["id"]).all()
				_style_list = [{"id":s.id,"style_key":s.style_key,"style_value":s.style_value} for s in _style]
				item["styles"] = _style_list

			return pageResult(200,"get goods_sytle success",item_list,_page,_pageSize,_goods_count)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")	


#修改属性键值对
@bp.route("/api/goodsStyle",methods=["PUT"])
def goodsStyle_update():
	if request.method == "PUT":
		try:
			json_data = request.get_json()
			_id = json_data.get('id')
			_style_key = json_data.get('style_key')
			_style_value = json_data.get('style_value')
			_goods_style = db.session.query(GoodsStyle).filter_by(id = _id).first()
			_goods_style.style_key = _style_key
			_goods_style.style_value = _style_value
			db.session.commit()
			return result(200,"update goodsSytle success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use PUT method")	
	

#根据goodsId 随机添加一行数据
@bp.route("/api/goodsStyle/<goodsId>",methods=["GET"])
def goodsStyle_add_random(goodsId):
	if request.method == "GET":
		try:
			data = {
				"goods_id": goodsId,
                "style_key": "color",
                "style_value": "random color"
			}	
			db.session.add(GoodsStyle(**data))
			db.session.commit()
			return result(200,"random add goodsSytle success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")	




#根据goodsId 随机添加一行数据
@bp.route("/api/goodsStyle/<id>",methods=["DELETE"])
def goodsStyle_delete(id):
	if request.method == "DELETE":
		try:
			db.session.query(GoodsStyle).filter_by(id = id).delete()
			db.session.commit()
			return result(200,"delete goodsSytle success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use DELETE method")	


