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
from www.routes import set_route
from www.settings import config
from www.db import Engine

import aiohttp_jinja2, jinja2

def server():
	app = web.Application()
	set_route(app)
	app['config'] = config
	app['db'] = Engine(config['db']['database'], '', '', '', '')
	aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('www', 'templates'))
	app.on_cleanup.append(app['db'].close)
	web.run_app(app)






if __name__ == '__main__':
	print(__doc__ % __author__)
	server()
