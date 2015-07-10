#!/usr/bin/env python
#coding:utf-8
"""
  Purpose: ccoin Login Core Class
  Author:  xczh <christopher.winnie2012@gmail.com>

  Copyright (c) 2015 xczh. All rights reserved.
"""

from modules import Requests
import json
import hashlib

class Login(object):

    sid = ''
    userinfo = None
    login = False
    __result = {'login':False}

    def __init__(self,user,pwd):
        self.user = user
        if len(pwd) != 40:
            self.pwd = hashlib.sha1(pwd).hexdigest()
        else:
            self.pwd = pwd

    def login(self):
        post_data = {'email':self.user,'password':self.pwd,'remember_me':False}
        headers = {
            'User-Agent': 'Ccoin',
            'Accept': r'application/json, text/plain, */*',
            'Origin': r'https://coding.net',
            'Host':'coding.net',
            'Content-Type': r'application/x-www-form-urlencoded;charset=UTF-8',
            'Referer': r'https://coding.net/login',
        }
        current_user_url = r'https://coding.net/api/current_user'
        login_url = r'https://coding.net/api/login'
        r = Requests.get(current_user_url)
        if r.status_code == 200 and r.cookies['sid']:
            sid = r.cookies['sid']
            rp = Requests.post(login_url, data=post_data,cookies={'sid':sid})
            if rp.status_code == 200:
                ret = json.loads(rp.text)
                if ret['code'] == 0:
                    # Success
                    self.__result = {'login':True,'global_key':ret['data']['global_key'],'sid':sid,'userinfo':ret['data']}
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

    def getResult(self):
        return self.__result