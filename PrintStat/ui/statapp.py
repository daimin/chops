#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
'''
Created on 2012-11-19

@author: daimin
'''

import wx
import version
import statframe
import statlog

from functions import *


class StatApp(wx.App):

    def __init__(self, redirect):
        wx.App.__init__(self, redirect)
        
    def OnInit(self):
        
        wx.Log_SetActiveTarget(statlog.StatLog())
        
        # Now that we've warned the user about possibile problems,
        # lets import images
        import images as i
        global images
        images = i
        
        # Create and show the splash screen.  It will then create and show
        # the main frame when it is time to do so.
        wx.SystemOptions.SetOptionInt("mac.window-plain-transition", 1)
        self.SetAppName(conf.APP_NAME)
        
        # For debugging
        #self.SetAssertMode(wx.PYAPP_ASSERT_DIALOG)

        
        frame = statframe.StatFrame(None, conf.APP_NAME)
        frame.Show(True)
        
        self.SetTopWindow(frame)
        
        return True
    

