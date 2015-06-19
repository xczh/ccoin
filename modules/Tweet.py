#!/usr/bin/env python
#coding:utf-8
"""
  Purpose: ccoin Tweet Module
  Author:  xczh <christopher.winnie2012@gmail.com>
  
  Copyright (c) 2015 xczh. All rights reserved.
"""

from Base import BaseModule
import json

class TweetModule(BaseModule):
	
	tweet_url = r'https://coding.net/api/tweet'
	# Tweet will be deleted or not
	delete_action = True
	# Tweet content
	content = {'content':'hello coding'}
	
	def run(self):
		r = self.http_post(self.tweet_url, data=self.content)
		if r.status_code == 200:
			ret = json.loads(r.text)
			if ret['code'] == 0:
				no = ret['data']['id']
				self.logger.info('Tweet success. No: %d' %no )
				if not self.delete_action:
					return True
				# delete tweet
				delete_url = r'https://coding.net/api/tweet/%d' % no
				rd = self.http_delete(delete_url)
				if r.status_code == 200:
					retd = json.loads(rd.text)
					if retd['code'] == 0:
						self.logger.info('Tweet deleted. No: %d' %no)
						return True
					else:
						self.logger.error('Tweet delete failed. No: %d, you may need delete it yourself.' %no)
						return True
				else:
					self.logger.error('HTTP error while delete tweet. URL: %s' % delete_url)
					return False
			else:
				self.logger.error('Tweet send failed. Server response: %s' %ret)
				return False
		else:
			self.logger.error('HTTP error while send tweet. URL: %s' %self.tweet_url)
			return False
	