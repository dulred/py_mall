from flask import request,session
from app.views.auth import bp
from app.utils.utils import *
from app.model import db
from app.model.admin import Admin
from app.model.user import User
from app.model.court import Court
#登录接口。普通用户和管理员分开 
@bp.route("/api/login",methods=["POST","GET"])
def login():

	if request.method == "POST":
		account = request.form["account"]
		password = request.form["password"]
		password = md5(password)
		_type = request.form["type"]
		if _type == "admin":
			admin = Admin.query.filter_by(account=account).first()
			if admin:
				if admin.password == password:
					session["_id"] = admin._id
					admin.loginTime = getNowDataTime()
					db.session.commit()
					return result(200)
				else:
					return result(202,{"info":"密码不正确"})
			else:
				return result(201,{"info":"无该管理员信息"})
		else:
			user = User.query.filter_by(account=account).first()
			if user:
				if user.password==password:
					session["_id"] = user._id
					user.loginTime = getNowDataTime()
					db.session.commit()
					return result(200)
				else:
					return result(202,{"info":"密码不正确"})
			else:
				return result(201,{"info":"无该用户信息"})
	if request.method == "GET":
		return result()

#普通用户注册接口
@bp.route("/api/regist",methods=["POST"])
def regist():
	if request.method=="POST":
		try:
			account = request.form["account"]
			password = request.form["password"]
			password = md5(password)
			user = User(account=account,password=password)
			try:
				db.session.add(user)
				db.session.commit()
			except:
				return result(205,{"info":"重复注册"})
			user = User.query.filter_by(account=account).first()
			court = Court(user_id=user._id)
			db.session.add(court)
			db.session.commit()
			session["_id"] = user._id 
			return result(200)
		except:
			return result(502,{"info":"数据有误"})
		

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