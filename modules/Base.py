#!/usr/bin/env python
#coding=utf-8

import logging
import Requests

class BaseModule(object):

	def __init__(self,mArgs,mInfo):
		# Logger
		self.logger=logging.getLogger('Ccoin')
		# Module Name
		self.moduleName = str(self.__class__)
		# Args for modules (Read Only)
		self.__cookie = mArgs['cookie']
		self.__mArgs = mArgs
		# Module Info (Shared)
		self._mInfo = mInfo

	@property
	def mArgs(self):
		return self.__mArgs

	@property
	def mInfo(self):
		return self._mInfo

	def mInfoAdd(self,key,value):
		if key in self._mInfo:
			self.logger.error('the key %s to story in mInfo is already exists. value:%s' %(key,value))
			return False
		else:
			self._mInfo[key] = value
			return True

	def http_get(self,url):
		return Requests.get(url,cookies = self.__cookie)

	def http_post(self,url,data=None):
		return Requests.post(url, data, cookies = self.__cookie)
	
	def http_delete(self,url):
		return Requests.delete(url,cookies=self.__cookie)

	def start(self):
		if not self.init():
			self.logger.error('%s init failed, exit.' %self.moduleName)
		else:
			self.logger.info('%s init finished.' %self.moduleName)
		self.run()
		self.clean()

	def init(self):
		'''
		rewrite by subclass for init module
		@return True | False
		@notice if init method return false the module will exit.
		'''
		return True

	def run(self):
		'''
		rewrite by subclass for module's main function
		'''
		pass

	def clean(self):
		'''
		rewrite by subclass for clean work after run
		'''
		pass
