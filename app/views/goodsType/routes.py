from flask import request
from app.model.goodsType import *
from app.utils.utils import *
from app.views.goodsType import bp

#商品分类的查询
@bp.route("/api/goods/type")
def goods_type():
	if request.method == "GET":
		
		_types = GoodsType.query.all()
		data = dict()
		data["data"] = []
		for _type in _types:
			dic = _type.__dict__
			del dic["_sa_instance_state"]
			data["data"].append(dic) 

		return result(200,data)
	
#商品分类的添加
@bp.route("/api/goods/type/add",methods=["POST"])
def goods_type_add():
	if request.method=="POST":
		name = request.form["name"]
		_type = GoodsType(name=name)
		db.session.add(_type)
		db.session.commit()
		return result(200)

#商品分类删除
@bp.route("/api/goods/type/delete",methods=["DELETE"])
def goods_type_delete():
	if request.method=="DELETE":

		_id = request.form["id"]
		GoodsType.query.filter_by(_id=_id).delete()
		db.session.commit()

		return result(200)

