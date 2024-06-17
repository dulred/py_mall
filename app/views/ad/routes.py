from flask import request
from app.utils.utils import *
from app.views.ad import bp
from app.model.ad import *
#广告
@bp.route("/api/ads/add",methods=["POST"])
def ads_add():
	if request.method=="POST":

		form = request.form
		image = request.files["image"]
		save_path = "./static/ads/"+image.filename
		image.save(save_path)
		data = {
			"content":form["content"],
			"createTime":getNowDataTime(),
			"displayTime":form["displayTime"],
			"endTime":form["endTime"],
			"image":save_path,
			"title":form["title"],
			"intro":form["intro"],
		}
		ad = Ad(**data)
		db.session.add(ad)
		db.session.commit()
		return result(200)

#获取所有广告
@bp.route("/api/ads")
def ads():
	if request.method == "GET":
		ads = Ad.query.filter_by(displayTime>=getNowDataTime())
		data = dict()
		data["data"] = []
		for ad in ads:
			dic = ad.__dict__
			del dic["_sa_instance_state"]
			data["data"].append(dic) 

		return result(200,data)

#广告删除
@bp.route("/api/ads/delete",methods=["DELETE"])
def ads_delete():
	if request.method=="DELETE":

		_id = request.form["id"]
		Ad.query.filter_by(_id=_id).delete()
		return result(200)