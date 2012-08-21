#!/usr/bin/python
# -*- coding:gbk -*-   
#encoding=gbk
#author=daimin

import sys
from config import *
import time
import datetime

def isNotEmpty(text):
    if text:
        return True
    return text.isspace()
    return False

'''
记录日志
'''
def  pk_log(errMsg0="", errMsg1=""):
    if PK_LOG == True:
        lineNo = None
        tb = sys.exc_info()
        if errMsg0 == "":
            errMsg0 = tb[0]
            errMsg1 = tb[1]
        lineNo = tb[2].tb_lineno
        print errMsg0,errMsg1," on line:",lineNo

'''
检验一个变量是否存在
'''
def  isset(v):
    try:
        type (eval(v))
    except:
        return   0
    else:
        return   1    
    
#def GameMoney2RMB(gmney):
#    return int(gmney/MONEY_RATE)

    
    

    

   
    
