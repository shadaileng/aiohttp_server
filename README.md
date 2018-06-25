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
│       ├── __init__.py
│       ├── __main__.py
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

def server():
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
# routes.py
from www.views import index

def set_routes(app):
	app.router.add_get('/', index)

# app.py
from aiohttp import web

app = web.Application()
set_routes(app)
web.run_app(app)
```

> 将文件夹`www`当作一个模块,新建文件`__init__.py`和`__main__.py`

```
# __main__.py
from www.app import server

server()
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
        ├── __init__.py
        ├── __main__.py
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
    │   ├── __init__.py
    │   ├── __main__.py
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
config['BASC_DIR'] = BASC_DIR
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

## 视图模板

> 模板可以很方便地编写网页。只需要在`aophttp_jinjia2.template`注解标注的`view`函数返回页面需要数据的字典，就可以在页面上希纳是信息

> 首先要安装`aophttp_jinjia2`模块

```
$ pip3 install aophttp_jinjia2
```

> `www`模块下新建文件夹`templates`，放入模板文件

> 应用程序加载模板

```
# app.py
import aiohttp_jinja2
import jinja2

aiohttp_jinja2.setup(
    app, loader=jinja2.PackageLoader('www', 'templates'))
# aiohttp_jinja2.setup(
#    app, loader=jinja2.FileSystemLoader('./www/templates'))
```

> 请求处理函数标注模板，并返回数据

```
# views.py

import aiohttp_jinja2

@aiohttp_jinja2.template('index.html')
async def index(request):
  res = {'a': 1, 'b'： 2}
  return res

```

## 处理静态文件

> 项目目录下新建静态文件文件夹`static`,为应用程序添加静态路由

```
# routes.py

def set_route(app):
  app.router.add_get('/', index)
  set_static_route(app)

def set_static_route(app):
  app.router.add_static('/static/', path=config['BASC_DIR'] + '/static', name='static')
```

## 中间件

> 中间件堆放在`web`处理函数周围，在预处理请求的处理程序之前被调用，并且在得到响应以用于后处理给定的响应之后被调用。

> 每个中间件都接受请求`request`和处理函数`handler`两个参数，返回响应`response`。中间件时处理请求或者响应的协同程序。

```
import aiohttp_jinja2
from aiohttp import web

async def handle_404(request):
  return aiohttp_jinja2.render_template('404.html', request, {})

async def handle_500(request):
  return aiohttp_jinja2.render_template('500.html', request, {})

def create_error_middleware(overrides):
  @web.middleware
  async def error_middelware(request, handler):

    try:
      response = await handler(request)
      override = overrides.get(response.status)
      if override:
        return await override(request)
      return response
    except web.HTTPException as e:
      logging.error('error middleware: %s' % e)
      override = overrides.get(e.status)
      if override:
        return await override(request)
  return error_middelware

def set_middleware(app):
  
  ''' 
  500 - web.HTTPInternalServerError(text="测试中间件")
  404 - web.HTTPNotFound(text="测试中间件")
  '''
  error_middelware = create_error_middleware({404: handle_404, 500: handle_500})
  app.middlewares.append(error_middelware)
```

> 根据处理函数`handler`处理请求`request`得到响应`response`的状态码来选择`jinja2`要渲染的模板。

> 如果处理函数在处理请求时抛出异常(`Internal Error`对应状态码`500`,`NotFound`对应状态码`404`)，捕获`web.HTTPException`异常，并根据其状态码选择选渲染模板。

## 表单

> 如果表单函数是`get`(`<form method='get'>`),可以使用`Request.query`获取参数。

```
async def index(request):
  for k, v in request.query.items():
    print('%s: %s' % (k, v))
```

> 如果表单函数是`post`, 可以使用`Request.post()`或者`Request.multipart()`接受数据。

> `Request.post()`支持`application/x-www-form-urlencoded`和`multipart/form-data`两种数据编码，上传的文件数据会保存到临时文件夹。

```
# 表单
<form method='post' accept-charset='utf-8' enctype='application/x-www-form-urlencoded'>
  <label for="name">name</label>
  <input type="text" name="name" value=""><br><br>
  <label for="password">password</label>
  <input type="password" name="password" value=""><br><br>
  <input type="submit" value="login"/>
</form>

# 后台接收数据
async def login_post(request):
  data = await request.post()
  name = data['name']
  password = data['password']
```

## 文件上传

> 首先设置表单数据编码`enctype="multipart/form-data"`

```
<form method="post" action="/upload" enctype="multipart/form-data">
  <label for="file">file</label>
  <input type="file" name="file" value=""><br><br>
  <input type="submit" value="upload"/>
</form>
```

> 通过`Request.post()`将上传的文件写入到内存中，然后根据文件字段取对应的文件信息.

```
async def upload(request):
  data = await request.post()
  file = data['file']
  filename = file.filename
  file_ = file.file
  with open('./' + filename, 'wb') as f:
    data = file_.read()
    f.write(data)
```

> 如果上传的文件过大，可能会包内存溢出的异常。为了解决这个问题，可以分块读取文件。

```
async def upload(request):
  reader = await request.multipart()
  data = await reader.next()
  filename = data.filename
  with open('./' + filename, 'wb') as f:
    while True:
      # 默认每次读取8192字节
      chunk = await data.read_chunk()
      if not chunk:
        break
      print(len(chunk))
      f.write(chunk)
```