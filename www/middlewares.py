#!usr/bin/python3
#-*- coding: utf-8 -*-

'''
	******************
	*   Middlewares  *
	******************
	     Powered By %s
'''

__author__ = 'Shadaileng'

import logging; logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s line:%(lineno)d %(filename)s %(funcName)s >>> %(message)s')

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
			print('===================================')
			print('response: %s' % response)
			print('===================================')
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
if __name__ == '__main__':
	print(__doc__ % __author__)
