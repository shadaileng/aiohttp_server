#!usr/bin/python3
#-*- coding: utf-8 -*-

'''
	******************
	*       App      *
	******************
	     Powered By %s
'''

__author__ = 'Shadaileng'

import logging; logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s line:%(lineno)d %(filename)s %(funcName)s >>> %(message)s')

from aiohttp import web
from .routes import set_route
from .settings import config
from .db import Engine, close_db, init_db
from .middlewares import set_middleware

import aiohttp_jinja2, jinja2

def server():
	app = web.Application()
	app['config'] = config
	# 加载模板
	aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('www', 'templates'))
	# 程序启动和关闭的回调函数
	app.on_startup.append(init_db)
	app.on_cleanup.append(close_db)
	app.on_cleanup.append(clearWebsocket)
	# 添加中间件
	set_middleware(app)
	# 设置websockets
	app['websockets'] = {}
	# 设置路由
	set_route(app)
	# 启动程序
	web.run_app(app)


async def clearWebsocket(app):
	print('=======================')
	for ws in app['websockets'].values():
		await ws.close()
	app['websockets'].clear()



if __name__ == '__main__':
	print(__doc__ % __author__)
	server()
