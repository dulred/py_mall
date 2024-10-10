from flask import request,jsonify
import os
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