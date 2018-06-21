#!usr/bin/python3
#-*- coding: utf-8 -*-

'''
	******************
	*     DataBase   *
	******************
	     Powered By %s
'''

__author__ = 'Shadaileng'

import logging; logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s line:%(lineno)d %(filename)s %(funcName)s >>> %(message)s')

from .settings import config
import sqlite3, os, random, asyncio
from .models import User, Blog, Comment, File

class Engine(object):
	def __init__(self, database, user, password, host, port, minsize=5, maxsize=5, flag='sqlite3'):
		self._database = database
		self._user = user
		self._password = password
		self._host = host
		self._port = port
		self._flag = flag
		self._pool = []
		self._minsize = minsize
		self._maxsize = maxsize
		# if not os.path.exists(database):
		# 	raise Exception('not found', 'database', database)
		# else:
		for i in range(minsize):
			conn = self.create_conn()
		
	def connect(self):
		''' 获取数据库连接: 如果连接池中没有空闲连接, 创建一个新的连接，下一次获取连接时，这个连接空闲则会被删除'''
		conn = None
		for i, conn in enumerate(self._pool):
			if conn.index >= self._minsize and conn.status == 0:
				self._pool.pop(i)
		for conn in self._pool:
			if conn.status == 0:
				break
		if conn is None or conn.status == 1:
			conn = self.create_conn()
		conn.status = 1
		return conn

	def create_conn(self):
		''' 创建数据库连接 '''
		try:
			el = sqlite3.connect(self._database)
			if el:
				# print('%s connect successed' % self._database)
				pre_conn = self._pool[len(self._pool) - 1] if len(self._pool) > 0 else None
				conn = Connection(len(self._pool) if len(self._pool) <= 5 else random.randint(100, 999), el, 0, self._minsize)
				self._pool.append(conn)
			else:
				conn = None
		except Exception as e:
			logging.error(e)
			conn = None
		return conn

	async def select(self, sql, args = (), size = None):
		''' 查询数据 '''
		logging.info('%s %s' % (sql, args))
		try:
			with self.connect() as conn:
				connection = conn.el
				cur = connection.cursor()
				cur.execute(sql, args or ())
				if size:
					result = cur.fetchmany(size)
				else:
					result = cur.fetchall()
		except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
			logging.error('Could not complete operation: %s' % e)
			result = None
			cur = None
		finally:
			if cur is not None:
				cur.close()
		return result

	async def execute(self, sql, args=()):
		''' 执行UDI '''
		logging.info('%s %s' % (sql, args))
		try:
			with self.connect() as conn:
				connection = conn.el
				connection.execute(sql, args)
				change = connection.total_changes
				connection.commit()
		except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
			logging.error('Could not complete operation: %s' % e)
			change = 0
		logging.info('change rows: %d' % change)
		return change

class Connection(object):
	"""docstring for Connection"""
	def __init__(self, index, el, status, minsize):
		super(Connection, self).__init__()
		self.index = index
		self.el = el
		self.status = status
		self.minsize = minsize
	def __enter__(self):
		# logging.info('Connection enter: %s' % self.index)
		return self
	def __exit__(self, type, value, trace):
		# logging.info('Connection exit: %s' % self.index)
		self.status = 0
		if self.index >= self.minsize:
			if self.el:
				self.el.close()
				self.el = None
	def __str__(self):
		return '{index: %s, el: %s, status: %s}' % (self.index, self.el, self.status)
	def close(self):
		if self.el:
			self.el.close()
			self.el = None

async def init_db(app):
	config = app['config']
	engine = Engine(config['db']['database'], config['db']['user'], config['db']['password'], config['db']['host'], config['db']['port'])
	app['db'] = engine

async def close_db(app):
	''' 关闭程序时，关闭所有连接 '''
	engine = app['db']
	len_ = len(engine._pool)
	logging.info('close engine: %s' % len_)
	print('===========================')
	for i in range(len_):
		conn = engine._pool[len(engine._pool) - 1]
		conn.close()
		engine._pool.pop()
	print('===========================')
	logging.info('close engine: %s' % len(engine._pool))


if __name__ == '__main__':
	print(__doc__ % __author__)
	engine = Engine(config['db']['database'], '', '', '', '')
	tasks = [User().create(engine), Blog().create(engine), Comment().create(engine), File().create(engine)]
	loop = asyncio.get_event_loop()
	loop.run_until_complete(asyncio.wait(tasks))
	loop.close()
