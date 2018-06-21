#!usr/bin/python3
#-*- coding: utf-8 -*-

'''
	******************
	*      Models    *
	******************
	     Powered By %s
'''

__author__ = 'Shadaileng'

import logging; logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s line:%(lineno)d %(filename)s %(funcName)s >>> %(message)s')

from .apis import APIValueError, APIError

from datetime import datetime

class Column(object):
	def __init__(self, name, column_type, primary_key=False, nullable=False, default=None):
		self.name = name
		self.column_type = column_type
		self.primary_key = primary_key
		self.nullable = nullable
		self.default = default
	def __str__(self):
		return '{name: %s, column_type: %s, primary_key: %s, nullable: %s, default: %s}' % (self.name, self.column_type, self.primary_key, self.nullable, self.default)

class TableMetaClass(type):
	def __new__(cls, name, bases, attrs):
		if name == 'Table':
			return type.__new__(cls, name, bases, attrs)
		
		logging.info('found model: %s' % name)
		
		mappings = dict()
		fields = []
		primary_key = None
		
		for k, v in attrs.items():
			if isinstance(v, Column):
				logging.info('  found mapping: %s ==> %s' % (k, v))
				mappings[k] = v
				if v.primary_key:
					if primary_key:
						raise APIValueError(k, 'already has primary_key %s' % primary_key)
					primary_key = k
				fields.append(k)
		if primary_key is None:
			raise APIError('', '', 'not found primary_key')
		for k in mappings.keys():
			attrs.pop(k)
		attrs['__mappings__'] = mappings
		attrs['__primary_key__'] = primary_key
		attrs['__fields__'] = fields
		attrs['__table__'] = name.upper()
		return type.__new__(cls, name, bases, attrs)

class Table(dict, metaclass=TableMetaClass):
	def __init__(self, **kw):
		super(Table, self).__init__(**kw)
	
	def __getattr__(self, key):
		try:
			return self.get(key)
		except KeyError:
			raise AttributeError('Model object has no attribute %s' % key)
	
	def __setattr__(self, key, val):
		self[key] = val
	
	def getValue(self, key):
		return getattr(self, key, None)
	
	def getValueDefault(self, key):
		value = self.getValue(key)
		if value is None:
			field = self.__mappings__[key]
			if field.default is not None:
				value = field.default() if callable(field.default) else field.default
				logging.info('field %s use default value: %s' % (key, value))
				setattr(self, key, value)
		return value
	
	def rows2mapping(self, rows):
		mappings = []
		fields = list(self.__fields__)
		# logging.info('fields: %s' % fields)
		# logging.info('rows: %s' % rows)
		for row in rows:
			mappings.append(dict(zip(fields, row)))
		logging.info('mappings: %s' % mappings)
		return mappings

	async def findCount(self, engine):
		''' 查询表的记录数 '''
		print('================================findCount======================================')
		params = ['1 = 1']
		args = []
		for field in self.__fields__:
			value = self.getValue(field)
			if value is None:
				continue
			params.append('%s = ?' % field)
			args.append(value)
		sql = 'select count(%s) _num_ from %s where %s' % (self.__primary_key__, self.__table__, ' and '.join(params))

		logging.info('SQL: %s' % sql)
		logging.info('ARG: %s' % args)
		count = await engine.select(sql, args)
		logging.info('count: %s' % count)
		if count is None:
			count = 0
		else:
			count = count[0][0]
		print('================================================================================')
		return count;
	async def find(self, engine, index=0, pageSize=10):
		''' 查询 - index < 0 查询全部 \n index > 0 分页查询 '''
		print('==================================find=========================================')
		params = ['1 = 1']
		args = []
		for field in self.__fields__:
			value = self.getValue(field)
			if value is None:
				continue
			params.append('%s = ?' % field)
			args.append(value)
		sql = 'select count(%s) _num_ from %s where %s' % (self.__primary_key__, self.__table__, ' and '.join(params))

		logging.info('SQL: %s' % sql)
		logging.info('ARG: %s' % args)
		count = await engine.select(sql, args)
		logging.info('count: %s' % count)
		if count is None:
			count = 0
		else:
			count = count[0][0]
		pageCount = count // pageSize + 1 if count % pageSize else count // pageSize
		if index < 0:
			sql = 'select * from %s where %s' % (self.__table__, ' and '.join(params))
		else:
			sql = 'select * from %s where %s limit %s offset %s' % (self.__table__, ' and '.join(params), pageSize, (index if index * pageSize < count else pageCount - 1) * pageSize)

		logging.info('SQL: %s' % sql)
		logging.info('ARG: %s' % args)
		rows = await engine.select(sql, args)
		logging.info('rows: %s' % rows)
		mappings = self.rows2mapping(rows)
		page = {
			"has_next": index < pageCount - 1,
			"has_previous": index > 0,
			"page_index": index,
			"page_count": pageCount,
			"item_count": count
		}
		print('================================================================================')
		return {'data': mappings, 'page': page}
	async def update(self, engine):
		''' 修改 - 主键不能为空 '''
		print('=================================update========================================')
		args = []
		params = []
		if self.getValue(self.__primary_key__) is None:
			raise APIValueError(self.__primary_key__, 'field %s can not be null' % self.__primary_key__)
		for field in self.__fields__:
			value = self.getValue(field)
			if value is None or field == self.__primary_key__:
				continue
			params.append('%s = ?' % field)
			args.append(value)
		args.append(self.getValue(self.__primary_key__))
		sql = 'update %s set %s where %s' % (self.__table__, ','.join(params), '%s = ?' % self.__primary_key__)
		logging.info('SQL : %s' % sql)
		logging.info('ARGS: %s' % args)
		changes = await engine.execute(sql, args)
		logging.info('Update changes: %s' % changes)
		
		print('================================================================================')
		return changes

	async def delete(self, engine):
		''' 根据实体参数删除记录 '''
		print('==================================delete=======================================')
		if self.getValue(self.__primary_key__):
			args = [self.getValue(self.__primary_key__)]
			sql = 'delete from %s where %s' % (self.__table__, '%s = ?' % self.__primary_key__)
		else:
			params = []
			args = []
			for field in self.__fields__:
				value = self.getValue(field)
				if value is None or field == self.__primary_key__:
					continue
				params.append('%s = ?' % field)
				args.append(value)
			sql = 'delete from %s where %s' % (self.__table__, ' and '.join(params))

		logging.info('SQL: %s' % sql)
		logging.info('ARG: %s' % args)
		changes = await engine.execute(sql, args)
		logging.info('Delete changes: %s' % changes)
		print('================================================================================')
		return changes;
	async def insert(self, engine):
		''' 插入记录 '''
		print('==================================insert=======================================')
		params = []
		args = []
		for field in self.__fields__:
			params.append('?')
			args.append(self.getValueDefault(field))
		sql = 'insert into %s(%s) values(%s)' % (self.__table__, ','.join(list(map(lambda x: x.upper(), self.__fields__))), ','.join(params))
		logging.info('SQL : %s' % sql)
		logging.info('ARGS: %s' % args)
		changes = await engine.execute(sql, args)
		logging.info('Insert changes: %s' % changes)
		print('================================================================================')
		return changes
	async def create(self, engine):
		''' 创建表结构 '''
		print('==================================create=======================================')
		sql = 'select * from sqlite_master where name = ? and type = "table"'
		args = [self.__table__]
		logging.info('SQL: %s' % sql)
		logging.info('ARG: %s' % args)
		result = await engine.select(sql, args)
		logging.info('isExits result: %s' % result)
		if result is None or len(result) <= 0:
			logging.info('table %s not exits' % self.__table__)
			sql = 'CREATE TABLE %s( %s )' % (self.__table__, ',' .join(list('%s %s %s %s' % (key, val.column_type, 'PRIMARY KEY AUTOINCREMENT' if val.column_type == 'INTEGER' else 'PRIMARY KEY' if val.primary_key else '', 'DEFAULT (%s)' % val.default if isinstance(val.default, str) else '') for key, val in self.__mappings__.items())))
			logging.info('SQL: %s' % sql)
			result = await engine.execute(sql)
		else:
			logging.info('table %s is exits' % self.__table__)
			print('================================================================================')
			return False
		print('================================================================================')
		return True
		
class File(Table):
	hashpath = Column(name='hashpath', column_type='Varchar(50)', primary_key=True)
	path = Column(name='path', column_type='Varchar(50)')
	name = Column(name='name', column_type='Varchar(50)')
	filetype = Column(name='filetype', column_type='Varchar(50)')
	size = Column(name='size', column_type='Varchar(50)')
	atime = Column(name='atime', column_type='Varchar(50)')
	mtime = Column(name='mtime', column_type='Varchar(50)')
	ctime = Column(name='ctime', column_type='Varchar(50)')	
		
class User(Table):
	id = Column(name='id', column_type='Intege', primary_key=True)
	name = Column(name='name', column_type='Varchar(50)')
	password = Column(name='password', column_type='Varchar(50)')
	email = Column(name='email', column_type='Varchar(50)')
	admin = Column(name='admin', column_type='Varchar(50)')
	image = Column(name='image', column_type='Varchar(50)')
	createtime = Column(name='createtime', column_type='Varchar(50)', default=lambda : datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f'))
	updatetime = Column(name='updatetime', column_type='Varchar(50)', default=lambda : datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f'))	
	
class Blog(Table):
	id = Column(name='id', column_type='Intege', primary_key=True)
	userid = Column(name='name', column_type='Varchar(50)')
	name = Column(name='password', column_type='Varchar(50)')
	# summary = Column(name='email', column_type='Varchar(50)')
	content = Column(name='admin', column_type='Varchar(1024)')
	createtime = Column(name='image', column_type='Varchar(50)', default=lambda : datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f'))
	updatetime = Column(name='createtime', column_type='Varchar(50)', default=lambda : datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f'))

class Comment(Table):
	id = Column(name='id', column_type='Intege', primary_key=True)
	userid = Column(name='userid', column_type='Varchar(50)')
	blogid = Column(name='blogid', column_type='Varchar(50)')
	content = Column(name='content', column_type='Varchar(140)')
	createtime = Column(name='createtime', column_type='Varchar(50)', default=lambda : datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f'))
	updatetime = Column(name='updatetime', column_type='Varchar(50)', default=lambda : datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f'))


if __name__ == '__main__':
	print(__doc__ % __author__)
