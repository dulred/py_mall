from flask import request, jsonify
import os
import uuid
from app.utils.utils import *
from datetime import datetime, timedelta
from app.views.upload import bp
from config import *
from app.model.users import *



# 上传临时主图
@bp.route('/api/upload/tmp/main', methods=['POST'])
def goods_main_tmp_pages():
    if 'file' not in request.files:
        return result(404,'No file part')

    file = request.files['file']

    if file.filename == '':
        return result(400,'file isEmpty')

    if file and allowed_file(file.filename):
        # 生成新的文件名
        filename = generate_filename(file.filename)
        file_path = os.path.join(GOODS_MAIN_TMP_FOLDER_URL,filename)
        file.save(file_path)
        return result(200,'File uploaded successfully',{'http_url': f"{GOODS_MAIN_TMP_HTTP_URL}{filename}"})
    else:
        return result(400,'Invalid file type. Allowed types: png, jpg, jpeg, gif')


# 上传临时thumb图
@bp.route('/api/upload/tmp/thumb', methods=['POST'])
def goods_thumb_tmp_pages():
    if 'file' not in request.files:
        return result(404,'No file part')

    file = request.files['file']

    if file.filename == '':
        return result(404,'file isEmpty')

    if file and allowed_file(file.filename):
        # 生成新的文件名
        filename = generate_filename(file.filename)
        file_path = os.path.join(GOODS_THUMB_TMP_FOLDER_URL,filename)
        file.save(file_path)
        return result(200,'File uploaded successfully',{'http_url': f"{GOODS_THUMB_TMP_HTTP_URL}{filename}"})
    else:
        return result(400,'Invalid file type. Allowed types: png, jpg, jpeg, gif')
    

# 上传临时详细图
@bp.route('/api/upload/tmp/detail', methods=['POST'])
def goods_detail_tmp_pages():
    if 'file' not in request.files:
        return result(404,'No file part')

    file = request.files['file']

    if file.filename == '':
        return result(404,'file isEmpty')

    if file and allowed_file(file.filename):
        # 生成新的文件名
        filename = generate_filename(file.filename)
        file_path = os.path.join(GOODS_DETAIL_TMP_FOLDER_URL,filename)
        file.save(file_path)
        return result(200,'File uploaded successfully',{'http_url': f"{GOODS_DETAIL_TMP_HTTP_URL}{filename}"})
    else:
        return result(400,'Invalid file type. Allowed types: png, jpg, jpeg, gif')


# 上传临时sku图
@bp.route('/api/upload/tmp/sku', methods=['POST'])
def goods_sku_tmp_pages():
    if 'file' not in request.files:
        return result(404,'No file part')

    file = request.files['file']

    if file.filename == '':
        return result(404,'file isEmpty')

    if file and allowed_file(file.filename):
        # 生成新的文件名
        filename = generate_filename(file.filename)
        file_path = os.path.join(GOODS_SKU_TMP_FOLDER_URL,filename)
        file.save(file_path)
        return result(200,'File uploaded successfully',{'http_url': f"{GOODS_SKU_TMP_HTTP_URL}{filename}"})
    else:
        return result(400,'Invalid file type. Allowed types: png, jpg, jpeg, gif')


# 上传avatar图,利用token，查出用户id，覆盖入库，删除原来的文件，生成新的文件
@bp.route('/api/upload/avatar', methods=['POST'])
def avatar_pages():
    if 'file' not in request.files:
        return result(404,'No file part')

    file = request.files['file']

    if file.filename == '':
        return result(404,'file isEmpty')

    if file and allowed_file(file.filename):
        # 生成新的文件名
        filename = generate_filename(file.filename)
        file_path = os.path.join(GOODS_AVATAR_FOLDER_URL,filename)
        file.save(file_path)

        # 1.查询是否被禁用或者注销 2.覆盖入库，并删除原来的文件 to do
        token = request.headers.get('Authorization')
        if not token:
            return result(401,'Token is missing')

        payload = verify_token(token)
        if 'error' in payload:
            return  result(401,payload)

        user_id = payload['user_id']
        user = db.session.query(User).filter(User.id == user_id).first()
        user.avatar =  f"{GOODS_AVATAR_HTTP_URL}{filename}"
        db.session.commit()

        return result(200,'File uploaded successfully',{'avatar': f"{GOODS_AVATAR_HTTP_URL}{filename}"})
    else:
        return result(400,'Invalid file type. Allowed types: png, jpg, jpeg, gif')



# # 定期调用此函数进行清理 todo
# TEMP_UPLOAD_FOLDER = 'temp_uploads'
# EXPIRATION_TIME = timedelta(hours=1)  # 1小时后删除
# def clean_temp_files():
#     now = datetime.now()
#     for filename in os.listdir(TEMP_UPLOAD_FOLDER):
#         file_path = os.path.join(TEMP_UPLOAD_FOLDER, filename)
#         file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
#         if now - file_creation_time > EXPIRATION_TIME:
#             os.remove(file_path)
#             print(f'Deleted expired file: {file_path}')

