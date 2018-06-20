#!usr/bin/python3
#-*- coding: utf-8 -*-

'''
	******************
	*      Models    *
	******************
	     Powered By %s
'''

__author__ = 'Shadaileng'

class APIError(Exception):
	def __init__(self, error, data='', message=''):
		super(APIError, self).__init__(message)
		self.error = error
		self.data = data
		self.message = message


class APIValueError(APIError):
	def __init__(self, field, message=''):
		super(APIValueError, self).__init__('value: invalid', field, message)

class APIResourceNotFoundError(APIError):
	def __init__(self, field, message=''):
		super(APIResourceNotFoundError, self).__init__('value: notfound', field, message)



if __name__ == '__main__':
	print(__doc__ % __author__)
