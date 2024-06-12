from flask import Flask
from config import DevelopmentConfig

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 在这里注册蓝图(Blueprint)
    from app.views.main import bp as main_bp
    from app.views.auth import bp as auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth') 

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