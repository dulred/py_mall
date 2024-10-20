import json
from flask import request
from app.model.goods import Goods
from app.model.sku import Sku
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


#分页获取分类下商品以及spec_style
@bp.route("/api/goods/spec/categoryType",methods=["POST"])
def goods_spec():
	if request.method == "POST":
		try:
			json_data = request.get_json()
			_page = json_data.get('page')
			_pageSize = json_data.get('pageSize')
			offset = (_page - 1) * _pageSize
			_goods_count = db.session.query(Goods).filter_by(categoryId = json_data.get("categoryId"),isDeleted = 0).count()
			_goods = db.session.query(Goods).filter_by(categoryId = json_data.get("categoryId"),isDeleted = 0).offset(offset).limit(_pageSize).all()
			item_list = [{"id":item.id,"description":item.description,"name":item.name,"pictureUrl": item.pictureUrl,"isDiscontinued":item.isDiscontinued,"specs":[]} for item in _goods]
			for item in item_list:
				_specs = db.session.query(Specs).filter_by(goodsId = item["id"]).all()
				_specs_list = [{"id":s.id,"name":s.name,"values":s.values,"rank":s.rank} for s in _specs]
				item["specs"] = _specs_list

			return pageResult(200,"get goods_specs success",item_list,_page,_pageSize,_goods_count)
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use POST method")




#根据goodsId 随机添加一行数据
@bp.route("/api/goods/spec/<goodsId>",methods=["GET"])
def specs_add_random(goodsId):
	if request.method == "GET":
		try:
			data = {
				"goodsId": goodsId,
                "name": "color",
                "values": "randomColor",
				"rank":50
			}	
			db.session.add(Specs(**data))
			db.session.commit()
			return result(200,"random add specs success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")	




#修改spec数据
@bp.route("/api/spec",methods=["PUT"])
def specs_update():
	if request.method == "PUT":
		try:
			json_data = request.get_json()
			spec = db.session.query(Specs).filter_by(id=json_data["id"],isDeleted = 0).first()
			spec.name = json_data.get("name")
			spec.values = json_data.get("values")
			spec.rank = json_data.get("rank")
			db.session.commit()
			return result(200,"update specs success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use PUT method")	



#删除specs数据
@bp.route("/api/spec/<id>",methods=["DELETE"])
def specs_delete(id):
	if request.method == "DELETE":
		try:
			db.session.query(Specs).filter_by(id=id).delete()
			db.session.commit()
			return result(200,"delete specs success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use DELETE method")	



def recursive_sku(end_index,path,general_list,now):
    end_index -=1
    if end_index == 0:
        return
    item = []

    if end_index == len(path):
        for i in range(path[end_index - 1]):
            temp  = [i]
            item.append(temp)
    else:
        temp = general_list[len(path) - (end_index + 1)]
        temp_len = len(temp)
        total = path[now] * temp_len
        for i in range(total):
            if i < temp_len:  
                temp_item = temp[i % temp_len].copy()
                temp_item.insert(0,0)
                item.append(temp_item)
            else:
                temp_item = temp[i % temp_len].copy()
                n = math.ceil( i / temp_len )
                if i % temp_len == 0:
                    temp_item.insert(0, n)
                else:
                    temp_item.insert(0, n-1)
                item.append(temp_item)
        now-=1
            
    general_list.append(item)

    recursive_sku(end_index,path,general_list,now)



def generate_json(name,valueName):
    json  = {
        "name":name,
        "valueName":valueName
    }

    return json


#点击生成或更新sku数据
@bp.route("/api/spec/generate/<goodsId>",methods=["GET"])
def specs_generate_sku(goodsId):
	if request.method == "GET":
		try:
			# 是否存在有对应skuId，有的话删除再创建
			exit_sku_count = db.session.query(Sku).filter_by(goodsId = goodsId).count()
			if exit_sku_count > 0:
				db.session.query(Sku).filter_by(goodsId = goodsId).delete()
				db.session.commit()
			specs = db.session.query(Specs).filter_by(goodsId=goodsId).all()
			specs_list = [{"name":item.name,"values":item.values} for item in specs]
			mock_list_value = []
			mock_list_name = []
			mock_list_se = []
			for spec in specs_list:
				se = spec["values"].split(',')
				mock_list_se.append(se)
				mock_list_value.append(len(se))
				mock_list_name.append(spec["name"])
			
			# print(mock_list_value)
			# print(mock_list_name)

			general_list = []
			now = len(mock_list_value) - 2
			end_index = len(mock_list_value)
			recursive_sku(end_index + 1,mock_list_value,general_list,now)
			
			json_list = []

			# print(general_list[len(mock_list_value) - 1])

			for i in range(len(general_list[len(mock_list_value) - 1])):
				temp_list = []
				for index,item in enumerate(mock_list_name):
					specific_list  = mock_list_se[index].copy()
					number = general_list[len(mock_list_value) - 1][i][index]
					dict = generate_json(item,specific_list[number])
					temp_list.append(dict)
				json_list.append(temp_list)

			# print(json_list)
			for index,item in enumerate(json_list):
				temp = {
					"goodsId":goodsId,
					"inventory":0,
					"price":9999,
					"picture":"https://localhost/uploads/goods/sku/2024101211382_d64c5640_goods.png",
					"specs":json.dumps(item,ensure_ascii=False)
				}
				db.session.add(Sku(**temp))
				db.session.commit()

			return result(200,"generate specs success")
		
		except Exception as e:
			return result(400,str(e))
		
	return result(400,"please use GET method")	






