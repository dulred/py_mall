from flask import request, jsonify
import os
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