#!/usr/bin/python
# -*- coding:gbk -*-   
#encoding=gbk
#author=daimin

import os
import sys
from os.path import *
import codecs
import time
import re
import datetime
from activity import *
from act_cls import *
from db_util import *
from playground_parse import *

'''
得到所有的昨天的日志文件
'''
def getYesdayLog(yesday):
    logs = []
    # 
    yesdayfmt = yesday.strftime("%Y%m%d")
    p = re.compile(r'activity\.\w*svc\..*log\.'+yesdayfmt)
    #cwd = os.getcwd()
    curdir = os.listdir(log_dir)
    for d in curdir:
        m = p.match(d)
        if m:
            logd = log_dir+m.group()
            logs.append(logd)  
    print logs
    return logs

'''
读取并解析
'''
def readAndParse(logs,yesday):
    pobjs = []
    for logd in logs:
        print (logd and "gamesvc")
        #logfile = open(logd,'r')
        
        #lines = logfile.readlines()
        #for line in lines:
        #   pobj = Act.genParsedObj(line,yesday)
        #    pobjs.append(pobj)
    
    return pobjs
            


def parse():
    now = datetime.datetime.now()
    offday = 1
    if len(sys.argv) > 1:
        offday = sys.argv[1]
        offday = int(offday)
        
    yesday = now - datetime.timedelta(days = offday )
    
    logs = getYesdayLog(yesday)
    if logs:
        pobjs = readAndParse(logs,yesday)
        #dbUtil = DbUtil(yesday)
        #dbUtil.update(pobjs)
