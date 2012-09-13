#!/usr/bin/python
# -*- coding: gbk -*-
#encoding=gbk
#author=daimin
'''
Created on 2012-8-22

@author: daimin
Ϊ�˱���ԭ�еĴ����ļ�̫�����Էֿ�ҵ��
����ļ���Ҫ�ǻ�ȡ�ܵ�½�û�
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
        """���ݴ���Ĵ������ڣ�ǰ��7��
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
                    
                    if regType == 1:                 #����ע���û�ȥ��
                        continue 
                    if is_robot(username):           #������ȥ��
                        continue
                    self.loguser[username] = 1
    
    def up_week_user_count(self):
        
        db_util.DbUtil.update_week_loguser(self.parseday.strftime("%Y-%m-%d"), len(self.loguser))
        