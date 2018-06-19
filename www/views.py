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

import asyncio

from aiohttp import web

async def index(request):
	res = await request.app['db'].select('select * from file')
	print('res: %s' % res)
	return web.Response(text='Hello Aiohttp')


if __name__ == '__main__':
	print(__doc__ % __author__)
