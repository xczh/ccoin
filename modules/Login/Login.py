#!/usr/bin/env python
#coding=utf-8

from .. import Base
from .. import Requests
from urllib import urlencode
import json
import hashlib

class LoginModule(Base.BaseModule):
	
	login_url = r'https://coding.net/api/login'
	current_user_url = r'https://coding.net/api/current_user'
	sid = ''
	userinfo = None
	login = False
	
	def init(self):
		self.email = self.args.user
		if self.args.plain is True:
			self.password = hashlib.sha1(self.args.pwd).hexdigest()
		else:
			self.password = self.args.pwd
	
	def run(self):
		post_data = {'email':self.email,'password':self.password,'remember_me':False}
		headers = {'User-Agent': 'Ccoin',
		   'Accept': r'application/json, text/plain, */*',
		   'Origin': r'https://coding.net',
		   'Host':'coding.net',
		   'Content-Type': r'application/x-www-form-urlencoded;charset=UTF-8',
		   'Referer': r'https://coding.net/login',
		}		
		r = Requests.get(self.current_user_url)
		if r.status_code == 200 and r.cookies['sid']:
			self.sid = r.cookies['sid']
			rp = Requests.post(self.login_url, data=post_data,cookies={'sid':self.sid})
			if rp.status_code == 200:
				ret = json.loads(rp.text)
				if ret['code'] == 0:
					# Success
					self.userinfo = ret['data']
					self.login = True
					return True
				else:
					# Wrong Password
					self.logger.error('login failed. Server response: %s' %(rp.text))
					return False
			else:
				self.logger.error('unknown error while login: %s' %self.login_url)
				return False
		else:
			self.logger.error('unknown error before login: %s' %self.current_user_url)
			return False			
	
	def clean(self):
		self.saveModuleInfo({'sid':self.sid,'userinfo':self.userinfo,'login':self.login})