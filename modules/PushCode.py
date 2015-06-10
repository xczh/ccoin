#!/usr/bin/env python
#coding=utf-8

from Base import BaseModule
import Requests
import json
import time

class PushCodeModule(BaseModule):
	
	push_url = r'https://coding.net/api/user/christopher_winnie/project/dust/git/new/master%252Fcoding_coin'
	cookie = None
	
	def init(self):
		if self.moduleInfo['login'] is True:
			self.cookie = {'sid':self.moduleInfo['sid']}
			get_last_sha1_url = r'https://coding.net/api/user/%s/project/%s/git/new/%sQWEASD%s' %(self.moduleInfo['userinfo']['global_key'],self.conf.PUSH_PROJECT,self.conf.PUSH_BRANCH,self.conf.PUSH_PATH.replace('/','%252F'))
			get_last_sha1_url = get_last_sha1_url.replace('QWEASD','%252F')
			r = Requests.get(get_last_sha1_url,cookies = self.cookie)
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
			self.push_url = r'https://coding.net/api/user/%s/project/%s/git/new/%sQWEASD%s' %(self.moduleInfo['userinfo']['global_key'],self.conf.PUSH_PROJECT,self.conf.PUSH_BRANCH,self.conf.PUSH_PATH)
			self.push_url = self.push_url.replace('QWEASD','%252F')
			title = str(time.time())
			self.post_data = {'title':title,'content':title,'message':'Coding Coin','lastCommitSha':lastCommitSha}
			return True
		else:
			self.logger.error('You are not logged in.')
			return False
	
	def run(self):
		if self.cookie:
			r = Requests.post(self.push_url, data = self.post_data, cookies = self.cookie)
			if r.status_code == 200:
				ret = json.loads(r.text)
				if ret['code'] == 0:
					self.logger.info('PushCode success.')
					return True
				else:
					self.logger.error('PushCode Failed. Server response: %s' %ret)
			else:
				self.logger.error('HTTP error while pushCode. URL: %s \n HTTP Code: %s' %(self.push_url,r.status_code))
				return False
		else:
			self.logger.info('You are not logged in. PushCode module exit.')
			return False
	
	def clean(self):
		pass