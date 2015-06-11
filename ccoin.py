#!/usr/bin/env python
#coding=utf-8

import conf
import logging
import sys
import os
import time

from login import Login
from modules import Requests
from modules.Tweet import TweetModule
from modules.PushCode import PushCodeModule

class Ccoin(object):
	# Version
	version = '1.0.1'
	# CLI args
	args = None
	# Logger
	logger = None
	# Module Shared Info
	mInfo = {}

	# User
	login = False
	sid =None
	userinfo = None
	global_key = None

	@classmethod
	def initLogger(cls):
		logger=logging.getLogger('Ccoin')
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
		parser.add_argument('-u','--user', dest='user',action='store',type=str,default='',
				            help='Your coding.net Email or Personality Suffix')
		parser.add_argument('-p','--pwd', dest='pwd',action='store',type=str,default='',
				            help='Your coding.net Password')
		parser.add_argument('-P','--push-project', dest='push_project',action='store',type=str,default='',
				            help='push to which project')
		parser.add_argument('-B','--push-branch', dest='push_branch',action='store',type=str,default='',
				            help='push to which branch')	
		parser.add_argument('-D','--push-path', dest='push_path',action='store',type=str,default='',
				                    help='push to project\'s dir name')		
		parser.add_argument('-v','--version', action='version', version='ccoin %s' % cls.version)
		cls.args = parser.parse_args()

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
								'git pull origin dev:dev')
				sys.exit(-1)
				return False
			else:
				return True

	@classmethod
	def main(cls):
		# init logger
		cls.initLogger()
		# get cli args
		cls.argsParser()
		# check for update
		cls.update()
		# login
		u = Login(cls.args.user,cls.args.pwd)
		if u.login():
			msg = u.getResult()
			cls.login = True
			cls.global_key = msg['global_key']
			cls.sid = msg['sid']
			cls.userinfo = msg['userinfo']
		else:
			# login failed, exit.
			sys.exit(-1)

		# build module args
		mArgs = {
			'login':cls.login,
			'global_key':cls.global_key,
		    'cookie':{'sid':cls.sid},
			'userinfo':cls.userinfo,
		    'PUSH_PROJECT':cls.args.push_project,
		    'PUSH_BRANCH':cls.args.push_branch,
		    'PUSH_PATH':cls.args.push_path,
		}
		for k,v in mArgs.iteritems():
			if not v and k in conf.__dict__:
				mArgs[k] = conf.__dict__[k]
		cls.logger.debug(str(mArgs))
		
		# module work
		for name in conf.ENABLED_MODULE:
			m = globals()[name](mArgs,cls.mInfo)
			m.start()

		# end
		cls.logger.info('Process finished.')

if __name__=='__main__':
	Ccoin.main()