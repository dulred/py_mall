'''
Author: yzs dulred@qq.com
Date: 2024-06-27 12:08:37
LastEditors: yzs dulred@qq.com
LastEditTime: 2024-07-01 10:35:38
FilePath: \py_mall\app\views\comments\routes.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from flask import request,session
from app.model.goods import *
from app.model.address import *
from app.model.goodsType import *
from app.model.user import *
from app.model.vip import *
from app.model.admin import *
from app.utils.utils import *
from app.views.user import bp


#查看用户个人信息
@bp.route("/api/self",methods=["GET"])
def self_info():

	if request.method == "GET":
		sId = session['_id'] 
		user = User.query.get(sId)
		user = user.__dict__
		del user["_sa_instance_state"]
		del	user['createTime']
		del	user['loginTime']
		del	user['logoutTime']
		del	user['password']
		try:
			user['vip']=Vip.query.get(user['vip']).name
		except:
			user['vip'] = '暂无VIP'
		user['address'] = []
		try:
			addresses = Address.query.filter_by(user_id=sId)
			for address in addresses:
				address = address.__dict__
				del address["_sa_instance_state"]
				user['address'].append(address)
		except:
			pass

		if not user['name']:
			user['name'] = '未命名'

		return result(200,user)


# 获取所有用户信息
@bp.route("/api/users",methods=["POST","GET"])
def getUser():
	if request.method == "GET":

		nums = User.query.count()
		return result(200,{"nums":nums})

	if request.method == "POST":
		start = request.form["start"]
		nums = request.form["nums"]
		users = User.query.offset(start).limit(nums)
		data = dict()
		data["data"] = []
		for user in users:
			dic = user.__dict__
			del dic["_sa_instance_state"]
			
			
			data["data"].append(dic)
		return result(200,data)
	

#用户充值     
@bp.route("/api/balance",methods=["POST"])
def balance():
	if request.method=="POST":
		balance = request.form["balance"]
		sId = session.get("_id")
		user = User.query.get(sId)
		try:
			user.balance = user.balance + balance
		except:
			user.balance = balance
		db.session.commit()
		return result()
	

#添加管理员
@bp.route("/api/admin/add",methods=["POST"])
def admin_add():
	if request.method == "POST":

		form = request.form
		data = {
			"name":form["name"],
			"account":form["account"],
			"password":md5(form["password"]),
			"createTime":getNowDataTime(),
			"level":form["level"]
		}
		admin = Admin(**data)
		db.session.add(admin)
		db.session.commit()
		return result(200)
	
#退出系统
@bp.route("/api/quit",methods=["POST"])
def quit():
	if request.method == "POST":
		_id = session["_id"]
		_type = request.form["type"]
		if _type == "admin":
			admin = Admin.query.get(_id)
			admin.logoutTime = getNowDataTime()
		else:
			user = User.query.get(_id)
			user.logoutTime = getNowDataTime()
		del session["_id"]
		return result(200)