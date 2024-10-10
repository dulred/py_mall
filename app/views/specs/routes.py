from flask import request
from app.views.specs import bp
from app.model.specs import *
from app.utils.utils import *

#specs添加接口
@bp.route("/api/specs",methods=["POST"])
def specs_add():
	if request.method == "POST":
		try:
			data = request.form
			db.session.add(Specs(**data))
			db.session.commit()
			return result(200,"select address success",request.form["goodsId"])
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")