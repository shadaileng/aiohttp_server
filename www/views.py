#!usr/bin/python3
#-*- coding: utf-8 -*-

'''
	******************
	*      Views     *
	******************
	     Powered By %s
'''

__author__ = 'Shadaileng'

from aiohttp import web

async def index(request):
	print(request.app['config'])
	return web.Response(text='Hello Aiohttp')


if __name__ == '__main__':
	print(__doc__ % __author__)
