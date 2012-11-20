#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
'''
Created on 2012-11-19

@author: daimin
'''
import wx

import images
import conf

from wx.lib.mixins.treemixin import ExpansionState
TreeBaseClass = wx.TreeCtrl


class StatTree(ExpansionState, TreeBaseClass):
    def __init__(self, parent):
        TreeBaseClass.__init__(self, parent, style=wx.TR_DEFAULT_STYLE|
                               wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.TR_LINES_AT_ROOT | wx.TR_HIDE_ROOT)
        self.BuildTreeImageList()


    def AppendItem(self, parent, text, image=-1, wnd=None):
        item = TreeBaseClass.AppendItem(self, parent, text, image=image)
            
        return item
            
    def BuildTreeImageList(self):
        imgList = wx.ImageList(16, 16)
        for png in conf._statPngs:
            imgList.Add(images.catalog[png].GetBitmap())
            
        # add the image for modified demos.
        imgList.Add(images.catalog["custom"].GetBitmap())

        self.AssignImageList(imgList)


    def GetItemIdentity(self, item):
        return self.GetPyData(item)
