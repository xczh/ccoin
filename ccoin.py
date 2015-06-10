#!/usr/bin/env python
#coding=utf-8

import conf
import logging
import sys
import os
import time
from modules import Requests
from modules.Login.Login import LoginModule
from modules.Tweet import TweetModule
from modules.PushCode import PushCodeModule

class Ccoin(object):
	version = '0.1.0'
	args = None
	logger = None
	moduleInfo = {}
	
	@classmethod
	def initLogger(cls):
		logger=logging.getLogger(cls.__name__)
		logger.setLevel(logging.DEBUG)
		format = logging.Formatter(conf.LOG_FORMAT,conf.LOG_DATE_FORMAT)
		if conf.DEBUG:
			# 调试模式
			# Console Handler
			console = logging.StreamHandler()
			console.setLevel(logging.DEBUG)
			console.setFormatter(format)
			logger.addHandler(console)
		else:
			# 运行模式
			# File Handler
			file_handler = logging.FileHandler(filename=os.path.join(conf.LOG_DIR,cls.__name__ + '-%d.log' % int(time.time())),mode='w')
			if conf.LOG_LEVEL == 'INFO':
				file_handler.setLevel(logging.INFO)
			elif conf.LOG_LEVEL == 'ERROR':
				file_handler.setLevel(logging.ERROR)
			else:
				file_handler.setLevel(logging.WARNING)
			file_handler.setFormatter(format)
			logger.addHandler(file_handler)		
		cls.logger = logger
	
	@classmethod
	def argsParser(cls):
		import argparse
		parser = argparse.ArgumentParser(description='an automatic acquisition of coding coins tool.')
		parser.add_argument('-u','--user', dest='user',action='store',type=str,default=conf.USER,
			                help='Your coding.net Email or Personality Suffix')
		parser.add_argument('-p','--pwd', dest='pwd',action='store',type=str,default=conf.PWD,
			                help='Your coding.net Password')
		parser.add_argument('--plain', dest='plain',action='store_true',default=False,
		                    help='if the -p param provided is plaintext')		
		parser.add_argument('-v','--version', action='version', version='ccoin %s' % cls.version)
		return parser.parse_args()
	
	@classmethod
	def update(cls):
		import json
		# URL
		url = r'https://coding.net/u/xczh/p/coding_coins/git/raw/master/update.html'
		r = Requests.get(url)
		if r.status_code != 200:
			cls.logger.error('Update Fail. The HTTP Status is %d' % r.status_code)
			return False
		else:
			cls.logger.debug('HTTP response body: %s' % r.text)
			ret = json.loads(r.text)
			cls.logger.info('Newest Version is: %s' % ret['version'])
			if ret['version'] > cls.version:
				# Need Update
				cls.logger.warn('Current version is old. It may cause fail.\n You can get newest version by this command:\n'
				                'git pull')
				sys.exit(-1)
				return False
			else:
				return True
	
	@classmethod
	def main(cls):
		cls.initLogger()
		cls.args = cls.argsParser()
		cls.update()
		s = LoginModule(cls.logger, cls.args, conf, cls.moduleInfo)
		s.start()
		s = TweetModule(cls.logger, cls.args, conf, cls.moduleInfo)
		s.start()
		s = PushCodeModule(cls.logger, cls.args, conf, cls.moduleInfo)
		s.start()
		cls.logger.info('Process finished.')

if __name__=='__main__':
	Ccoin.main()