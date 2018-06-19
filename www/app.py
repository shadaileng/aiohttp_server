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
from routes import set_route
from settings import config
from db import Engine

def server():
	app = web.Application()
	set_route(app)
	app['config'] = config
	app['db'] = Engine(config['db']['database'], '', '', '', '')
	web.run_app(app)






if __name__ == '__main__':
	print(__doc__ % __author__)
	server()
