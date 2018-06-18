#!usr/bin/python3
#-*- coding: utf-8 -*-

'''
	******************
	*     Modules    *
	******************
	     Powered By %s
'''

__author__ = 'Shadaileng'

from settings import config
import sqlite3, os

class Engine(object):
	def __init__(self, database, user, password, host, port, minsize=5, maxsize=5, flag='sqlite3'):
		self._database = database
		self._user = user
		self._password = password
		self._host = host
		self._port = port
		self._flag = flag
		self._pool = []
		if not os.path.exists(database):
			raise Exception('not found', 'database', database)
		else:
			for i in range(minsize):
				self._pool.append({'index': i, 'el': sqlite3.connect(self._database), 'status': 0})
		
	def connect(self):
		for conn in self._pool:
			if conn['status'] == 0:
				break
		if conn is None or conn['status'] == 1:
			try:
				conn = sqlite3.connect(self._database)
				self._pool.append({'index': i, 'el': conn, 'status': 1})
			except Exception as e:
				logging.warning(e)
				conn = None
			if conn:
				logging.info('%s connect successed' % self._database)
		else:
			conn['status'] = 1
		return conn

if __name__ == '__main__':
	print(__doc__ % __author__)
	engine = Engine('./test.db', '', '', '', '')
	print(engine.connect())
