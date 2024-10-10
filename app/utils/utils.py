import hashlib
import random
import time 
from datetime import datetime,timedelta
import uuid
from flask import jsonify
import shutil
import os
import pytz
def result(code=200,msg='处理成功!',d={}):
    data = dict()#object.__dict__
    data['code'] = code
    data['msg'] = msg
    data['result'] = d
    response = jsonify({'code':code,'msg': msg,'result':d})
    response.status_code = code
    return response

def md5(m):
	return hashlib.md5(m.encode()).hexdigest()

def getNowDataTime():
	return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

def getTimeStamp():
	return time.time()

def getOrderNum():
	orderNum = str(getTimeStamp()).replace('.','')
	return orderNum

def moveFile(file_path,temp_dir,target_dir):
	# 临时路径
	tmp_file_path = os.path.join(temp_dir, os.path.basename(file_path))
	# 定义目标文件路径
	final_file_path = os.path.join(target_dir, os.path.basename(file_path))
	# 移动文件
	shutil.move(tmp_file_path, final_file_path)






import jwt

# 配置密钥和算法
SECRET_KEY = 'misha777'
ALGORITHM = 'HS256'

#生成token
def create_token(user_id):
    expiration = datetime.utcnow() + timedelta(hours=720)
    payload = {
        'user_id': user_id,
        'exp': expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token
# 验证token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # 成功解码，返回有效载荷
    except jwt.ExpiredSignatureError:
        return result(401,'Token expired')
    except jwt.InvalidTokenError:
        return result(401,'Invalid token')

# 从token获取信息
def get_user_from_token(token):
    payload = verify_token(token)
    if 'error' in payload:
        return result(401,'Token 无效或过期')  # Token 无效或过期
    return payload['user_id']

# 生成订单编号 (时间戳加随机数)
def generate_order_number():
    current_datetime = datetime.now()
    timestamp = int(current_datetime.timestamp()* 1000)  # 当前时间戳（毫秒）
    random_number = random.randint(1000, 9999)  # 4 位随机数
    order_number = f"{timestamp}{random_number}"
    return order_number

# 假设这些数据是从某个数据源获取的
provinces = {
    "110000": "北京市",
    "02": "Shanghai",
    "03": "Guangdong",
    # 其他省份
}

cities = {
    "110100": "北京市",
    "0102": "Xicheng",
    "0201": "Huangpu",
    # 其他城市
}

counties = {
    "110101": "东城区",
    "010102": "Tiananmen",
    "020101": "Nanjing Road",
    # 其他县区
}

def get_full_location(province_code, city_code, county_code):
    # 获取省份
    province = provinces.get(province_code, "xx")
    
    # 获取城市
    city = cities.get(city_code, "xx")
    
    # 获取县区
    county = counties.get(county_code, "xx")
    
    # 构建完整地址
    full_location = f"{province} {city} {county}"
    
    return full_location






def gmt_to_Shanghai(str_dataTime):

    if not str_dataTime:
         return ''

    # 创建上海时区对象
    shanghai_tz = pytz.timezone("Asia/Shanghai")

    # 将 GMT 时间转换为上海时间
    gmt_time = pytz.utc.localize(str_dataTime)  # 转换为带时区的 UTC 时间
    shanghai_time = gmt_time.astimezone(shanghai_tz)

    # 格式化为指定的字符串格式
    formatted_time = shanghai_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time





# 配置上传目录
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_filename(original_filename):
    """生成新的文件名"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:13]  # 年月日时分秒毫秒
    unique_id = str(uuid.uuid4().hex[:8])  # 8位UUID
    file_extension = original_filename.rsplit('.', 1)[1].lower()  # 原文件扩展名
    return f"{timestamp}_{unique_id}_goods.{file_extension}"

