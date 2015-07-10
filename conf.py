#!/usr/bin/env python
#coding:utf-8
"""
  Purpose: ccoin configuration file
  Author:  xczh <christopher.winnie2012@gmail.com>

  Copyright (c) 2015 xczh. All rights reserved.
"""

''' === Common Option === '''

'''
  Login
'''
USER = 'default_user'
PWD = 'default_pwd'

'''
  PushCode Module
'''
PUSH_PROJECT = 'dust'
PUSH_BRANCH = 'master'
PUSH_PATH = 'coding_coin'

'''
  WebHook Module
'''
WEBHOOK_URL = ''
WEBHOOK_KEY = '' # It will be send as 'key' field for auth

''' === Advanced Option === '''

''' If you don't know what the meaning of it, don't edit it. '''

'''
  Global
'''
import os,sys
DEBUG = False
PATH_ROOT = os.path.split(os.path.realpath(sys.argv[0]))[0]
ENABLED_MODULE = ['PushCodeModule','PointModule','WebHookModule']

'''
  Log
'''
LOG_LEVEL = 'INFO' # INFO,WARNING,ERROR
LOG_FORMAT = r'[%(asctime)s %(levelname)s] %(message)s'
LOG_DATE_FORMAT = r'%Y-%m-%d %H:%M:%S'
LOG_DIR = os.path.join(PATH_ROOT,'log')
