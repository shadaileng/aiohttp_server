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

import asyncio, aiohttp_jinja2, aiohttp

from aiohttp import web
from .models import File
from faker import Faker

routes = web.RouteTableDef()

def get_random_name():
    fake = Faker()
    return fake.name()

@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def index(request):
	logging.info('index')
	print('=====================================')
	print('query: %s' % request.query)
	for k, v in request.query.items():
		print('%s: %s' % (k, v))
	print('=====================================')

	return {}
@routes.get('/login')
@aiohttp_jinja2.template('login.html')
async def login(request):
	return {}

@routes.post('/login')
@aiohttp_jinja2.template('index.html')
async def login_post(request):
	data = await request.post()
	name = data['name']
	password = data['password']
	logging.info('name: %s, password: %s' % (name, password))
	logging.info('data: %s' % data)
	return {'name': name, 'password': password}

@routes.post('/upload')
@aiohttp_jinja2.template('index.html')
async def upload(request):
	# data = await request.post()
	# file = data['file']
	# filename = file.filename
	# file_ = file.file
	# with open('./' + filename, 'wb') as f:
	# 	data = file_.read()
	# 	f.write(data)
	reader = await request.multipart()
	print(reader)
	data = await reader.next()
	filename = data.filename
	with open('./' + filename, 'wb') as f:
		while True:
			chunk = await data.read_chunk()
			if not chunk:
				break
			print(len(chunk))
			f.write(chunk)
	return {'filename': filename}

@routes.get('/chat')
@aiohttp_jinja2.template('chat.html')
async def chat(request):
	ws_current = web.WebSocketResponse()
	ws_ready = ws_current.can_prepare(request)
	if not ws_ready.ok:
		return aiohttp_jinja2.render_template('chat.html', request, {})
	await ws_current.prepare(request)
	
	name = get_random_name()
	logging.info('%s join' % name)
	await ws_current.send_json({'action': 'connect', 'name': name})
	
	for ws in request.app['websockets'].values():
		await ws.send_json({'action': 'join', 'name': name})
	request.app['websockets'][name] = ws_current
	
	while True:
		msg = await ws_current.receive()
		if msg.type == aiohttp.WSMsgType.text:
			for ws in request.app['websockets'].values():
				if ws is not ws_current:
					await ws.send_json({'action': 'sent', 'name': name, 'text': msg.data})
		else:
			break
	request.app['websockets'].pop(name)
	logging.info('%s disconnect' % name)
	
	for ws in request.app['websockets'].values():
		await ws.send_json({'action': 'disconnect', 'name': name})
	
	return ws_current
	
if __name__ == '__main__':
	print(__doc__ % __author__)
