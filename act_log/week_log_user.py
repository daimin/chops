#!/usr/bin/python
# -*- coding: gbk -*-
#encoding=gbk
#author=daimin
'''
Created on 2012-8-22

@author: daimin
为了避免原有的处理文件太大，所以分开业务
这个文件主要是获取周登陆用户
'''

import datetime
import re
import os

from activity import *
from config import *
from common import *
import db_util

class WeekLogUser(object):
    
    def __init__(self, parseday):
        """根据传入的处理日期，前推7天
        """
        self.loguser = {}
        logs = self.get_log_file(parseday)
        for logd in logs:
            logfile = open(logd,'r')
            self.do_with_log(logfile)
            logfile.close()
        
        self.up_week_user_count()
        del logs
    
    def get_log_file(self,parseday):
        logs = []
        self.parseday = parseday
        for i in range(0,7):
            doday = parseday - datetime.timedelta(days = i )
            dodayfmt = doday.strftime("%Y%m%d")
            p = re.compile(r'activity\.loginsvc\..*log\.'+dodayfmt)
            curdir = os.listdir(log_dir)
            for d in curdir:
                m = p.match(d)
                if m:
                    logd = log_dir+m.group()
                    logs.append(logd)
        return logs
    
    def do_with_log(self,logfile):
        lines = logfile.readlines()
        for line in lines:
            if line <> "":
                linelist = line.split(",")
                if int(linelist[1]) == ACT_LOGIN:
                    username = linelist[5]
                    regType = int(linelist[6])
                    
                    if regType == 1:                 #快速注册用户去掉
                        continue 
                    if is_robot(username):           #机器人去掉
                        continue
                    self.loguser[username] = 1
    
    def up_week_user_count(self):
        
        db_util.DbUtil.update_week_loguser(self.parseday.strftime("%Y-%m-%d"), len(self.loguser))
        