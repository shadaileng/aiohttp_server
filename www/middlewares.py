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

import aiohttp_jinja2, json
from aiohttp import web

async def handle_404(request):
	return aiohttp_jinja2.render_template('404.html', request, {})

async def handle_500(request):
	return aiohttp_jinja2.render_template('500.html', request, {})

def response_factory(overrides):
	@web.middleware
	async def response(request, handler):

		try:
			rep = await handler(request)
			print('===================================')
			print('response: %s' % rep)
			print('===================================')
			if isinstance(rep, web.StreamResponse):
				override = overrides.get(rep.status)
				if override:
					rep = await override(request)
			elif isinstance(rep, bytes):
				rep = web.Response(body=rep)
				rep.content_type = 'application/octet-stream'
			elif isinstance(rep, str):
				if rep.startswith('redirect:'):
					rep = web.HTTPFound(rep[9:])
				else:
					rep = web.Response(body=rep.encode('utf-8'))
					rep.content_type = 'text/html;charset=utf-8'
			elif isinstance(rep, dict):
				rep = web.Response(body=json.dumps(rep, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
				rep.content_type = 'application/json'
		except web.HTTPException as e:
			logging.error('error middleware: %s' % e)
			print('request: %s' % request)
			override = overrides.get(e.status)
			if override:
				rep = await override(request)
		return rep
	return response

def set_middleware(app):
	
	''' 
	500 - web.HTTPInternalServerError(text="测试中间件")
	404 - web.HTTPNotFound(text="测试中间件")
	'''
	response = response_factory({404: handle_404, 500: handle_500})
	app.middlewares.append(response)
if __name__ == '__main__':
	print(__doc__ % __author__)
