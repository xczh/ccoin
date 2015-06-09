#!/usr/bin/env python
#coding=utf-8

import os

'''
  coding.net 登录信息
'''
USER = 'default_user'
PWD = 'default_pwd'

'''
  基础配置
'''
# 调试模式
DEBUG = True
PATH_ROOT = os.getcwd()

'''
  日志配置
'''
# 输出日志等级，可选INFO,WARNING,ERROR之一，默认值WARNING
LOG_LEVEL = 'WARNING'
# 日志头格式
#LOG_FORMAT = r'[%(asctime)s %(levelname)s]%(filename)s(%(lineno)dL) %(message)s'
LOG_FORMAT = r'[%(asctime)s %(levelname)s] %(message)s'
# 日期格式
LOG_DATE_FORMAT = r'%Y-%m-%d %H:%M:%S'
# 日志路径
LOG_DIR = os.path.join(PATH_ROOT,'log')