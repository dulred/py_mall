from flask import request, jsonify
import os
from app.views.sw import bp
from app.model.sw import *
from config import GOODS_SW_FOLDER_URL,GOODS_SW_TMP_FOLDER_URL,GOODS_SW_HTTP_URL
from app.utils.utils import *
import threading

def sw_placeholder(items_list_type,flag):
	if flag == 0:
		if len(items_list_type) < 3:
			need_insert  = 3 - len(items_list_type)
			for _ in range(need_insert):
				items_list_type.append({"pictureUrl":"https://via.placeholder.com/400x320","isPlaceholder":1})
	elif flag == 1:
		if len(items_list_type) < 3:
			need_insert  = 3 - len(items_list_type)
			for _ in range(need_insert):
				items_list_type.append({"pictureUrl":"https://via.placeholder.com/400x589","isPlaceholder":1})

#获取所有首尾图（Backstage）
@bp.route("/api/sw",methods=["GET"])
def sw_all():
	if request.method == "GET":
		try:
			sw = db.session.query(SW).filter_by(isDeleted=0).all()
			items_list = [{'id':item.id,'pictureUrl': item.pictureUrl, 'imgType': 1 if item.imgType else 0,'isSelected':item.isSelected,"isPlaceholder":0} for item in sw]

			# 过滤 imgType 为 0 的项
			items_list_type_0 = [item for item in items_list if item['imgType'] == 0]
			sw_placeholder(items_list_type_0,0)

			# 过滤 imgType 为 1 的项
			items_list_type_1 = [item for item in items_list if item['imgType'] == 1]
			sw_placeholder(items_list_type_1,1)
			
			res =  {
				"s":items_list_type_0,
				"w":items_list_type_1
			}
			return result(200,"select sw success",res)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")

#首尾图添加接口
@bp.route("/api/sw",methods=["POST"])
def sw_add():
	if request.method == "POST":
		try:
			if 'file' not in request.files:
				return result(404,'No file part')

			file = request.files['file']

			if file.filename == '':
				return result(404,'file isEmpty')

			if file and allowed_file(file.filename):
				# 生成新的文件名
				filename = generate_filename(file.filename)
				file_path = os.path.join(GOODS_SW_FOLDER_URL,filename)
				file.save(file_path)
				data  = {
					"pictureUrl": f"{GOODS_SW_HTTP_URL}{os.path.basename(file_path)}",
					"imgType": int(request.form.get('imgType')),
					"isSelected":False
				}
				sw = SW(**data)
				try:
					db.session.add(sw)
					db.session.commit()
				except Exception as e:  
					return result(200,str(e))
				return result(200,'File uploaded successfully',{'http_url': f"{GOODS_SW_HTTP_URL}{filename}"})
			else:
				return result(400,'Invalid file type. Allowed types: png, jpg, jpeg, gif')
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")

#首尾图更新接口
@bp.route("/api/sw",methods=["PUT"])
def sw_update():
	if request.method == "PUT":
		try:
			if 'file' not in request.files:
				return result(404,'No file part')

			file = request.files['file']

			if file.filename == '':
				return result(404,'file isEmpty')

			if file and allowed_file(file.filename):
				# 生成新的文件名
				filename = generate_filename(file.filename)
				file_path = os.path.join(GOODS_SW_FOLDER_URL,filename)
				file.save(file_path)

				sw_id = int(request.form.get('id'))
				sw = db.session.query(SW).filter_by(id=sw_id).first()
				sw.pictureUrl =  f"{GOODS_SW_HTTP_URL}{os.path.basename(file_path)}"
				try:
					db.session.commit()
				except Exception as e:  
					return result(200,str(e))
				return result(200,'File uploaded successfully',{'http_url': f"{GOODS_SW_HTTP_URL}{filename}"})
			else:
				return result(400,'Invalid file type. Allowed types: png, jpg, jpeg, gif')
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use PUT method")


#首尾图更新选中状态
@bp.route("/api/sw/selected",methods=["PUT"])
def sw_update_status():
	if request.method == "PUT":
		try:
			sw_id = int(request.form.get('id'))
			sw_list = db.session.query(SW).filter_by(imgType = request.form.get('imgType')).all()
			for item in sw_list:
				item.isSelected = True if item.id == sw_id else False
			try:
				db.session.commit()
			except Exception as e:  
				return result(200,str(e))
			return result(200,'selected status update successfully')
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use PUT method")




# 获取能展示在页面的首尾图(小程序端使用)
@bp.route("/api/ntk/sw/first_last_show",methods=["GET"])
def sw_first_last_show():
	if request.method == "GET":
		try:
			selected_items = db.session.query(SW).filter_by(isSelected=1).all()	
			items_list = [{'pictureUrl': item.pictureUrl, 'imgType': 1 if item.imgType else 0} for item in selected_items]
			return result(200,"get sw images success",items_list)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")

