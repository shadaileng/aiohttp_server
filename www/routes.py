#!usr/bin/python3
#-*- coding: utf-8 -*-

'''
	******************
	*      Routes    *
	******************
	     Powered By %s
'''

__author__ = 'Shadaileng'

from views import index

def set_route(app):
	app.router.add_get('/', index)


if __name__ == '__main__':
	print(__doc__ % __author__)
