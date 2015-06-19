#!/usr/bin/env python
#coding:utf-8
"""
  Purpose: ccoin Point Module
  Author:  xczh <christopher.winnie2012@gmail.com>
  
  Copyright (c) 2015 xczh. All rights reserved.
"""

from Base import BaseModule
import json
import time

class PointModule(BaseModule):
	
	point_url = r'https://coding.net/api/point/points'
	
	def run(self):
		r = self.http_get(self.point_url)
		if r.status_code == 200:
			ret = json.loads(r.text)
			if ret['code'] == 0:
				self.logger.info('Get point info success.')
				self.logger.info('Current: point left:%.2f, point total:%.2f' %(ret['data']['points_left'],ret['data']['points_total']))
				return True
			else:
				self.logger.error('Get point Failed. Server response: %s' %ret)
				return False
		else:
			self.logger.error('HTTP error while get point. URL: %s \n HTTP Code: %s' %(self.point_url,r.status_code))
			return False
	