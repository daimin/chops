#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
'''
Created on 2012-11-21

@author: daimin
'''
import wx

def MessageBox(content,title):
    return wx.MessageBox(content, caption=title, style=wx.YES_NO | wx.ICON_QUESTION)
    
    
