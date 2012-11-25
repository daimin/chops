#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
'''
Created on 2012-11-25

@author: daimin
'''
import time
import wx

import conf

from functions import *
#---------------------------------------------------------------------------
# Show how to derive a custom wxLog class

import datetime

class StatLog(wx.PyLog):
    
    file_object = None
    
    def __init__(self, logTime=0):
        wx.PyLog.__init__(self)
        self.logTime = logTime
        
    @staticmethod
    def get_log_file():
        if StatLog.file_object == None:
            StatLog.file_object = open(conf.log_dir + datetime.datetime.now().strftime("%Y%m%d")+".log", 'a')
        return StatLog.file_object
    
    @staticmethod
    def close_log_file():
        if StatLog.file_object <> None:
            StatLog.file_object.close()
            StatLog.file_object = None
        
    def DoLogString(self, message, timeStamp):
        
        message = time.strftime("%X", time.localtime(timeStamp)) + \
                      ": " + message
                      
        write_log(StatLog.get_log_file(), message)