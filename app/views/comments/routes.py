
'''
Author: yzs dulred@qq.com
Date: 2024-06-27 12:08:37
LastEditors: yzs dulred@qq.com
LastEditTime: 2024-07-01 11:10:59
FilePath: \py_mall\app\views\comments\routes.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

from flask import request,session
from app.model.goods import *
from app.model.address import *
from app.model.goodsType import *
from app.model.comment import *
from app.utils.utils import *
from app.views.comments import bp

#用户评论商品
@bp.route("/api/add/comment",methods=["POST"])
def add_comment():
	if request.method=="POST":
		sId = session["_id"]
		form = request.form
		image = request.files["image"]
		save_path = "./static/comments/"+image.filename
		image.save(save_path)
		data = {
			"createTime":getNowDataTime(),
			"content":form["content"],
			"points":form["points"],
			"user":sId,
			"good":form["goodsId"],
			"screenCut":save_path
		}
		db.session.add(Comment(**data))
		db.session.commit()
		return result()

#获取商品评论内容
@bp.route("/api/comment/<int:goodsId>",methods=["GET","DELETE"])
def comment(goodsId):
	if request.method == "GET":
		comments = Comment.query.filter_by(good=goodsId)
		data = dict()
		data["data"] = []
		for comment in comments:
			dic = comment.__dict__
			del dic["_sa_instance_state"]
			data["data"].append(dic)
		return result(200,data)