from decimal import Decimal
import math
import traceback
from flask import g, json, request
from sqlalchemy import and_
from app.model.cart import Cart
from app.model.cartItems import CartItem
from app.model.delivery import Delivery
from app.model.goods import *
from app.model.addresses import *
from app.model.goodsTags import *
from app.model.logistic import Logistic
from app.model.orderItems import OrderItem
from app.model.orders import Order
from app.model.sku import Sku
from app.model.users import *

from app.utils.utils import *
from app.views.orders import bp
from datetime import datetime, timedelta

#获取预付订单
@bp.route("/api/order/pre",methods=["POST"])
def order_pre():
	if request.method == "POST":
		try:
			# 1.再次购买
			# 2.立即购买
			# 3.从购物车中创造订单
			postFee = 8 # 运费，假设为8元 (后期要对接物流系统)
			        # 获取原始请求数据
			raw_data = request.data.decode('utf-8')
			
			# 如果请求数据不为空，则尝试解析 JSON
			if raw_data:
				try:
					req = request.get_json()
				except Exception as e:
					return  result(400,"Failed to decode JSON object")
			else:
				req = {}

			req_orderId = req.get('orderId',None)
			req_count = req.get('count',None)
			req_skuId = req.get('skuId',None)
			cartItems_list = [ { } ]
			summary = {}

			if req_orderId:
				# 1.再次购买  查订单对应的订单项，然后看  skuId-->goodsId  以及Count
				orderItems = db.session.query(OrderItem).filter_by(orderId=int(req_orderId)).all()
				cartItems_list = [{"skuId": item.skuId, "count":item.count } for item in orderItems]

				for item in cartItems_list:	
					sku = db.session.query(Sku).filter_by(id=int(item["skuId"])).first()
					good = db.session.query(Goods).filter_by(id=sku.goodsId).first()
					str_json = json.loads(sku.specs) 
					attrsText = ""
					attrsText = ', '.join(item['valueName'] for item in str_json)
					item["id"] = sku.goodsId
					item["skuId"] = item["skuId"]
					item["count"] = item["count"]
					item["name"] = good.name
					item["picture"] = good.pictureUrl
					item["payPrice"] = sku.price
					item["price"] = sku.price
					item["attrsText"] = attrsText
					item["totalPayPrice"] = Decimal(item["count"])  * Decimal(str(sku.price))
					item["totalPrice"] = Decimal(item["count"])* Decimal(str(sku.price))

				#计算summary信息
				summary = {
					"discountPrice": 0,
					"goodsCount":  sum(Decimal(item["count"]) for item in cartItems_list),
					"totalPrice": sum(Decimal(str(item["totalPrice"])) for item in cartItems_list),
					"postFee": postFee,
					"totalPayPrice":  Decimal(str(sum(Decimal(str(item["totalPrice"])) for item in cartItems_list)))  + Decimal(str(postFee)) 
				}
			elif req_count and req_skuId:
				# 2.立即购买
				for item in cartItems_list:	
					sku = db.session.query(Sku).filter_by(id=int(req_skuId)).first()
					good = db.session.query(Goods).filter_by(id=sku.goodsId).first()
					str_json = json.loads(sku.specs) 
					attrsText = ""
					attrsText = ', '.join(item['valueName'] for item in str_json)
					item["id"] = sku.goodsId
					item["skuId"] = int(req_skuId)
					item["count"] = int(req_count)
					item["name"] = good.name
					item["picture"] = good.pictureUrl
					item["payPrice"] = sku.price
					item["price"] = sku.price
					item["attrsText"] = attrsText
					item["totalPayPrice"] =Decimal(int(req_count)) * Decimal(str(sku.price))
					item["totalPrice"] = Decimal(int(req_count)) * Decimal(str(sku.price))

				#计算summary信息
				summary = {
					"discountPrice": 0,
					"goodsCount":  sum(Decimal(item["count"]) for item in cartItems_list),
					"totalPrice": sum(Decimal(str(item["totalPrice"])) for item in cartItems_list),
					"postFee": postFee,
					"totalPayPrice":  Decimal(str(sum(Decimal(str(item["totalPrice"])) for item in cartItems_list)))  + Decimal(str(postFee)) 
				}

			else:		
				# 3.从购物车中创造订单
				cart = db.session.query(Cart).filter_by(userId = g.user_id).first()
				cartItems = db.session.query(CartItem).filter(and_(CartItem.cartId == cart.id,CartItem.selected == True)).all()
				cartItems_list = [{'id':item.goodsId,'count':item.count,"skuId":item.skuId} for item in cartItems]
				for item in cartItems_list:
					good = db.session.query(Goods).filter_by(id=item["id"]).first()
					sku = db.session.query(Sku).filter_by(id=item["skuId"]).first()
					str_json = json.loads(sku.specs) 
					attrsText = ""
					attrsText = ', '.join(item['valueName'] for item in str_json)
					item["name"] = good.name
					item["picture"] = good.pictureUrl
					item["payPrice"] = sku.price
					item["price"] = sku.price
					item["attrsText"] = attrsText
					item["totalPayPrice"] = Decimal(item["count"])*Decimal(str(sku.price))
					item["totalPrice"] = Decimal(item["count"])*Decimal(str(sku.price))
				# 计算summary信息
				summary = {
					"discountPrice": 0,
					"goodsCount":  sum(Decimal(item["count"]) for item in cartItems_list),
					"totalPrice": sum(Decimal(str(item["totalPrice"])) for item in cartItems_list),
					"postFee": postFee,
					"totalPayPrice": Decimal(str(sum(Decimal(str(item["totalPrice"])) for item in cartItems_list)))  + Decimal(str(postFee)) 
				}

			# 获取用户的默认收获地址
			address = db.session.query(Address).filter_by(userId = g.user_id).all()
			address_list = [{'id':item.id,'receiver':item.receiver,'contact':item.contact,'provinceCode':item.provinceCode,'cityCode':item.cityCode,'countyCode':item.countyCode,'address':item.address,'isDefault':1 if item.isDefault else 0} for item in address]
			for i in address_list:
				i['fullLocation'] = get_full_location( str(i['provinceCode']),str(i['cityCode']), str(i['countyCode']))
			
			re_data = {
				"goods":cartItems_list,
				"summary":summary,
				"userAddresses":address_list,
			}

			return result(200,"get orderPre success",re_data)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")

#创建订单
@bp.route("/api/order",methods=["POST"])
def order_add():
	if request.method == "POST":
		try:
			data = request.get_json()
			goods = data.get('goods')
			generate_id = generate_order_number()
			# 配送的快递公司之类的信息，没对接物流系统之前，先默认创造一个delivery表数据，以及一个logistic表 数据
			delivery = Delivery(orderId = generate_id, companyName = "测试公司",companyNumber = "1234567890", companyPhone = "13800000000",count=sum(item["count"] for item in goods))
			db.session.add(delivery)
			db.session.commit()
			delivery_id = db.session.query(Delivery).filter_by(orderId = generate_id).first().id
			logistic = Logistic(orderId = generate_id, deliveryId = delivery_id,text="备货中",time = str(datetime.now()))
			db.session.add(logistic)
			db.session.commit()
			order = Order(id = generate_id ,userId = g.user_id, buyerMessage = data.get('buyerMessage'), deliveryTimeType = data.get('deliveryTimeType'),addressId = data.get('addressId'),
				  payChannel = data.get('payChannel'), payType = data.get('payType'),deliveryId = delivery_id)
			db.session.add(order)
			db.session.commit()
			
			for item in goods:
				orderItem = OrderItem(orderId = generate_id,skuId =item["skuId"],count = item["count"])
				db.session.add(orderItem)
				db.session.commit()

			return result(200,"create order success",{"id":generate_id})
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")

#返回订单详情
@bp.route("/api/order/<id>",methods=["GET"])
def orderDetail(id):
	if request.method == "GET":
		try:
			order = db.session.query(Order).filter_by(id = id).first()
			# 计算countdown 倒计时
			# 假设 order.createdAt 是一个 datetime 对象
			countdown = -2
			if order.orderState == 1:
				created_at = order.createdAt
				current_time = datetime.now()
				# 计算时间差（以秒为单位）
				time_difference = (current_time - created_at).total_seconds()
				# 定义 30 分钟的秒数
				thirty_minutes_seconds = 30 * 60

				if time_difference > thirty_minutes_seconds:
					countdown = -1
					order.orderState = 6
					db.session.commit()
				else:
					countdown = thirty_minutes_seconds-time_difference

			# 收货地址
			address = db.session.query(Address).filter_by(id = order.addressId).first()

			# orderSkuItems
			orderItems = db.session.query(OrderItem).filter_by(orderId = id).all()
			orderSkus = [{"id":item.skuId,"quantity":item.count} for item in orderItems]

			for item in orderSkus:
				sku = db.session.query(Sku).filter_by(id=item["id"]).first()
				good = db.session.query(Goods).filter_by(id=sku.goodsId).first()
				str_json = json.loads(sku.specs) 
				attrsText = ""
				attrsText = ', '.join(i['valueName'] for i in str_json)
				item["curPrice"] = sku.price
				item["spuId"] = good.id
				item["name"] = good.name
				item["attrsText"] = attrsText
				item["image"] = good.pictureUrl

			orderResult = {
				"id" : order.id,
				"orderState":order.orderState,
				"countdown":countdown,
				"skus":orderSkus,
				"receiverContact":address.receiver,
				"receiverMobile":address.contact,
				"receiverAddress":address.address,
				"createTime":order.createdAt.strftime('%Y-%m-%d %H:%M:%S'),
				"totalMoney": sum(Decimal(str(item["curPrice"])) * Decimal(str(item["quantity"])) for item in orderSkus),
				"postFee":8,
				"payMoney":Decimal(str(sum(Decimal(str(item["curPrice"])) * Decimal(str(item["quantity"]))  for item in orderSkus)))  + Decimal(str(8)) 
			}

			return result(200,"get orderDetail success",orderResult)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")




#返回订单列表 (分订单状态以及分页)
@bp.route("/api/order",methods=["GET"])
def orderList():
	if request.method == "GET":
		try:
			# 如果订单被删除，就不返回 todo
			page = request.args.get('page',type=int)
			pageSize = request.args.get('pageSize',type=int)
			orderState = request.args.get('orderState',type=int)

			if orderState == 0 or orderState == 1 :
				order_c = db.session.query(Order).filter(and_(Order.orderState == 1,Order.userId == g.user_id,Order.isDeleted == False)).all()
				for i in order_c:
					created_at = i.createdAt
					current_time = datetime.now()
					# 计算时间差（以秒为单位）
					time_difference = (current_time - created_at).total_seconds()
					# 定义 30 分钟的秒数
					thirty_minutes_seconds = 30 * 60
					if time_difference > thirty_minutes_seconds:
						i.orderState = 6
				db.session.commit()

			total_count = 0
			orderListResult = {}

			if orderState == 0:
				# 计算偏移量
				offset = (page - 1) * pageSize
				order = db.session.query(Order).filter(and_(Order.userId == g.user_id,Order.isDeleted == False)).offset(offset).limit(pageSize).all()
				order_list = [{"id":item.id,"orderState":item.orderState,"createdAt":item.createdAt,"addressId":item.addressId} for item in order]
				
				for item in order_list:
					orderItems = db.session.query(OrderItem).filter_by(orderId = item["id"]).all()
					
					
					# 计算countdown 倒计时
					created_at = item["createdAt"]
					current_time = datetime.now()
					# 计算时间差（以秒为单位）
					time_difference = (current_time - created_at).total_seconds()
					# 定义 30 分钟的秒数
					thirty_minutes_seconds = 30 * 60
					countdown = 0
					if time_difference > thirty_minutes_seconds:
						countdown = -1
					else:
						countdown = thirty_minutes_seconds-time_difference
					
					orderSkus = [{"id":item.skuId,"quantity":item.count} for item in orderItems]
					totalNum =0	
					for ii in orderSkus:
						totalNum += ii["quantity"]
						sku = db.session.query(Sku).filter_by(id=ii["id"]).first()
						good = db.session.query(Goods).filter_by(id=sku.goodsId).first()
						str_json = json.loads(sku.specs) 
						attrsText = ""
						attrsText = ', '.join(i['valueName'] for i in str_json)
						ii["curprice"] = sku.price
						ii["spuId"] = good.id
						ii["name"] = good.name
						ii["attrsText"] = attrsText
						ii["image"] = good.pictureUrl


					# 收货地址
					address = db.session.query(Address).filter_by(id = item["addressId"]).first()
					item["totalNum"] = totalNum
					item["countdown"] = countdown
					item["skus"] = orderSkus
					item["receiverContact"] = address.receiver
					item["receiverMobile"] = address.contact
					item["receiverAddress"] = address.address
					item["createTime"] = item["createdAt"].strftime('%Y-%m-%d %H:%M:%S')
					item["totalMoney"] = sum(ii["curprice"] * ii["quantity"] for ii in orderSkus)
					item["postFee"] = 8
					item["payMoney"] = sum(ii["curprice"] * ii["quantity"] for ii in orderSkus) + 8
					del item["createdAt"]

				total_count = db.session.query(Order).filter( and_(Order.userId == g.user_id,Order.isDeleted == False) ).count()
				orderListResult = {
					"counts": total_count,
					"items": order_list,         
					"page": page,
					"pageSize": pageSize,
					"pages": math.ceil(total_count / pageSize)  # 向上取整
				}
			else:
				# 计算偏移量
				offset = (page - 1) * pageSize
				order = db.session.query(Order).filter(and_(Order.orderState == orderState,Order.userId == g.user_id,Order.isDeleted == False)).offset(offset).limit(pageSize).all()
				order_list = [{"id":item.id,"orderState":item.orderState,"createdAt":item.createdAt,"addressId":item.addressId} for item in order]
				for item in order_list:
					orderItems = db.session.query(OrderItem).filter_by(orderId = item["id"]).all()
					# 计算countdown 倒计时
					created_at = item["createdAt"]
					current_time = datetime.now()
					# 计算时间差（以秒为单位）
					time_difference = (current_time - created_at).total_seconds()
					# 定义 30 分钟的秒数
					thirty_minutes_seconds = 30 * 60
					countdown = 0
					if time_difference > thirty_minutes_seconds:
						countdown = -1
					else:
						countdown = thirty_minutes_seconds-time_difference
					
					orderSkus = [{"id":item.skuId,"quantity":item.count} for item in orderItems]
					totalNum =0
					for ii in orderSkus:
						totalNum += ii["quantity"]
						sku = db.session.query(Sku).filter_by(id=ii["id"]).first()
						good = db.session.query(Goods).filter_by(id=sku.goodsId).first()
						str_json = json.loads(sku.specs) 
						attrsText = ""
						attrsText = ', '.join(i['valueName'] for i in str_json)
						ii["curprice"] = sku.price
						ii["spuId"] = good.id
						ii["name"] = good.name
						ii["attrsText"] = attrsText
						ii["image"] = good.pictureUrl


					# 收货地址
					address = db.session.query(Address).filter_by(id = item["addressId"]).first()
					item["totalNum"] = totalNum
					item["countdown"] = countdown
					item["skus"] = orderSkus
					item["receiverContact"] = address.receiver
					item["receiverMobile"] = address.contact
					item["receiverAddress"] = address.address
					item["createTime"] = item["createdAt"].strftime('%Y-%m-%d %H:%M:%S')
					item["totalMoney"] = sum(ii["curprice"] * ii["quantity"] for ii in orderSkus)
					item["postFee"] = 8
					item["payMoney"] = sum(ii["curprice"] * ii["quantity"] for ii in orderSkus) + 8
					del item["createdAt"]

				total_count = db.session.query(Order).filter( and_(Order.orderState == orderState, Order.userId == g.user_id,Order.isDeleted == False) ).count()
				orderListResult = {
					"counts": total_count,
					"items": order_list,         
					"page": page,
					"pageSize": pageSize,
					"pages": math.ceil(total_count / pageSize)  # 向上取整
				}

			return result(200,"get orderList success",orderListResult)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")





#删除订单
@bp.route("/api/order",methods=["DELETE"])
def deleteOrder():
	if request.method == "DELETE":
		try:
			data = request.get_json()
			for item in data["ids"]:
				order = db.session.query(Order).filter_by(id = item).first()
				order.isDeleted = True

				orderItems = db.session.query(OrderItem).filter_by(orderId = item).all()
				for i in orderItems:
					i.isDeleted = True

				delivery = db.session.query(Delivery).filter_by(id = order.deliveryId).first()
				delivery.isDeleted = True

				logistics = db.session.query(Logistic).filter_by(orderId = item).all()
				for i in logistics:
					i.isDeleted = True

				db.session.commit()

			return result(200,"delete order success",{})
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use DELETE method")



#模拟发货
@bp.route("/api/order/consignment/<id>",methods=["GET"])
def consignment(id):
	if request.method == "GET":
		try:
			# 如果订单被删除，就不执行
			order = db.session.query(Order).filter_by(id = id).first()
			order.orderState = 3
			db.session.commit()
			return result(200,"consignment success",id)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")


#确认收货
@bp.route("/api/order/receipt/<id>",methods=["GET"])
def receipt(id):
	if request.method == "GET":
		try:
			# 如果订单被删除，就不执行
			order = db.session.query(Order).filter_by(id = id).first()
			order.orderState = 4
			db.session.commit()

			order = db.session.query(Order).filter_by(id = id).first()
			# 计算countdown 倒计时
			# 假设 order.createdAt 是一个 datetime 对象
			countdown = -2
			if order.orderState == 1:
				created_at = order.createdAt
				current_time = datetime.now()
				# 计算时间差（以秒为单位）
				time_difference = (current_time - created_at).total_seconds()
				# 定义 30 分钟的秒数
				thirty_minutes_seconds = 30 * 60

				if time_difference > thirty_minutes_seconds:
					countdown = -1
					order.orderState = 6
					db.session.commit()
				else:
					countdown = thirty_minutes_seconds-time_difference

			# 收货地址
			address = db.session.query(Address).filter_by(id = order.addressId).first()

			# orderSkuItems
			orderItems = db.session.query(OrderItem).filter_by(orderId = id).all()
			orderSkus = [{"id":item.skuId,"quantity":item.count} for item in orderItems]

			for item in orderSkus:
				sku = db.session.query(Sku).filter_by(id=item["id"]).first()
				good = db.session.query(Goods).filter_by(id=sku.goodsId).first()
				str_json = json.loads(sku.specs) 
				attrsText = ""
				attrsText = ', '.join(i['valueName'] for i in str_json)
				item["curPrice"] = sku.price
				item["spuId"] = good.id
				item["name"] = good.name
				item["attrsText"] = attrsText
				item["image"] = good.pictureUrl

			orderResult = {
				"id" : order.id,
				"orderState":order.orderState,
				"countdown":countdown,
				"skus":orderSkus,
				"receiverContact":address.receiver,
				"receiverMobile":address.contact,
				"receiverAddress":address.address,
				"createTime":order.createdAt.strftime('%Y-%m-%d %H:%M:%S'),
				"totalMoney": sum(Decimal(str(item["curPrice"])) * Decimal(str(item["quantity"])) for item in orderSkus),
				"postFee":8,
				"payMoney":Decimal(str(sum(Decimal(str(item["curPrice"])) * Decimal(str(item["quantity"]))  for item in orderSkus)))  + Decimal(str(8)) 
			}

			return result(200,"receipt success",orderResult)


		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")




#取消订单
@bp.route("/api/order/cancel/<id>",methods=["PUT"])
def cancelOrder(id):
	if request.method == "PUT":
		try:

			# 取消理由入库 todo
			print(request.get_json().get("cancelReason"))

			# 如果订单被删除，就不执行
			order = db.session.query(Order).filter_by(id = id).first()
			order.orderState = 6
			db.session.commit()

			order = db.session.query(Order).filter_by(id = id).first()
			# 计算countdown 倒计时
			# 假设 order.createdAt 是一个 datetime 对象
			countdown = -2
			if order.orderState == 1:
				created_at = order.createdAt
				current_time = datetime.now()
				# 计算时间差（以秒为单位）
				time_difference = (current_time - created_at).total_seconds()
				# 定义 30 分钟的秒数
				thirty_minutes_seconds = 30 * 60

				if time_difference > thirty_minutes_seconds:
					countdown = -1
					order.orderState = 6
					db.session.commit()
				else:
					countdown = thirty_minutes_seconds-time_difference

			# 收货地址
			address = db.session.query(Address).filter_by(id = order.addressId).first()

			# orderSkuItems
			orderItems = db.session.query(OrderItem).filter_by(orderId = id).all()
			orderSkus = [{"id":item.skuId,"quantity":item.count} for item in orderItems]

			for item in orderSkus:
				sku = db.session.query(Sku).filter_by(id=item["id"]).first()
				good = db.session.query(Goods).filter_by(id=sku.goodsId).first()
				str_json = json.loads(sku.specs) 
				attrsText = ""
				attrsText = ', '.join(i['valueName'] for i in str_json)
				item["curPrice"] = sku.price
				item["spuId"] = good.id
				item["name"] = good.name
				item["attrsText"] = attrsText
				item["image"] = good.pictureUrl

			orderResult = {
				"id" : order.id,
				"orderState":order.orderState,
				"countdown":countdown,
				"skus":orderSkus,
				"receiverContact":address.receiver,
				"receiverMobile":address.contact,
				"receiverAddress":address.address,
				"createTime":order.createdAt.strftime('%Y-%m-%d %H:%M:%S'),
				"totalMoney": sum(Decimal(str(item["curPrice"])) * Decimal(str(item["quantity"])) for item in orderSkus),
				"postFee":8,
				"payMoney":Decimal(str(sum(Decimal(str(item["curPrice"])) * Decimal(str(item["quantity"]))  for item in orderSkus)))  + Decimal(str(8)) 
			}

			return result(200,"receipt success",orderResult)


		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use PUT method")




# 搜索订单 
@bp.route("/api/ntk/order/search",methods=["POST"])
def searchGood():
	if request.method == "POST":
		try:
			# 如果订单被删除，就不返回 todo		
			data = request.get_json()
			page = data['page']
			pageSize = data['pageSize']
			val = data['val']
			orderState = 0
			print("---------------------" + val)
			if orderState == 0 or orderState == 1 :
				order_c = db.session.query(Order).filter(and_(Order.orderState == 1,Order.userId == g.user_id,Order.isDeleted == False)).all()
				for i in order_c:
					created_at = i.createdAt
					current_time = datetime.now()
					# 计算时间差（以秒为单位）
					time_difference = (current_time - created_at).total_seconds()
					# 定义 30 分钟的秒数
					thirty_minutes_seconds = 30 * 60
					if time_difference > thirty_minutes_seconds:
						i.orderState = 6
				db.session.commit()

			total_count = 0
			orderListResult = {}
			# 计算偏移量
			offset = (page - 1) * pageSize
			order = db.session.query(Order).filter(and_(Order.userId == g.user_id,Order.isDeleted == False)).offset(offset).limit(pageSize).all()
			order_list = [{"id":item.id,"orderState":item.orderState,"createdAt":item.createdAt,"addressId":item.addressId} for item in order]
			
			for item in order_list:
				orderItems = db.session.query(OrderItem).filter_by(orderId = item["id"]).all()
				
				
				# 计算countdown 倒计时
				created_at = item["createdAt"]
				current_time = datetime.now()
				# 计算时间差（以秒为单位）
				time_difference = (current_time - created_at).total_seconds()
				# 定义 30 分钟的秒数
				thirty_minutes_seconds = 30 * 60
				countdown = 0
				if time_difference > thirty_minutes_seconds:
					countdown = -1
				else:
					countdown = thirty_minutes_seconds-time_difference
				
				orderSkus = [{"id":item.skuId,"quantity":item.count} for item in orderItems]
				totalNum =0	
				for ii in orderSkus:
					totalNum += ii["quantity"]
					sku = db.session.query(Sku).filter_by(id=ii["id"]).first()
					good = db.session.query(Goods).filter_by(id=sku.goodsId).first()
					str_json = json.loads(sku.specs) 
					attrsText = ""
					attrsText = ', '.join(i['valueName'] for i in str_json)
					ii["curprice"] = sku.price
					ii["spuId"] = good.id
					ii["name"] = good.name
					ii["attrsText"] = attrsText + "fsafsaas"
					ii["image"] = good.pictureUrl	


				# 收货地址
				address = db.session.query(Address).filter_by(id = item["addressId"]).first()
				item["totalNum"] = totalNum
				item["countdown"] = countdown
				item["skus"] = orderSkus
				item["receiverContact"] = address.receiver
				item["receiverMobile"] = address.contact
				item["receiverAddress"] = address.address
				item["createTime"] = item["createdAt"].strftime('%Y-%m-%d %H:%M:%S')
				item["totalMoney"] = sum(ii["curprice"] * ii["quantity"] for ii in orderSkus)
				item["postFee"] = 8
				item["payMoney"] = sum(ii["curprice"] * ii["quantity"] for ii in orderSkus) + 8
				del item["createdAt"]

				total_count = db.session.query(Order).filter( and_(Order.userId == g.user_id,Order.isDeleted == False) ).count()
				orderListResult = {
					"counts": total_count,
					"items": order_list,         
					"page": page,
					"pageSize": pageSize,
					"pages": math.ceil(total_count / pageSize)  # 向上取整
				}

			return result(200,"get orderList success",orderListResult)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")


#分页获取所有订单
@bp.route("/api/orders/all",methods=["POST"])
def orders_all():
	if request.method == "POST":
		try:
			data = request.get_json()
			page = data.get('page')
			pageSize = data.get('pageSize')
			# 计算偏移量
			offset = (page - 1) * pageSize
			total_count = db.session.query(Order).filter_by(isDeleted = 0).count()
			users_list =  db.session.query(Order).filter_by(isDeleted = 0).offset(offset).limit(pageSize).all()
			item_list = [{'id':item.id,'userId':item.userId,'orderState':item.orderState,'buyerMessage':item.buyerMessage,'deliveryTimeType': item.deliveryTimeType,'addressId':item.addressId,'payChannel':item.payChannel,"payType":item.payType,"deliveryId":item.deliveryId} for item in users_list]
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