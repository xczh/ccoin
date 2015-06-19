#!/usr/bin/env python
#coding:utf-8
"""
  Purpose: ccoin Pushcode Module
  Author:  xczh <christopher.winnie2012@gmail.com>
  
  Copyright (c) 2015 xczh. All rights reserved.
"""

from Base import BaseModule
import json
import time

class PushCodeModule(BaseModule):
	
	push_url = r'https://coding.net/api/user/christopher_winnie/project/dust/git/new/master%%252Fcoding_coin'
	# commit remark
	commit_remark = 'Coding Coin'
	
	def init(self):
		get_last_sha1_url = r'https://coding.net/api/user/%s/project/%s/git/new/%s%%252F%s' %(self.mArgs['global_key'],self.mArgs['PUSH_PROJECT'],self.mArgs['PUSH_BRANCH'],self.mArgs['PUSH_PATH'].replace('/','%252F'))
		r = self.http_get(get_last_sha1_url)
		if r.status_code == 200:
			ret = json.loads(r.text)
			if ret['code'] == 0:
				lastCommitSha = ret['data']['lastCommit']
			else:
				self.logger.error('get lastCommitSha failed. URL: %s \n Server response: %s' %(get_last_sha1_url,ret))
				return False
		else:
			self.logger.error('HTTP error while get lastCommitSha. URL: %s' %get_last_sha1_url)
			return False 
		self.push_url = r'https://coding.net/api/user/%s/project/%s/git/new/%s%%252F%s' %(self.mArgs['global_key'],self.mArgs['PUSH_PROJECT'],self.mArgs['PUSH_BRANCH'],self.mArgs['PUSH_PATH'])
		title = time.strftime('%Y%m%d-%H%M%S')
		self.post_data = {'title':title,'content':title,'message':self.commit_remark,'lastCommitSha':lastCommitSha}
		return True
	
	def run(self):
		r = self.http_post(self.push_url, data = self.post_data)
		if r.status_code == 200:
			ret = json.loads(r.text)
			if ret['code'] == 0:
				self.logger.info('PushCode success.')
				return True
			else:
				self.logger.error('PushCode Failed. Server response: %s' %ret)
				return False
		else:
			self.logger.error('HTTP error while pushCode. URL: %s \n HTTP Code: %s' %(self.push_url,r.status_code))
			return False
	