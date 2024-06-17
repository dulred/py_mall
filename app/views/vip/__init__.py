from flask import Blueprint

bp = Blueprint('vip', __name__)

from app.views.vip import bp


""" 
在 Flask 应用中，最后一行 from app.main import routes 是必要的，即使它看起来不直接使用。以下是为什么这行代码至关重要的详细解释。

为什么需要 from app.main import routes
加载路由定义: Flask 蓝图(Blueprint)并不会自动发现和注册它的路由。你必须显式地加载定义路由的模块。from app.main import routes 确保路由文件 routes.py 被导入，这样 Flask 才能识别并注册蓝图中的所有路由。

避免循环导入: 如果你在 routes.py 中直接访问 bp 而不通过 __init__.py，可能会导致循环导入问题。通过在 __init__.py 中导入 routes，你可以避免这个问题，因为导入顺序和作用域管理得更好。

确保执行路由注册代码: 路由文件 routes.py 通常包含注册路由的代码。如果不导入它，路由注册代码不会被执行，从而导致路由无法生效。导入模块时，模块中的顶级代码会执行，从而注册路由。 
"""