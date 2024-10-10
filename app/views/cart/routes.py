from flask import g, json, request
from sqlalchemy import and_
from app.model.goods import Goods
from app.model.sku import Sku
from app.views.cart import bp
from app.model.cart import *
from app.model.cartItems import *
from app.utils.utils import *


#购物车项添加接口
@bp.route("/api/cartItem",methods=["POST"])
def cartItem_add():
	if request.method == "POST":
		try:
			cart  = db.session.query(Cart).filter_by(userId=g.user_id).first()
			if not cart:
				cart = Cart(userId=g.user_id)
				db.session.add(cart)
				db.session.commit()
				cart = db.session.query(Cart).filter_by(userId=g.user_id).first()
			
			data = request.get_json()
			goodsId = db.session.query(Sku).filter_by(id=data["skuId"]).first().goodsId
			c_cartItem = db.session.query(CartItem).filter(and_(CartItem.skuId==data["skuId"],CartItem.cartId == cart.id)).first()
			if c_cartItem:
				c_cartItem.count = c_cartItem.count + int(data["count"])
				db.session.commit()
				return result(200,"update cartItem success")
			else:
				cartItem = CartItem(cartId=cart.id,skuId=data["skuId"],count=data["count"],goodsId = goodsId)
				db.session.add(cartItem)
				db.session.commit()
				return result(200,"add cartItem success")
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")


#获取购物项
@bp.route("/api/cartItem",methods=["GET"])
def cartItem_find():
	if request.method == "GET":
		try:
			cart  = db.session.query(Cart).filter_by(userId=g.user_id).first()
			if not cart:
				cart = Cart(userId=g.user_id)
				db.session.add(cart)
				db.session.commit()
				cart = db.session.query(Cart).filter_by(userId=g.user_id).first()
			
			cartItems = db.session.query(CartItem).filter_by(cartId=cart.id).all()
			cartItems_list = [{"id":item.goodsId,"skuId":item.skuId,"count":item.count,"selected":item.selected}for item in cartItems]
			
			for item in cartItems_list:
				good = db.session.query(Goods).filter_by(id=item["id"]).first()
				sku = db.session.query(Sku).filter_by(id=item["skuId"]).first()
				str = json.loads(sku.specs) 
				attrsText = ""
				attrsText = ', '.join(item['valueName'] for item in str)
				item["name"] = good.name
				item["picture"] = good.pictureUrl
				item["stock"] = sku.inventory
				item["nowPrice"] = sku.price
				item["attrsText"] = attrsText
		
			return result(200,"select cartItem success",cartItems_list)
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")


#修改购物项
@bp.route("/api/cartItem/<int:skuId>",methods=["PUT"])
def cartItem_update(skuId):
	if request.method == "PUT":
		try:
			data = request.get_json()
			cart = db.session.query(Cart).filter_by(userId=g.user_id).first()
			cartItem = db.session.query(CartItem).filter(and_(CartItem.skuId==skuId,CartItem.cartId == cart.id)).first()
			selected = data.get('selected')
			count = data.get('count')

			if count is not None:
				cartItem.count = count
				db.session.commit()
				return result(200,"update count success")
			else:
				cartItem.selected = selected
				db.session.commit()
				return result(200,"update selected success")
			
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use PUT method")


#删除购物项
@bp.route("/api/cartItem",methods=["DELETE"])
def cartItem_delete():
	if request.method == "DELETE":
		try:
			cart = db.session.query(Cart).filter_by(userId=g.user_id).first()
			data = request.get_json()
			for item in data["ids"]:
				cartItem = db.session.query(CartItem).filter(and_(CartItem.skuId==item,CartItem.cartId == cart.id)).first()
				db.session.delete(cartItem)
				db.session.commit()

			return result(200,"delete cartItem success")
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use DELETE method")



#全选
@bp.route("/api/cartItem/selected",methods=["PUT"])
def carItemSelected():
	if request.method == "PUT":
		try:
			cart = db.session.query(Cart).filter_by(userId=g.user_id).first()
			cartItem = db.session.query(CartItem).filter(and_(CartItem.cartId == cart.id)).all()
			data = request.get_json()
			if data["selected"]:
				for item in cartItem:
					item.selected = True
					db.session.commit()
			else:
				for item in cartItem:
					item.selected = False
					db.session.commit()
			return result(200,"selected ALL or NOT success")
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use PUT method")
