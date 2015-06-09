#!/usr/bin/env python
#coding=utf-8

class BaseModule(object):
	
	def __init__(self,logger,args,moduleInfo):
		self.args = args
		self.logger = logger
		self.moduleInfo = moduleInfo
	
	def init(self):
		pass
	
	def run(self):
		pass
	
	def clean(self):
		pass
	
	def saveModuleInfo(self,info):
		self.moduleInfo.update(info)
		
	def start(self):
		self.init()
		self.run()
		self.clean()