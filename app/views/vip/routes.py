from flask import request
from app.utils.utils import *
from app.views.vip import bp
from app.model.vip import *

#VIP删除
@bp.route("/api/vip/delete",methods=["DELETE"])
def vip_delete():
	if request.method=="DELETE":

		_id = request.form["id"]
		Vip.query.filter_by(_id=_id).delete()
		return result(200)
	
#VIP添加
@bp.route("/api/vip/add",methods=["POST"])
def vip_add():
	if request.method == "POST":

		name = request.form["name"]
		level = request.form["level"]
		vip = Vip(name=name,level=level)
		db.session.add(vip)
		db.session.commit()
		return result()

#获取所有VIP信息
@bp.route("/api/vip")
def vip():
	if request.method=="GET":
		vips = Vip.query.all()
		data = dict()
		data["data"] = []
		for vip in vips:
			dic = vip.__dict__
			del dic["_sa_instance_state"]
			data["data"].append(dic) 

		return result(200,data)