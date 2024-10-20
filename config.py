import os

# 开发和生产环境的域名
DOMAIN_PRODUCTION ="https://www.guagnximisa.top"
DOMAIN_DEVELOPMENT="https://localhost"

# 数据库的生产和开发环境
DEV_MYSQL_IP = "192.168.1.253"
PRO_MYSQL_IP = "127.0.0.1"
#是否是开发环境 
ISDEV = True
DOMAIN = DOMAIN_DEVELOPMENT
MYSQL_IP = DEV_MYSQL_IP
if ISDEV:
    DOMAIN = DOMAIN_DEVELOPMENT
    MYSQL_IP = DEV_MYSQL_IP
else:
    DOMAIN = DOMAIN_PRODUCTION
    MYSQL_IP = PRO_MYSQL_IP


# 获取根路径
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "123.com"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{ipaddress}:{port}/{database}".format(username="root",password="123456",ipaddress=MYSQL_IP,port="3306",database="mall")
    SQLALCHEMY_TRACK_MODIFICATIONS = True#动态追踪修改设置
    SQLALCHEMY_ECHO = True 

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# 白名单
WHITE_NAME_LIST = ["/api/login","/api/login/wxMin/simple","/api/admin"]

# 字体图文件
FONT_FOLDER_URL = "D:\\dulred\\dev\\uploads\\font"

# --商品主图
# 上传临时主图文件目录路径
GOODS_MAIN_TMP_FOLDER_URL = "D:\\dulred\\dev\\uploads\\goods\\tmp\\main"
# 上传主图文件目录路径
GOODS_MAIN_FOLDER_URL = "D:\\dulred\\dev\\uploads\\goods\\main"

# 临时主图https路径
GOODS_MAIN_TMP_HTTP_URL =f"{DOMAIN}/uploads/tmp/main/"   #部署其他地方localhost这个要改
# 主图https路径
GOODS_MAIN_HTTP_URL =f"{DOMAIN}/uploads/main/"   #部署其他地方localhost这个要改




# --首尾图
# 上传临时首页首图文件目录路径
GOODS_SW_TMP_FOLDER_URL = "D:\\dulred\\dev\\uploads\\home\\sw\\tmp"
# 上传首页尾图文件目录路径
GOODS_SW_FOLDER_URL = "D:\\dulred\\dev\\uploads\\home\\sw"

# 首页尾图https路径
GOODS_SW_HTTP_URL =f"{DOMAIN}/uploads/home/sw/" #部署其他地方localhost这个要改  
# 临时首页尾图https路径
GOODS_SW_TMP_HTTP_URL =f"{DOMAIN}/uploads/tmp/home/sw/" #部署其他地方localhost这个要改  





# --轮播图（跟goods的id关联）
# 上传临时首页首图文件目录路径
GOODS_CAROUSEL_TMP_FOLDER_URL = "D:\\dulred\\dev\\uploads\\home\\carousel\\tmp"
# 上传首页尾图文件目录路径
GOODS_CAROUSEL_FOLDER_URL = "D:\\dulred\\dev\\uploads\\home\\carousel"

# 首页尾图https路径
GOODS_CAROUSEL_HTTP_URL =f"{DOMAIN}/uploads/home/carousel/" #部署其他地方localhost这个要改  
# 临时首页尾图https路径
GOODS_CAROUSEL_TMP_HTTP_URL =f"{DOMAIN}/uploads/tmp/home/carousel/" #部署其他地方localhost这个要改  




# --商品详细页thumb图
# 上传临时缩略图文件目录路径
GOODS_THUMB_TMP_FOLDER_URL = "D:\\dulred\\dev\\uploads\\goods\\tmp\\thumb"
# 上传缩略图文件目录路径
GOODS_THUMB_FOLDER_URL = "D:\\dulred\\dev\\uploads\\goods\\thumb"

# 临时首页尾图https路径
GOODS_THUMB_HTTP_URL =f"{DOMAIN}/uploads/goods/thumb/" #部署其他地方localhost这个要改  
# 首页尾图https路径
GOODS_THUMB_TMP_HTTP_URL =f"{DOMAIN}/uploads/tmp/goods/thumb/" #部署其他地方localhost这个要改  



# --商品详细页detail图
# 上传临时详细图文件目录路径
GOODS_DETAIL_TMP_FOLDER_URL = "D:\\dulred\\dev\\uploads\\goods\\tmp\\detail"
# 上传详细图文件目录路径
GOODS_DETAIL_FOLDER_URL = "D:\\dulred\\dev\\uploads\\goods\\detail"

# 临时首页尾图https路径
GOODS_DETAIL_HTTP_URL =f"{DOMAIN}/uploads/goods/detail/" #部署其他地方localhost这个要改  
# 首页尾图https路径
GOODS_DETAIL_TMP_HTTP_URL =f"{DOMAIN}/uploads/tmp/goods/detail/" #部署其他地方localhost这个要改  




# --sku图
# 上传临时sku图文件目录路径
GOODS_SKU_TMP_FOLDER_URL = "D:\\dulred\\dev\\uploads\\goods\\tmp\\sku"
# 上传sku图文件目录路径
GOODS_SKU_FOLDER_URL = "D:\\dulred\\dev\\uploads\\goods\\sku"

# 临时sku图https路径
GOODS_SKU_HTTP_URL =f"{DOMAIN}/uploads/goods/sku/" #部署其他地方localhost这个要改  
# sku图https路径
GOODS_SKU_TMP_HTTP_URL =f"{DOMAIN}/uploads/tmp/goods/sku/" #部署其他地方localhost这个要改 



# 上传avatar图文件目录路径
GOODS_AVATAR_FOLDER_URL = "D:\\dulred\\dev\\uploads\\avatar"

# avatar图https路径
GOODS_AVATAR_HTTP_URL =f"{DOMAIN}/uploads/avatar/" #部署其他地方localhost这个要改  




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