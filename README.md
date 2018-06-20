# <center>aiohttp server</center>

> 使用`aiohttp`编写一个服务器

## 基础框架

```
├── aiohttp
│   ├── static
│   │   ├── images
│   │   │   └── background.png
│   │   └── style.css
│   ├── templates
│   │   ├── 404.html
│   │   ├── 500.html
│   │   ├── base.html
│   │   ├── detail.html
│   │   ├── index.html
│   │   └── results.html
│   └── www 
│       ├── db.py
│       ├── app.py
│       ├── models.py
│       ├── middlewares.py
│       ├── routes.py
│       ├── settings.py
│       ├── utils.py
│       └── views.py
├── config
│   │
│   └── default.yaml
├── tests
│   ├── conftest.py
│   ├── __init__.py
│   └── test_integration.py
├── init_db.py
├── Makefile
├── README.md
├── requirements.txt
├── setup.py
└── tox.ini
```

## 环境

> linux
```
$ virtualenv --no-site-package venv
$ source venv/bin/activate
```

> win
```
> virtualenv --no-site-package venv
> venv/Scrits/activate.bat
```

## 简单服务

> `aiohttp`服务是围绕`aiohttp.web.Application`实体建立的,它用于注册启动/清理信号，连接路线等。

> 安装`aiohttp`模块

```
$ pip3 install aiohttp
```

> 创建一个服务应用

```
# app.py
from aiohttp import web

app = web.Application()
web.run_app(app)
```

> 创建视图

```
# views.py
from aiohttp import web

async def index(request):
	return web.Response(text='Hello Aiohttp')
```

> 为视图注册路由

```
#routes.py
from www.views import index

def set_routes(app):
	app.router.add_get('/', index)

# app.py
from aiohttp import web

app = web.Application()
set_routes(app)
web.run_app(app)
```

> 运行`app.py`

```
$ python3 -m www
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)
```

> 浏览器访问`localhost:8080`, 浏览器显示结果
```
Hello Aiohttp!
```

> 基本的项目文件如下

```
├── aiohttp
    └── www
        ├── app.py
        ├── views.py
        └── routes.py
```

## 配置文件

> 使用`yaml`进行配置项目

```
$ pip3 install pyyaml
```

> 在项目目录下创建`config`文件夹，并新建配置文件`default.yaml`

```
├── aiohttp
    ├── www
    │   ├── app.py
    │   ├── views.py
    │   └── routes.py
    └── config
        └── default.yaml

# default.yaml
db:
  database: ./res/test.db
  user: 
  password: 
  host:
  port:
```

> `settings.py`模块加载配置文件

```
# settings.py
import yaml, os

BASC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = BASC_DIR + '/config/default.yaml'

def get_config(path):
	with open(path) as file:
		config = yaml.load(file)
	return config

config = get_config(config_path)
```

> 服务应用中加载配置

```
# app.py

from aiohttp import web
from www.routes import set_route
from www.settings import config

def server():
	app = web.Application()
	set_route(app)
	app['config'] = config
	web.run_app(app)
```

## 数据库

> 搭建一个可以创建数据库连接、查询和修改数据的框架。新建文件`db.py`

```
class Engine(object):
  ....

class Connection(object):
  """docstring for Connection"""
  ....
```


> 搭建一个`ORM`框架，执行`UDIQ`。新建文件`models.py`

```
class Column(object):
  ....
class TableMetaClass(type):
  ....
class Table(dict, metaclass=TableMetaClass):
  ....
class File(Table):
  ....
class User(Table):
  ....
class Blog(Table):
  ....
class Comment(Table):
  ....

```

> 初始化数据库，执行`db.py`文件

```
$ python3 www/db.py
```

> 应用记录`Engine`，并注册关闭程序资源回收函数

```
# app.py
from aiohttp import web
from www.routes import set_route
from www.settings import config
from www.db import Engine

def server():
	app = web.Application()
	set_route(app)
	app['config'] = config
	app['db'] = Engine(config['db']['database'], '', '', '', '')
	app.on_cleanup.append(app['db'].close)
	web.run_app(app)
```

