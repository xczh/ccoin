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



''' === Advanced Option === '''

''' If you don't know what the meaning of it, don't edit it. '''

'''
  Global
'''
import os
DEBUG = False
PATH_ROOT = os.getcwd()
ENABLED_MODULE = ['TweetModule','PushCodeModule','PointModule']

'''
  Log
'''
LOG_LEVEL = 'INFO' # INFO,WARNING,ERROR
LOG_FORMAT = r'[%(asctime)s %(levelname)s] %(message)s'
LOG_DATE_FORMAT = r'%Y-%m-%d %H:%M:%S'
LOG_DIR = os.path.join(PATH_ROOT,'log')
