'''
Author: yzs dulred@qq.com
Date: 2024-06-27 12:08:37
LastEditors: yzs dulred@qq.com
LastEditTime: 2024-07-01 10:35:38
FilePath: \py_mall\app\views\comments\routes.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import math
from flask import g, request
from app.model.admin_user import AdminUser
from app.model.goods import *
from app.model.addresses import *
from app.model.goodsTags import *
from app.model.users import *
from app.utils.utils import *
from app.views.user import bp
from config import DOMAIN

#使用账号密码登录接口
@bp.route("/api/login",methods=["POST"])
def login():
	if request.method == "POST":
		username = request.get_json().get("username")
		password = request.get_json().get("password")
		password = md5(password)
		user = AdminUser.query.filter_by(username=username,isActive = 1,isDeleted=0).first()
		token = create_token(user.id)
		if user:
			if user.password==password:
				user.loginTime = getNowDataTime()
				db.session.commit()
				return result(200,'login success!',{"token": token})
			else:
				return result(202,'login error!',{"info":"密码不正确",})
		else:
			return result(201,'login error!',{"info":"无该用户信息"})


#管理员注册接口 (内部人员使用)
""" {
    "username": "admin",
    "password": "123456",
    "roleId":1 (默认是管理员，模块级别以及接口级别的权限控制)
} """
@bp.route("/api/admin",methods=["POST"])
def admin_register():
	if request.method == "POST":
		json_data = request.get_json()
		username = json_data.get("username")
		_password = json_data.get("password")
		_roleId = json_data.get("roleId")
		password = md5(_password)
		db.session.add(AdminUser(avatar=f"{DOMAIN}/uploads/avatar/2024083017245_f4ff8519_goods.png",gender="男",birthday="1990-01-01",provinceCode=110000
						,cityCode=110000,countyCode=110101,loginTime = getNowDataTime(),username=username,password=password,roleId = _roleId,mobile=123456789))
		db.session.commit()
		return result(200,'register success!')
	return result(400,"please use POST method")


# 小程序模拟手机号登录
@bp.route("/api/login/wxMin/simple", methods=["POST"])
def simple_login():
	if request.method=="POST":
		try:
			# todo 查看是否被禁用或者注销
			phoneNumber =  request.get_json().get('phoneNumber')
			user = db.session.query(User).filter_by(mobile=phoneNumber).first()
			if user:
				token = create_token(user.id)
				user_dict = {
					"nickname": user.nickname,
					"id": user.id,
					"mobile": user.mobile,
					"avatar": user.avatar,
					"token": token
				}
				return result(200,'pre user success!',user_dict)
			else:
				db.session.add(User(mobile=phoneNumber,avatar=f"{DOMAIN}/uploads/avatar/2024083017245_f4ff8519_goods.png",gender="男",birthday="1990-01-01",profession="保密",provinceCode=110000
						,cityCode=110000,countyCode=110101,loginTime = getNowDataTime()))
				db.session.commit()
				re_user = db.session.query(User).filter_by(mobile=phoneNumber).first()
				user_id = re_user.id
				token = create_token(user_id)
				user_dict = {
					"nickname": re_user.nickname,
					"id": re_user.id,
					"mobile": re_user.mobile,
					"avatar": re_user.avatar,
					"token": token
				}
				return result(200,'create user success!',user_dict)
		
		except Exception as e:
			return result(502,str(e))


#查看用户个人信息
@bp.route("/api/self",methods=["GET"])
def self_info():
	try:
		user = db.session.query(User).filter_by(id = g.user_id).first()
		user_dict = {
			"avatar":user.avatar,
			"birthday":user.birthday.strftime('%Y-%m-%d') if user.birthday else None,
			"fullLocation":get_full_location(str(user.provinceCode), str(user.cityCode),str(user.countyCode)),
			"gender":user.gender,
			"id":user.id,
			"nickname":user.nickname,
			"profession":user.profession,
		}
		return result(200,'select user',user_dict)
	except Exception as e:
		return result(400,str(e))



#修改用户状态
@bp.route("/api/user",methods=["PUT"])
def update_user_status():
	if request.method == "PUT":
		try:
			json_data = request.get_json()
			user = db.session.query(User).filter_by(id=json_data.get("id")).first()
			if json_data.get('type') == 0:
				user.isActive = json_data.get('value')

			if json_data.get('type') == 1:
				user.isDeleted = json_data.get('value')

			try:
				db.session.commit()
			except Exception as e:
				return result(400,str(e))
			
			return result(200,"update user success")
		except Exception as e:
			return result(400,str(e))
	return result(400,"please use PUT method")



# 修改个人信息
@bp.route("/api/self",methods=["PUT"])
def update_self():
	if request.method == "PUT":
		try:
			data = request.get_json()
			user = db.session.query(User).filter(User.id == g.user_id).first()
			user.nickname = data["nickname"]
			user.gender = data["gender"]
			user.birthday = data["birthday"]
			user.provinceCode = data["provinceCode"]
			user.cityCode = data["cityCode"]
			user.countyCode = data["countyCode"]
			user.profession = data["profession"]
			print(data["provinceCode"] + " " + data["cityCode"] + " " + data["countyCode"])
			db.session.commit()
			user = db.session.query(User).filter(User.id == g.user_id).first()
			user_dict = {
				"avatar":user.avatar,
				"birthday":user.birthday.strftime('%Y-%m-%d') if user.birthday else None,
				"fullLocation":get_full_location(str(user.provinceCode), str(user.cityCode),str(user.countyCode)),
				"gender":user.gender,
				"id":user.id,
				"nickname":user.nickname,
				"profession":user.profession,
			}
			return result(200,"update user success",user_dict)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use PUT method")



#分页获取所有用户信息
@bp.route("/api/users/all",methods=["POST"])
def users_all():
	if request.method == "POST":
		try:
			data = request.get_json()
			page = data.get('page')
			pageSize = data.get('pageSize')
			# 计算偏移量
			offset = (page - 1) * pageSize
			total_count = db.session.query(User).filter_by(isDeleted = 0).count()
			users_list =  db.session.query(User).filter_by(isDeleted = 0).offset(offset).limit(pageSize).all()
			print(type(users_list[0].birthday))
			print(type(users_list[0].loginTime))
			item_list = [{'id':item.id,'nickname':item.nickname,'mobile':item.mobile,'avatar': item.avatar,'gender':item.gender,'birthday':gmt_to_Shanghai(item.birthday),"profession":item.profession,"provinceCode":item.provinceCode,"cityCode":item.cityCode,"countyCode":item.countyCode,"remark":item.remark,"balance":item.balance,"loginTime":gmt_to_Shanghai(item.loginTime),"logoutTime":gmt_to_Shanghai(item.logoutTime),"isActive":item.isActive,"isDeleted":item.isDeleted} for item in users_list]
			list_result = {
				"total": total_count,
				"pages": math.ceil(total_count / pageSize),
				"page": page,
				"pageSize": pageSize,
				"items": item_list,
			}
			return result(200,"查询成功",list_result)
		except Exception as e:
			return result(400,str(e))
	return result(400,"please use POST method")




#分页获取所有管理员信息
@bp.route("/api/admin/all",methods=["POST"])
def admin_all():
	if request.method == "POST":
		try:
			data = request.get_json()
			page = data.get('page')
			pageSize = data.get('pageSize')
			# 计算偏移量
			offset = (page - 1) * pageSize
			total_count = db.session.query(AdminUser).filter_by(isDeleted = 0).count()
			users_list =  db.session.query(AdminUser).filter_by(isDeleted = 0).offset(offset).limit(pageSize).all()
			print(type(users_list[0].birthday))
			print(type(users_list[0].loginTime))
			item_list = [{'id':item.id,"roleId":item.roleId,'nickname':item.nickname,'mobile':item.mobile,'avatar': item.avatar,'gender':item.gender,'birthday':gmt_to_Shanghai(item.birthday),"provinceCode":item.provinceCode,"cityCode":item.cityCode,"countyCode":item.countyCode,"remark":item.remark,"loginTime":gmt_to_Shanghai(item.loginTime),"logoutTime":gmt_to_Shanghai(item.logoutTime),"isActive":item.isActive,"isDeleted":item.isDeleted} for item in users_list]
			list_result = {
				"total": total_count,
				"pages": math.ceil(total_count / pageSize),
				"page": page,
				"pageSize": pageSize,
				"items": item_list,
			}
			return result(200,"查询成功",list_result)
		except Exception as e:
			return result(400,str(e))
	return result(400,"please use POST method")



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
	
#退出系统
@bp.route("/api/quit",methods=["POST"])
def quit():
	if request.method == "POST":
		_type = request.form["type"]
		user = User.query.get(_id)
		user.logoutTime = getNowDataTime()
		return result(200)
# 返回特定用户的信息
@bp.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    # 逻辑处理，返回特定用户的信息
    # user_id 是用户的唯一标识符
	return result(200)

@bp.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    # 逻辑处理，更新特定用户的信息
    # 请求体中包含更新的数据
	return result(200)

@bp.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    # 逻辑处理，删除特定用户
	return result(200)