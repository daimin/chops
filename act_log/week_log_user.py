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
    
    def get_log_file(self,parseday):
        logs = []
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
                    
                    if regType == 1:
                        return 
                    if is_robot(username):
                        return
                    self.loguser[username] = 1
    
    def get_week_user_count(self):
        return len(self.loguser)
                    
                    


if __name__ == "__main__":
    now = datetime.datetime.now()
    wlu = WeekLogUser(now)
    print wlu.get_week_user_count()