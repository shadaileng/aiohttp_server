#!usr/bin/python3
#-*- coding: utf-8 -*-

'''
	******************
	*     Settings   *
	******************
	     Powered By %s
'''

__author__ = 'Shadaileng'

import logging; logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s line:%(lineno)d %(filename)s %(funcName)s >>> %(message)s')

import yaml, os

BASC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = BASC_DIR + '/config/default.yaml'

def get_config(path):
	with open(path) as file:
		config = yaml.load(file)
	return config

config = get_config(config_path)
config['BASC_DIR'] = BASC_DIR

if __name__ == '__main__':
	print(__doc__ % __author__)
	logging.info(config)
