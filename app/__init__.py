from flask import Flask,request,session
from config import *
from app.model import *
import simplejson as json
from app.utils.utils import *

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    # 在这里注册蓝图(Blueprint)
    from app.views.auth import bp as auth_bp
    from app.views.goods import bp as goods_bp
    from app.views.goodsType import bp as goodsType_bp
    from app.views.address import bp as address_bp
    from app.views.vip import bp as vip_bp
    from app.views.orders import bp as orders_bp
    from app.views.comments import bp as comments_bp
    from app.views.court import bp as court_bp
    from app.views.payforme import bp as payforme_bp
    app.register_blueprint(auth_bp) 
    app.register_blueprint(goods_bp)
    app.register_blueprint(goodsType_bp) 
    app.register_blueprint(address_bp) 
    app.register_blueprint(vip_bp) 
    app.register_blueprint(orders_bp) 
    app.register_blueprint(comments_bp) 
    app.register_blueprint(court_bp) 
    app.register_blueprint(payforme_bp) 

    @app.before_request
    def before():
        try:
            data = json.loads(request.get_data(as_text=True))
            request.form = data
        except:
            pass
        url = request.path #当前请求的URL
        passUrl = WHITE_NAME_LIST
        if url in passUrl:
            pass 
        elif "static" in url:
            pass
        elif "/api/goods/detail/" in url:
            pass 
        else:
            _id = session.get("_id",None)
            if not _id:
                return result(203,{"info":"未登录"})
            else:
                pass 
		
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