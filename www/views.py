#!usr/bin/python3
#-*- coding: utf-8 -*-

'''
	******************
	*      Views     *
	******************
	     Powered By %s
'''

__author__ = 'Shadaileng'

import logging; logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s line:%(lineno)d %(filename)s %(funcName)s >>> %(message)s')

import asyncio, aiohttp_jinja2

from aiohttp import web
from www.models import File

@aiohttp_jinja2.template('index.html')
async def index(request):
	file = File()
	res = await file.find(request.app['db'])
#	print('res: %s' % res)
#	return web.Response(text='Hello Aiohttp')
	return res

if __name__ == '__main__':
	print(__doc__ % __author__)
