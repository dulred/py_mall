from flask import request
from app.model.logistic import Logistic
from app.views.delivery import bp
from app.model.delivery import *
from app.utils.utils import *


#获取对应订单的发货信息
@bp.route("/api/delivery/<orderId>",methods=["GET"])
def delivery_find(orderId):
	if request.method == "GET":
		try:

			delivery = Delivery.query.filter_by(orderId=orderId).first()
			logistics = db.session.query(Logistic).filter_by(deliveryId=delivery.id).all()
			logistics_list =[{"id":logistic.id, "text":logistic.text, "time":logistic.time} for logistic in logistics]
			deliveryResult = {
				"company": {
					"name":delivery.companyName,
					"number":delivery.companyNumber,
					"tel":delivery.companyPhone
				},
				"count":delivery.count,
				"list":logistics_list
			}

			return result(200,"get delivery success",deliveryResult)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")