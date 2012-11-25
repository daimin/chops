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

class StatSplashScreen(wx.SplashScreen):
    """启动页面
    """
    def __init__(self):
        bmp = wx.Image(opj("images/splash.png")).ConvertToBitmap()
        wx.SplashScreen.__init__(self, bmp,
                                 wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
                                 1000, None, -1)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.fc = wx.FutureCall(400, self.ShowMain)

    
    def OnClose(self, evt):
        # Make sure the default handler runs too so this window gets
        # destroyed
        evt.Skip()
        self.Hide()
        
        # if the timer is still running then go ahead and show the
        # main frame now
        if self.fc.IsRunning():
            self.fc.Stop()    

    def ShowMain(self):
        frame = statframe.StatFrame(None, conf.APP_NAME)
        frame.Show()
        if self.fc.IsRunning():
            self.Raise()
        

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
      
        #splash = StatSplashScreen()
        #splash.Show()
        
        frame = statframe.StatFrame(None, conf.APP_NAME)
        frame.Show(True)
        
        self.SetTopWindow(frame)
        
        return True
    

