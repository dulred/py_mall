import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "123.com"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{ipaddress}:{port}/{database}".format(username="root",password="123456",ipaddress="192.168.1.26",port="3306",database="mall")
    SQLALCHEMY_TRACK_MODIFICATIONS = True#动态追踪修改设置
    SQLALCHEMY_ECHO = True 

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

WHITE_NAME_LIST = ["/api/login","/api/regist","/api/goods/type","/api/by/tag/goods","/payforme"]

""" 
这个配置文件包含以下几个部分:

导入 os 模块,用于获取操作系统相关的一些信息。
定义 basedir 变量,存储当前文件所在的绝对路径,方便后续引用。
定义基本配置类 Config。该类包含一些常用的配置项:

SECRET_KEY: Flask应用的秘钥,用于安全相关的功能。
SQLALCHEMY_DATABASE_URI: SQLAlchemy 数据库连接URI,可以从环境变量中获取,也可以设置为本地 SQLite 数据库文件。
SQLALCHEMY_TRACK_MODIFICATIONS: 设置为 False 以禁用对象的修改跟踪,从而提高性能。


定义了两个继承自 Config 的子类:

DevelopmentConfig: 开发环境配置,将 DEBUG 模式设置为 True。
ProductionConfig: 生产环境配置,将 DEBUG 模式设置为 False。



在应用程序中,您可以根据不同的环境导入并使用相应的配置类。例如,在开发环境中使用 DevelopmentConfig,而在生产环境中使用 ProductionConfig。
 """