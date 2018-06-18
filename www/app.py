#!usr/bin/python3
#-*- coding: utf-8 -*-

'''
	******************
	*       App      *
	******************
	     Powered By %s
'''

__author__ = 'Shadaileng'

from aiohttp import web
from routes import set_route
from settings import config

def server():
	app = web.Application()
	set_route(app)
	app['config'] = config
	web.run_app(app)






if __name__ == '__main__':
	print(__doc__ % __author__)
	server()
