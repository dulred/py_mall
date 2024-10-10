from flask import g, request,session
from sqlalchemy import and_
from app.utils.utils import *
from app.views.address import bp
from app.model.addresses import *


# 添加个人地址
@bp.route("/api/address",methods=["POST"])
def address_add():
	if request.method == "POST":
		try:
			addressId = generate_order_number()
			data_json = request.get_json()
			if str(data_json["isDefault"]) == "1":
				address_re = db.session.query(Address).filter(and_(Address.userId == g.user_id,Address.isDefault == True)).first()
				if address_re:
					address_re.isDefault = False
					db.session.commit()
			data = {
				"id":addressId,	
				"userId":g.user_id,
				"receiver": data_json['receiver'],
				"contact": data_json['contact'],
				"provinceCode": data_json['provinceCode'],
				"cityCode": data_json['cityCode'],
				"countyCode": data_json['countyCode'],
				"address": data_json['address'],
				"isDefault": True if str(data_json['isDefault']) == '1' else False,
			}
			address = Address(**data)
			db.session.add(address)
			db.session.commit()
			return result(200,"add address success",addressId)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")



# 查找个人地址所有
@bp.route("/api/address",methods=["GET"])
def address_findAll():
	if request.method == "GET":
		try:
			data = db.session.query(Address).filter(and_(Address.userId ==g.user_id,Address.isDeleted == False)).all()
			item_list = [{'id':item.id,'receiver':item.receiver,'contact':item.contact,'provinceCode':item.provinceCode,'cityCode':item.cityCode,'countyCode':item.countyCode,'address':item.address,'isDefault':1 if item.isDefault else 0} for item in data]
			
			for i in item_list:
				i['fullLocation'] = get_full_location(str(i['provinceCode']),str(i['cityCode']), str(i['countyCode']))
			
			return result(200,"select address success",item_list)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")

# 查找个人地址ById
@bp.route("/api/address/<id>",methods=["GET"])
def address_findById(id):
	if request.method == "GET":
		try:
			data = db.session.query(Address).filter(and_(Address.id ==id,Address.isDeleted == False)).first()
			address = {
				"id":data.id,
                "receiver":data.receiver,
                "contact":data.contact,
                "provinceCode":data.provinceCode,
                "cityCode":data.cityCode,
                "countyCode":data.countyCode,
                "address":data.address,
                "isDefault": 1 if data.isDefault else 0,
                "fullLocation": get_full_location(str(data.provinceCode),str(data.cityCode), str(data.countyCode))
			}
			return result(200,"select address success",address)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")

# 修改个人地址
@bp.route("/api/address/<id>",methods=["PUT"])
def address_update(id):
	if request.method == "PUT":
		try:
			data = request.get_json()
			if str(data["isDefault"]) == "1":
				address_re = db.session.query(Address).filter(and_(Address.userId == g.user_id,Address.isDefault == True)).first()
				if address_re:
					address_re.isDefault = False
					db.session.commit()
			address = db.session.query(Address).filter_by(id = id).first()
			address.receiver = data["receiver"]
			address.contact = data["contact"]
			address.provinceCode = data["provinceCode"]
			address.cityCode = data["cityCode"]
			address.countyCode = data["countyCode"]
			address.address = data["address"]
			address.isDefault = True if str(data['isDefault']) == '1' else False
			db.session.commit()
			return result(200,"update address success",id)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use PUT method")

# 删除个人地址
@bp.route("/api/address/<int:id>",methods=["DELETE"])
def address_delete(id):
	if request.method == "DELETE":
		try:
			address = db.session.query(Address).filter_by(id = id).first()
			address.isDeleted = True
			db.session.commit()
			return result(200,"delete address success",id)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use DELETE method")