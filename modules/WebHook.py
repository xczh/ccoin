#!/usr/bin/env python
#coding:utf-8
"""
  Purpose: ccoin WebHook Module
  Author:  xczh <christopher.winnie2012@gmail.com>
  
  Copyright (c) 2015 xczh. All rights reserved.
"""

from Base import BaseModule
import time
import Requests

class WebHookModule(BaseModule):
	
	webhook_url = ''
	webhook_key = ''
	webhook_data = {}
	
	def init(self):
		if self.mArgs.has_key('WEBHOOK_URL') and self.mArgs.has_key('WEBHOOK_KEY'):
			if not self.mArgs['WEBHOOK_URL']:
				self.logger.error('WEBHOOK_URL is empty, WebHook Module exit.')
				return False
			else:
				self.webhook_url = self.mArgs['WEBHOOK_URL']
				self.webhook_key = self.mArgs['WEBHOOK_KEY']
				return True
		else:
			self.logger.error('Can not find WEBHOOK_URL in conf.py.')
			return False
	
	def run(self):
		self.webhook_data['key'] = self.webhook_key
		self.webhook_data['global_key'] = self.mArgs['global_key']
		self.webhook_data['point_left'] = self.mInfo['point_left']
		self.webhook_data['point_total'] = self.mInfo['point_total']
		self.webhook_data['date'] = time.strftime('%Y%m%d')
		
		self.logger.debug(self.webhook_data)

		r = Requests.post(self.webhook_url,data= self.webhook_data)
		if r.status_code == 200:
			self.logger.info('WebHook send success. URL:%s' %self.webhook_url)
			return True
		else:
			self.logger.error('HTTP error while get point. URL: %s, HTTP Code: %s' %(self.webhook_url,r.status_code))
			return False

	