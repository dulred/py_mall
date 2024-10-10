from flask import request
from app.views.pay import bp
from app.model.orders import *
from app.utils.utils import *


#模拟支付---修改订单为已支付状态，也可以说是待发货状态
@bp.route("/api/pay/mock",methods=["GET"])
def delivery_find():
	if request.method == "GET":
		try:
			orderId = request.args.get("orderId")
			order = Order.query.filter_by(id=orderId).first()
			order.orderState = 2
			db.session.commit()
			return result(200,"pay mock success",orderId)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")