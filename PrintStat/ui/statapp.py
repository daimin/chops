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
    def OnInit(self):

        # Check runtime version
        """
        if version.VERSION_STRING != wx.VERSION_STRING:
            wx.MessageBox(caption="Warning",
                          message="You're using version %s of wxPython, but this copy of the demo was written for version %s.\n"
                          "There may be some version incompatibilities..."
                          % (wx.VERSION_STRING, version.VERSION_STRING))
        """

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

        # Normally when using a SplashScreen you would create it, show
        # it and then continue on with the applicaiton's
        # initialization, finally creating and showing the main
        # application window(s).  In this case we have nothing else to
        # do so we'll delay showing the main frame until later (see
        # ShowMain above) so the users can see the SplashScreen effect.        
        splash = StatSplashScreen()
        splash.Show()

        return True
