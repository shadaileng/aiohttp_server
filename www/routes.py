#!usr/bin/python3
#-*- coding: utf-8 -*-

'''
	******************
	*      Routes    *
	******************
	     Powered By %s
'''

__author__ = 'Shadaileng'

import logging; logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s line:%(lineno)d %(filename)s %(funcName)s >>> %(message)s')

from .views import index
from .settings import config

def set_route(app):
	app.router.add_get('/', index)
	set_static_route(app)

def set_static_route(app):
	app.router.add_static('/static/', path=config['BASC_DIR'] + '/static', name='static')

if __name__ == '__main__':
	print(__doc__ % __author__)
