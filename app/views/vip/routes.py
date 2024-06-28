import traceback
from flask import request,session
from app.utils.utils import *
from app.views.vip import bp
from app.model.vip import *
from app.model.user import *
from app.model.receipt import *
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
	

#购买VIP
@bp.route("/api/buy/vip",methods=["POST"])
def buy_vip():
	if request.method == "POST":
		form = request.form
		sId = session.get("_id",None)
		user = User.query.get(sId)
		if user.balance < form["payValue"]:
			return result(204,{"info":"余额不足"})
		try:
			user.balance = user.balance - form["payValue"]
			data = {
				"orderNum":getOrderNum(),
				"createTime":getNowDataTime(),
				"payValue":form["payValue"],
				"cutoffValue":form["cutoffValue"],
				"user_id":sId,
				"vipId":form["vipId"]
			}
			print(data)
			r = VipReceipt(**data)
			user.vip = form["vipId"]
			db.session.add(r)
			db.session.commit()
			return result(200)
		except:
			traceback.print_exc()
			return result(502,{"info":"服务端错误"})

#查看自己VIP购买情况
@bp.route("/api/self/vip")
def self_vip():
	if request.method == "GET":
		sId = session.get("_id",None)
		vrs = VipReceipt.query.filter_by(user_id=sId)
		data = dict() 
		data["data"] = []
		for vr in vrs:
			dic = vr.__dict__
			del dic["_sa_instance_state"]
			data["data"].append(dic)
		return result(200,data)


