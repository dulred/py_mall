from flask import request
from sqlalchemy import desc
from app.model.goods import Goods
from app.utils.utils import *
from app.views.category import bp
from app.model.categories import *

#分类添加接口
@bp.route("/api/category",methods=["POST"])
def category_add():
	if request.method == "POST":
		try:
			# 接收和分解JSON 数据
			data = request.get_json()
			categoryLevel = data.get('categoryLevel')
			categoryName = data.get('categoryName')
			categoryRank = data.get('categoryRank')
			parentId = data.get('parentId')

			# 创建 Category 实例并插入到数据库
			category = Category(categoryLevel=categoryLevel, categoryName=categoryName, categoryRank=categoryRank, parentId=parentId)
			try:
				db.session.add(category)
				db.session.commit()
			except Exception as e:
				return result(205,str(e))

			return result(200)
		except Exception as e:
			return result(502,str(e))
	return result(400,msg="please use POST method")


#获取分类页数据接口(小程序展示)
@bp.route("/api/ntk/category/top",methods=["GET"])
def category_page():
	if request.method == "GET":
		try:
			# 创建 Category 实例并插入到数据库
			category1_list =  db.session.query(Category).filter_by(categoryLevel=1,isDeleted=0).order_by(desc(Category.categoryRank)).all()
			top_list = [{'id':item.id,'name':item.categoryName} for item in category1_list]
			category2_list = db.session.query(Category).filter_by(categoryLevel=2,isDeleted=0).all()
			children_list = [{'id':item.id,'name':item.categoryName,'parentId':item.parentId} for item in category2_list]

			goods_list =  db.session.query(Goods).filter_by(isDeleted = 0).all()
			goods_dict_list = [
				{
					'id': goods.id,
					'name': goods.name,
					'price': goods.price,
					'pictureUrl': goods.pictureUrl,
					'categoryId': goods.categoryId
					# 其他需要的字段
				} for goods in goods_list
			]

			for item in top_list:
				item["children"] = []
			for item in children_list:
				item["goods"] = []

			for item in children_list:
				for i in goods_dict_list:
					if i["categoryId"] == item["id"]:
						item["goods"].append(i)

			for item in top_list:
				for i in children_list:
					if i["parentId"] == item["id"]:
						item["children"].append(i)

			return result(200,'get category page success',top_list)
		except Exception as e:
			return result(502,str(e))
	return result(400,msg="please use GET method")

#获取所有一级分类的数据(backstage)
@bp.route("/api/category/first",methods=["GET"])
def category_1_list():
	if request.method == "GET":
		try:
			# 创建 Category 实例并插入到数据库
			category1_list =  db.session.query(Category).filter_by(categoryLevel=1,isDeleted=0).order_by(desc(Category.categoryRank)).all()
			item_list = []
			for item in category1_list:
				item_list.append({"id": item.id, "categoryName":item.categoryName})
			return result(200,'get first level category success',item_list)
		except Exception as e:
			return result(502,str(e))
	return result(400,msg="please use GET method")

#获取所有二级分类的数据(backstage)
@bp.route("/api/category/second",methods=["GET"])
def category_2_list():
	if request.method == "GET":
		try:
			# 创建 Category 实例并插入到数据库
			category1_list =  db.session.query(Category).filter_by(categoryLevel=2,isDeleted=0).order_by(desc(Category.categoryRank)).all()
			item_list = []
			for item in category1_list:
				item_list.append({"id": item.id, "categoryName":item.categoryName})
			return result(200,'get first level category success',item_list)
		except Exception as e:
			return result(502,str(e))
	return result(400,msg="please use GET method")



#获取所有分类级别的数据(backstage)
@bp.route("/api/category",methods=["GET"])
def category_all():
	if request.method == "GET":
		try:
			# 创建 Category 实例并插入到数据库
			category1_list =  db.session.query(Category).filter_by(categoryLevel=1,isDeleted=0).order_by(desc(Category.categoryRank)).all()
			top_list = [{'id':item.id,'name':item.categoryName,'rank':item.categoryRank} for item in category1_list]
			category2_list = db.session.query(Category).filter_by(categoryLevel=2,isDeleted=0).all()
			children_list = [{'id':item.id,'name':item.categoryName,'parentId':item.parentId,'rank':item.categoryRank} for item in category2_list]

			for item in top_list:
				item["children"] = []

			for item in top_list:
				for i in children_list:
					if i["parentId"] == item["id"]:
						item["children"].append(i)

			return result(200,'get category page success',top_list)
		except Exception as e:
			return result(502,str(e))
	return result(400,msg="please use GET method")


#获取特定分类的数据
@bp.route("/api/category/<id>",methods=["GET"])
def get_category_byId(id):
	if request.method == "GET":
		try:
			
			_ca = db.session.query(Category).filter_by(id=id,isDeleted = 0).first()
			item = {
                'categoryName': _ca.categoryName,
                'categoryLevel': _ca.categoryLevel,
                'categoryRank': _ca.categoryRank,
                'parentId': _ca.parentId,
			}

			return result(200,'get category success',item)
		except Exception as e:
			return result(502,str(e))
	return result(400,msg="please use GET method")


#修改分类
@bp.route("/api/category",methods=["PUT"])
def update_category():
	if request.method == "PUT":
		try:
			# 接收和分解JSON 数据
			data = request.get_json()
			id = data.get('id')
			categoryName = data.get('categoryName')
			categoryLevel = data.get('categoryLevel')
			categoryRank = data.get('categoryRank')
			parentId = data.get('parentId')

			_ca = db.session.query(Category).filter_by(id=id,isDeleted = 0).first()

			# 确保整个一级分类下没有任何二级分类
			if _ca.categoryLevel==1 and categoryLevel==2:
				ca_children_count = db.session.query(Category).filter_by(parentId = id,isDeleted = 0).count()
				if ca_children_count > 0:
					return result(400,'请先删除所有二级分类才能修改一级分类')
				
			# 确保整个二级分类没有任何对应商品
			if _ca.categoryLevel==2 and  categoryLevel==1:
				goods_count =  db.session.query(Goods).filter_by(categoryId= id,isDeleted = 0).count()
				if goods_count > 0:
					return result(400,'请先删除该类别下的商品才能修改一级分类')
			
			_ca.categoryLevel = categoryLevel
			_ca.categoryName = categoryName
			_ca.categoryRank = categoryRank
			_ca.parentId = parentId
			db.session.commit()

			return result(200,'update category success')
		except Exception as e:
			return result(502,str(e))
	return result(400,msg="please use PUT method")



#删除分类
@bp.route("/api/category/<id>",methods=["DELETE"])
def delete_category(id):
	if request.method == "DELETE":
		try:
			_ca = db.session.query(Category).filter_by(id=id).first()
			if _ca.categoryLevel == 1:
				# 获取该一级分类下的二级分类
				children_count = db.session.query(Category).filter_by(parentId=id,isDeleted = 0).count()
				if children_count>0:
					return result(400,'需要删除所有子类才能删除本类')
			else:
				# 创建 Category 实例并插入到数据库
				goods_count =  db.session.query(Goods).filter_by(categoryId= id,isDeleted = 0).count()
				print(goods_count)
				if goods_count > 0:
					return result(400,'请删除类别下的商品才能删除本类别')
			
			_ca.isDeleted = True
			db.session.commit()

			return result(200,'delete category success')
		except Exception as e:
			return result(502,str(e))
	return result(400,msg="please use DELETE method")