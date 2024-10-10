<!-- 启动本项目 --> （使用python 3.10.6）
python -m venv venv

venv\Scripts\activate

python -m pip install -r requirements.txt

<!-- 
还要配置和安装好mysql数据库
然后看config.py 这个配置文件里面根据自己修改用户名和密码，还需要创建一个mall 的 数据库
 -->
python run.py

修改完要使用 freeze 导入修改的依赖(如果有的话)
python -m pip freeze > requirements.txt

然后提交git


<!-- 题外话 python -m pip install cryptography-->
<!-- 创建和使用虚拟环境 -->

好的,我将为您总结在不同情况下创建、激活和使用Python虚拟环境的命令:

1. **创建虚拟环境**

   - 使用Python内置的venv模块:
     ```
     python -m venv venv
     ```

   - 使用virtualenv工具:
     ```
     virtualenv env
     ```

2. **激活虚拟环境**

   - Windows:
     ```
     env\Scripts\activate
     ```

   - Linux/macOS: 
     ```
     source env/bin/activate
     ```

   激活后，您的命令行前缀会变为`(env)`。

3. **使用虚拟环境**

   - 安装包:
     ```
     python -m pip install package_name
     ```

   - 运行Python脚本:
     ```
     python -m python script.py
     ```

4. **退出虚拟环境**

   - Windows/Linux/macOS:
     ```
     deactivate
     ```

5. **其他常用命令**

   - 列出所有已安装包:
     ```
     python -m pip list
     ```

   - 查看某个包信息:
     ```
     python -m pip show package_name
     ```

   - 生成requirements.txt文件:
     ```
     python -m pip freeze > requirements.txt
     ```

   - 根据requirements.txt安装所需包:
     ```
     python -m pip install -r requirements.txt
     ```

一些最佳实践:

- 项目根目录下创建并管理虚拟环境
- 将虚拟环境目录添加到`.gitignore`中
- 使用`pip freeze > requirements.txt`保存依赖环境快照
- 不同项目使用不同的虚拟环境
- 在CI/CD过程中重新构建虚拟环境

通过掌握这些命令和最佳实践,您就可以方便地在项目中创建、管理和使用Python虚拟环境了,从而实现更好的代码组织和环境隔离。





<!-- 
Flask作为一个灵活、模块化的Web框架,在构建项目结构时提供了很大的自由度。不过,对于大型项目来说,遵循一定的规范和最佳实践非常重要,这样可以提高代码的可读性、可维护性和可扩展性。以下是一种常见的Flask项目结构:
 -->


```
project/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   └── ...
│   ├── views/
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── auth.py
│   │   └── ...
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── ...
│   └── templates/
│       ├── errors/
│       └── ...
├── config.py
├── requirements.txt
├── run.py
├── tests/
│   └── ...
└── ...
```

- `app/`目录是Flask应用的主要代码所在位置。
- `app/__init__.py`是应用的入口点,用于创建Flask应用实例并注册蓝图等。
- `app/models/`目录存放数据模型相关代码。
- `app/views/`目录存放路由和视图函数相关代码,通常每个功能模块对应一个Python文件。
- `app/static/`目录存放静态文件,如CSS、JavaScript和图片等。
- `app/templates/`目录存放HTML模板文件。
- `config.py`包含应用的配置选项。
- `requirements.txt`列出了项目所需的Python包依赖。
- `run.py`是应用的入口脚本,用于启动Flask开发服务器。
- `tests/`目录存放单元测试代码。

关于使用蓝图(Blueprint),Flask官方文档非常鼓励在大型项目中使用它。蓝图可以将应用分解为一组小的、高度解耦的组件,每个蓝图维护一组与其功能相关的路由和视图函数。Flask官方示例[Larger Applications](https://flask.palletsprojects.com/en/2.2.x/patterns/packages/)就展示了如何使用蓝图构建模块化应用。

在实践中,我们可以将不同的功能模块(如认证、API等)划分为不同的蓝图,在`app/views/`目录下为每个蓝图创建一个Python文件,并在`app/__init__.py`中导入并注册这些蓝图。这种结构可以使项目结构更加清晰,代码更易于管理和扩展。

总之,建立规范化的Flask项目结构并适当使用蓝图,可以极大地提高Flask应用的可维护性和可扩展性,这对于大型项目来说是非常宝贵的。