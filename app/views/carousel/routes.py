from flask import request
import os
from app.views.carousel import bp
from app.model.carousel import *
from config import GOODS_CAROUSEL_FOLDER_URL,GOODS_CAROUSEL_TMP_FOLDER_URL,GOODS_CAROUSEL_HTTP_URL
from app.utils.utils import *
import threading
from sqlalchemy import desc



def carousel_placeholder(items_list_type):
	if len(items_list_type) < 6:
		need_insert  = 6 - len(items_list_type)
		for _ in range(need_insert):
			items_list_type.append({"pictureUrl":"https://via.placeholder.com/375x225","isPlaceholder":1})

#轮播图获取接口（手机端）全查
@bp.route("/api/ntk/carousel",methods=["GET"])
def carousel_list():
	if request.method == "GET":
		try:
			carousel_list =  db.session.query(Carousel).filter_by(isDeleted = 0).order_by(desc(Carousel.rank)).all()
			item_list = [{'pictureUrl': item.pictureUrl, 'goodsId':item.goodsId} for item in carousel_list]
			return result(200,"get carousel success",item_list)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")

#轮播图获取接口（backstage）全查 (有占位图)
@bp.route("/api/carousel",methods=["GET"])
def carousel_list_2():
	if request.method == "GET":
		try:
			carousel_list =  db.session.query(Carousel).filter_by(isDeleted = 0).order_by(desc(Carousel.rank)).all()
			item_list = [{'id':item.id,'pictureUrl': item.pictureUrl, 'goodsId':item.goodsId,'isPlaceholder':0,"rank":item.rank} for item in carousel_list]
			carousel_placeholder(item_list)
			return result(200,"get carousel success",item_list)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")


#轮播图上传接口
@bp.route("/api/carousel",methods=["POST"])
def carousel_add():
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
				file_path = os.path.join(GOODS_CAROUSEL_FOLDER_URL,filename)
				file.save(file_path)

				# 最低的rank (拿到之后-1即为默认的rank)
				lowest_rank = db.session.query(Carousel).order_by(Carousel.rank).first()
				# 入库数据的准备,(默认的goodsId给1)
				data  = {
					"pictureUrl": f"{GOODS_CAROUSEL_HTTP_URL}{os.path.basename(file_path)}",
					"rank": lowest_rank.rank - 1,
					"goodsId":1
				}
				carousel = Carousel(**data)
				try: 
					db.session.add(carousel)
					db.session.commit()
				except Exception as e:  
					return result(200,str(e))
				
				return result(200,'File uploaded successfully',{'http_url': f"{GOODS_CAROUSEL_HTTP_URL}{filename}"})
			else:
				return result(400,'Invalid file type. Allowed types: png, jpg, jpeg, gif')
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")




#轮播图修改接口
@bp.route("/api/carousel",methods=["PUT"])
def carousel_update():
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
				file_path = os.path.join(GOODS_CAROUSEL_FOLDER_URL,filename)
				file.save(file_path)


				form = request.form

				carousel=db.session.query(Carousel).filter_by(id=form['id'],isDeleted=0).first()

				# 提取文件名
				file_name = os.path.basename(carousel.pictureUrl)
				print("File name:", file_name)

				# 构建本地文件路径
				local_file_path = os.path.join(GOODS_CAROUSEL_FOLDER_URL, file_name)

				# 检查文件是否存在并删除文件
				if os.path.exists(local_file_path):
					os.remove(local_file_path)
				else:
					return result(500,f"File '{file_name}' does not exist.")
				
				carousel.pictureUrl = f"{GOODS_CAROUSEL_HTTP_URL}{filename}"

				try: 
					db.session.commit()
				except Exception as e:  
					return result(200,str(e))	
				
				return result(200,'File uploaded successfully',{'http_url': f"{GOODS_CAROUSEL_HTTP_URL}{filename}"})
			else:
				return result(400,'Invalid file type. Allowed types: png, jpg, jpeg, gif')
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use PUT method")


#轮播图修改rank接口
@bp.route("/api/carousel/rank",methods=["PUT"])
def carousel_update_rank():
	if request.method == "PUT":
		try:

			form = request.form

			carousel=db.session.query(Carousel).filter_by(id=form['id'],isDeleted=0).first()
			carousel.rank = form['rank']
			try: 
				db.session.commit()
			except Exception as e:  
				return result(200,str(e))
			
			return result(200,'update rank successfully')
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use PUT method")



#轮播图修改跳转商品id接口
@bp.route("/api/carousel/link",methods=["PUT"])
def carousel_update_link():
	if request.method == "PUT":
		try:

			data = request.get_json()

			carousel=db.session.query(Carousel).filter_by(id=data['id'],isDeleted=0).first()
			carousel.goodsId = data.get('goodsId')
			try: 
				db.session.commit()
			except Exception as e:  
				return result(200,str(e))
			
			return result(200,'update link successfully')
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use PUT method")


#轮播图删除接口
@bp.route("/api/carousel/<id>",methods=["DELETE"])
def carousel_delete(id):
	if request.method == "DELETE":
		try:
			carousel = db.session.query(Carousel).filter_by(id=id,isDeleted=0).first()
			carousel.isDeleted = 1
			try: 
				db.session.commit()
			except Exception as e:  
				return result(200,str(e))
			
			return result(200,"delete carousel success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use DELETE method")


