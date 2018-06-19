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

from apis import APIValueError, APIError

class Column(object):
	def __init__(self, name, column_type, primary_key=False, nullable=False, default=None):
		self.name = name
		self.column_type = column_type
		self.primary_key = primary_key
		self.nullable = nullable
		self.default = default

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
			return self[key]
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
		logging.info('fields: %s' % fields)
		logging.info('rows: %s' % rows)
		for row in rows:
			mappings.append(dict(zip(fields, row)))
		logging.info('mappings: %s' % mappings)
		return mappings

	async def findCount(self, engine):
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
		
class File(Table):
	hashpath = Column(name='hashpath', column_type='Varchar(50)', primary_key=True)
	path = Column(name='path', column_type='Varchar(50)')
	name = Column(name='name', column_type='Varchar(50)')
	filetype = Column(name='filetype', column_type='Varchar(50)')
	size = Column(name='size', column_type='Varchar(50)')
	atime = Column(name='atime', column_type='Varchar(50)')
	mtime = Column(name='mtime', column_type='Varchar(50)')
	ctime = Column(name='ctime', column_type='Varchar(50)')	


if __name__ == '__main__':
	print(__doc__ % __author__)
