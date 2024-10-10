'''
Author: yzs dulred@qq.com
Date: 2024-06-12 15:30:54
LastEditors: yzs dulred@qq.com
LastEditTime: 2024-07-01 10:52:39
FilePath: \py_mall\app\__init__.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from flask import Flask, g,request,send_from_directory
from config import *
from app.model import *
from app.utils.utils import *
from flask_cors import CORS

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)
    with app.app_context():
        db.init_app(app)
        db.create_all()
 
    # 在这里注册蓝图(Blueprint)
    from app.views.goods import bp as goods_bp
    from app.views.address import bp as address_bp
    from app.views.orders import bp as orders_bp
    from app.views.user import bp as user_bp
    from app.views.upload import bp as upload_bp
    from app.views.category import bp as category_bp
    from app.views.sw import bp as sw_bp
    from app.views.carousel import bp as carousel_bp
    from app.views.thumb import bp as thumb_bp
    from app.views.detail import bp as detail_bp
    from app.views.sku import bp as sku_bp
    from app.views.specs import bp as specs_bp
    from app.views.goodsStyle import bp as goodsStyles_bp
    from app.views.cart import bp as cart_bp
    from app.views.delivery import bp as delivery_bp
    from app.views.pay import bp as pay_bp
    app.register_blueprint(goods_bp)
    app.register_blueprint(address_bp) 
    app.register_blueprint(orders_bp) 
    app.register_blueprint(user_bp) 
    app.register_blueprint(upload_bp) 
    app.register_blueprint(category_bp) 
    app.register_blueprint(sw_bp) 
    app.register_blueprint(carousel_bp) 
    app.register_blueprint(detail_bp) 
    app.register_blueprint(thumb_bp) 
    app.register_blueprint(sku_bp)
    app.register_blueprint(specs_bp)
    app.register_blueprint(goodsStyles_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(delivery_bp)
    app.register_blueprint(pay_bp)

    # 创建商品主图临时上传目录（如果不存在）
    if not os.path.exists(GOODS_MAIN_TMP_FOLDER_URL):
        os.makedirs(GOODS_MAIN_TMP_FOLDER_URL)

    # 创建主图上传目录（如果不存在）
    if not os.path.exists(GOODS_MAIN_FOLDER_URL):
        os.makedirs(GOODS_MAIN_FOLDER_URL)


    # 创建主页首尾图临时上传目录（如果不存在）
    if not os.path.exists(GOODS_SW_TMP_FOLDER_URL):
        os.makedirs(GOODS_SW_TMP_FOLDER_URL)

    # 创建主页首尾图上传目录（如果不存在）
    if not os.path.exists(GOODS_SW_FOLDER_URL):
        os.makedirs(GOODS_SW_FOLDER_URL)



    # 创建轮播图临时上传目录（如果不存在）
    if not os.path.exists(GOODS_CAROUSEL_TMP_FOLDER_URL):
        os.makedirs(GOODS_CAROUSEL_TMP_FOLDER_URL)

    # 创建轮播图上传目录（如果不存在）
    if not os.path.exists(GOODS_CAROUSEL_FOLDER_URL):
        os.makedirs(GOODS_CAROUSEL_FOLDER_URL)


    # 创建缩略图临时上传目录（如果不存在）
    if not os.path.exists(GOODS_THUMB_TMP_FOLDER_URL):
        os.makedirs(GOODS_THUMB_TMP_FOLDER_URL)
    # 创建缩略图上传目录（如果不存在）
    if not os.path.exists(GOODS_THUMB_FOLDER_URL):
        os.makedirs(GOODS_THUMB_FOLDER_URL)


    # 创建详细图临时上传目录（如果不存在）
    if not os.path.exists(GOODS_DETAIL_TMP_FOLDER_URL):
        os.makedirs(GOODS_DETAIL_TMP_FOLDER_URL)
    # 创建详细图临时上传目录（如果不存在）
    if not os.path.exists(GOODS_DETAIL_FOLDER_URL):
        os.makedirs(GOODS_DETAIL_FOLDER_URL)


    # 创建sku临时上传目录（如果不存在）
    if not os.path.exists(GOODS_SKU_TMP_FOLDER_URL):
        os.makedirs(GOODS_SKU_TMP_FOLDER_URL)
    # 创建sku上传目录（如果不存在）
    if not os.path.exists(GOODS_SKU_FOLDER_URL):
        os.makedirs(GOODS_SKU_FOLDER_URL)

    
    # 创建avatar图上传目录（如果不存在）
    if not os.path.exists(GOODS_AVATAR_FOLDER_URL):
        os.makedirs(GOODS_AVATAR_FOLDER_URL)

    

    # 请求拦截器    
    @app.before_request
    def before():
        url = request.path #当前请求的URL
        passUrl = WHITE_NAME_LIST

        if url in passUrl:
            pass
        elif "/ntk" in url:
            pass
        elif "/uploads" in url:
            pass
        else:
            if request.method == 'OPTIONS':
                return '', 200  # 直接返回 200 对预检请求放行
            token = request.headers.get('Authorization')
            if not token:
                return result(401,{'error': 'Token is missing'})
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                g.user_id = payload['user_id']
            except jwt.ExpiredSignatureError:
                    return result(401,'Token expired')
            except jwt.InvalidTokenError:
                    return result(401,'Invalid token')
            pass

        # if url in passUrl:
        #     pass 
        # elif "/static" in url:
        #     pass
        # elif "/api/goods/detail/" in url:
        #     pass 
        # elif "/upload" in url:
        #     pass 
        # else:
        #     token = request.headers.get('Authorization')
        #     if not token:
        #         return result(401,{'error': 'Token is missing'})
            
        #     payload = verify_token(token)
        #     if 'error' in payload:
        #         return result(401,payload)
        #     g.user_id = payload['user_id']
        #     pass


    # 实现主图url映射
    @app.route('/uploads/tmp/main/<path:filename>')
    def tmp_main_files(filename):
        return send_from_directory(GOODS_MAIN_TMP_FOLDER_URL, filename)
    
    @app.route('/uploads/main/<path:filename>')
    def main_files(filename):
        return send_from_directory(GOODS_MAIN_FOLDER_URL, filename)
    

    # 实现首尾映射
    @app.route('/uploads/tmp/home/sw/<path:filename>')
    def tmp_sw_files(filename):
        return send_from_directory(GOODS_SW_TMP_FOLDER_URL, filename)
    
    @app.route('/uploads/home/sw/<path:filename>')
    def sw_files(filename):

        return send_from_directory(GOODS_SW_FOLDER_URL, filename)

    # 实现轮播图映射
    @app.route('/uploads/tmp/home/carousel/<path:filename>')
    def tmp_carousel_files(filename):
        return send_from_directory(GOODS_CAROUSEL_TMP_FOLDER_URL, filename)
    
    @app.route('/uploads/home/carousel/<path:filename>')
    def carousel_files(filename):
        return send_from_directory(GOODS_CAROUSEL_FOLDER_URL, filename)
    

    # 实现商品缩略图映射
    @app.route('/uploads/tmp/goods/thumb/<path:filename>')
    def tmp_thumb_files(filename):
        return send_from_directory(GOODS_THUMB_TMP_FOLDER_URL, filename)
    
    @app.route('/uploads/goods/thumb/<path:filename>')
    def thumb_files(filename):
        return send_from_directory(GOODS_THUMB_FOLDER_URL, filename)


    # 实现商品详情图映射
    @app.route('/uploads/tmp/goods/detail/<path:filename>')
    def tmp_detail_files(filename):
        return send_from_directory(GOODS_DETAIL_TMP_FOLDER_URL, filename)
    
    @app.route('/uploads/goods/detail/<path:filename>')
    def detail_files(filename):
        return send_from_directory(GOODS_DETAIL_FOLDER_URL, filename)
    

    # 实现sku图映射
    @app.route('/uploads/tmp/goods/sku/<path:filename>')
    def tmp_sku_files(filename):
        return send_from_directory(GOODS_SKU_TMP_FOLDER_URL, filename)
    
    @app.route('/uploads/goods/sku/<path:filename>')
    def sku_files(filename):
        return send_from_directory(GOODS_SKU_FOLDER_URL, filename)

    # 实现avatar图映射
    @app.route('/uploads/avatar/<path:filename>')
    def avatar_files(filename):
        return send_from_directory(GOODS_AVATAR_FOLDER_URL, filename)

    # 实现font字体库文件的映射
    @app.route('/uploads/font/<path:filename>')
    def font_files(filename):
        return send_from_directory(FONT_FOLDER_URL, filename)

    return app

""" 
这是一个简化版的 `app/__init__.py` 文件,只包含 `create_app` 函数:
这个简化版的 `__init__.py` 文件只完成了以下几个基本任务:

1. 从 Flask 导入 `Flask` 类。
2. 从 `config.py` 导入配置对象 `Config`。
3. 定义了 `create_app` 函数,作为应用的工厂函数。
4. 在 `create_app` 函数中:
   - 创建了 Flask 应用实例 `app`。
   - 从配置对象 `Config` 加载了应用配置。
   - 导入并注册了一个名为 `main` 的蓝图(Blueprint)。
5. 返回已创建并配置好的 Flask 应用实例 `app`。

这是一个最小化的 Flask 应用工厂函数实现,适合用于小型项目或者作为学习的入门示例。在实际的生产级应用中,您可能还需要在 `create_app` 函数中进行更多的配置和初始化操作,例如:

- 初始化数据库
- 注册更多的蓝图
- 配置日志记录
- 加载中间件
- 注册错误处理程序
- 等等

但是,这个简化版的 `__init__.py` 文件已经展示了 Flask 应用工厂模式的基本结构和思路,您可以在此基础上根据需要进行扩展和定制。

 """