from flask import request, jsonify
import os
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