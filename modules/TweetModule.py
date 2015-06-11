#!/usr/bin/env python
#coding=utf-8

from Base import BaseModule
import Requests
import json

class TweetModule(BaseModule):
	
	tweet_url = r'https://coding.net/api/tweet'
	sid = ''
	delete_action = True
	content = {'content':'hello coding'}
	cookie = None
	
	def init(self):
		if self.moduleInfo['login'] is True:
			self.cookie = {'sid':self.moduleInfo['sid']}
			return True
		else:
			self.logger.error('You are not logged in.')
			return False
	
	def run(self):
		if self.cookie:
			r = Requests.post(self.tweet_url, data=self.content,cookies=self.cookie)
			if r.status_code == 200:
				ret = json.loads(r.text)
				if ret['code'] == 0:
					no = ret['data']['id']
					self.logger.info('Tweet success. No: %d' %no )
					if not self.delete_action:
						return True
					# delete tweet
					delete_url = r'https://coding.net/api/tweet/%d' % no
					rd = Requests.delete(delete_url,allow_redirects=False,cookies=self.cookie)
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
						return True
				else:
					self.logger.error('Tweet send failed. Server response: %s' %ret)
					return False
			else:
				self.logger.error('HTTP error while send tweet. URL: %s' %self.tweet_url)
				return False
		else:
			self.logger.error('You are not logged in. Tweet Module exit.')
			return False
	
	def clean(self):
		pass