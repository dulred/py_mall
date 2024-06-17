from flask import request,session
from app.utils.utils import *
from app.views.address import bp
from app.model.address import *

#用户个人地址添加
@bp.route("/api/self/address/add",methods=["POST"])
def self_address_add():
	if request.method=="POST":
		sId = session['_id']
		form = request.form
		data = {
			"province":form["province"],
			"town":form["town"],
			"county":form["county"],
			"detail":form["detail"],
			"user_id":sId
		}
		address = Address(**data)
		db.session.add(address)
		db.session.commit()
		return result(200)
#地址添加
@bp.route("/api/address/add",methods=["POST"])
def address_add():
	if request.method=="POST":

		form = request.form
		data = {
			"province":form["province"],
			"town":form["town"],
			"county":form["county"],
			"detail":form["detail"],
		}
		address = Address(**data)
		db.session.add(address)
		db.session.commit()
		return result(200)

#获取所有地址信息接口
@bp.route("/api/address")
def address():
	if request.method == "GET":

		addresses = Address.query.filter_by(user_id=None)
		data = dict()
		data["data"]=[]
		for address in addresses:
			dic = address.__dict__
			del dic["_sa_instance_state"]
			data["data"].append(dic) 
		return result(200,data)
	
#地址删除
@bp.route("/api/address/delete",methods=["DELETE"])
def address_delete():
	if request.method=="DELETE":
		_id = request.form["id"]
		Address.query.filter_by(_id=_id).delete()
		db.session.commit()
		return result(200)