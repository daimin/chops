#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
'''
Created on 2012-11-19

@author: daimin
'''
import sys, os, time, traceback, types

import wx
import wx.aui

import images as em_images
import stat_tree
import modules
import statlog
from statdialog import MessageBox

from functions import *


class StatFrame(wx.Frame):

    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, -1, title, size = (conf.FRAME_WIDTH, conf.FRAME_HEIGHT),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE | wx.MAXIMIZE)
        self.SetMinSize((conf.FRAME_WIDTH,conf.FRAME_HEIGHT))
        
        
        # Use a panel under the AUI panes in order to work around a
        # bug on PPC Macs
        pnl = wx.Panel(self)
        self.pnl = pnl
        
        self.mgr = wx.aui.AuiManager() 
        self.mgr.SetManagedWindow(pnl)
        
        
        self.loaded = False
        self.cwd = os.getcwd()
        self.firstTime = True
        self.statPage = None

        icon = em_images.WXPdemo.GetIcon()
        self.SetIcon(icon)

            
        self.otherWin = None
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy)
        self.Bind(wx.EVT_MAXIMIZE, self.OnMaximize)

        self.Centre(wx.BOTH)
        self.CreateStatusBar(1, wx.ST_SIZEGRIP)

        self.dying = False 
        self.skipLoad = False
    

        self.ReadConfigurationFile()
        self.externalDemos = HuntExternalDemos()
        
        # Create a Notebook
        self.nb = wx.Notebook(pnl, -1, style=wx.CLIP_CHILDREN)
        imgList = wx.ImageList(16, 16)
        
        for png in ["overview", "code", "demo"]:
            bmp = em_images.catalog[png].GetBitmap()
            imgList.Add(bmp)
        self.nb.AssignImageList(imgList)

        
        self.BuildMenuBar()
        

        # Create a TreeCtrl
        leftPanel = wx.Panel(pnl, style=wx.TAB_TRAVERSAL|wx.CLIP_CHILDREN)
        self.treeMap = {}
        
        self.tree = stat_tree.StatTree(leftPanel)
        

        self.RecreateTree()
        self.tree.SetExpansionState(self.expansionState)
        self.tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
        self.tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnTreeLeftDown)
        
        

        # Set the wxWindows log target to be this textctrl
        # 日志文件处理
        
        if conf.ENVIRONMENT == "dev":
            # 调试用记得以后关掉
            wx.Log_SetActiveTarget(wx.LogStderr())
            wx.Log_SetTraceMask(wx.TraceMessages)           
            self.Bind(wx.EVT_ACTIVATE, self.OnActivate)
            wx.GetApp().Bind(wx.EVT_ACTIVATE_APP, self.OnAppActivate)

        # add the windows to the splitter and split it.
        leftBox = wx.BoxSizer(wx.VERTICAL)
        leftBox.Add(self.tree, 1, wx.EXPAND)
        if 'wxMac' in wx.PlatformInfo:
            leftBox.Add((5,5))  # Make sure there is room for the focus ring
        leftPanel.SetSizer(leftBox)

        # 加载默认显示页面
        self.LoadMudule(0)
        # select initial items
        self.nb.SetSelection(0)
        self.tree.SelectItem(self.root)

        # Load 'Main' module
        self.loaded = True

        # select some other initial module?
        if len(sys.argv) > 1:
            arg = sys.argv[1]
            if arg.endswith('.py'):
                arg = arg[:-3]
            selectedDemo = self.treeMap.get(arg, None)
            if selectedDemo:
                self.tree.SelectItem(selectedDemo)
                self.tree.EnsureVisible(selectedDemo)

        # Use the aui manager to set up everything
        self.mgr.AddPane(self.nb, wx.aui.AuiPaneInfo().CenterPane().Name("Notebook"))
        self.mgr.AddPane(leftPanel,
                         wx.aui.AuiPaneInfo().
                         Left().Layer(2).BestSize((240, -1)).
                         MinSize((160, -1)).
                         Floatable(conf.ALLOW_AUI_FLOATING).FloatingSize((240, 700)).
                         CloseButton(False).
                         Name("StatTree"))

        self.auiConfigurations[conf.DEFAULT_PERSPECTIVE] = self.mgr.SavePerspective()
        self.mgr.Update()

        self.mgr.SetFlags(self.mgr.GetFlags() ^ wx.aui.AUI_MGR_TRANSPARENT_DRAG)
        



    def ReadConfigurationFile(self):

        self.auiConfigurations = {}
        self.expansionState = [0, 1]

        config = GetConfig()
        val = config.Read('ExpansionState')
        if val:
            self.expansionState = eval(val)

        val = config.Read('AUIPerspectives')
        if val:
            self.auiConfigurations = eval(val)
        

    def BuildMenuBar(self):

        # Make a File menu
        self.mainmenu = wx.MenuBar()
        menu = wx.Menu()
 
        exitItem = wx.MenuItem(menu, -1, 'E&xit\tCtrl-Q', 'Get the heck outta here!')
        exitItem.SetBitmap(em_images.catalog['exit'].GetBitmap())
        menu.AppendItem(exitItem)
        self.Bind(wx.EVT_MENU, self.OnFileExit, exitItem)
        wx.App.SetMacExitMenuItemId(exitItem.GetId())
        self.mainmenu.Append(menu, '&文件')

        # Make a Demo menu
        menu = wx.Menu()
        for indx, item in enumerate(conf._treeList[:-1]):
            menuItem = wx.MenuItem(menu, -1, item[0])
            submenu = wx.Menu()
            for childItem in item[1]:
                mi = submenu.Append(-1, childItem[0])
                self.Bind(wx.EVT_MENU, self.OnDemoMenu, mi)
            menuItem.SetBitmap(em_images.catalog[conf._statPngs[childItem[1]]].GetBitmap())
            menuItem.SetSubMenu(submenu)
            menu.AppendItem(menuItem)
        self.mainmenu.Append(menu, '&' + conf.tree_menu_name)

        # Make an Option menu
        # If we've turned off floatable panels then this menu is not needed
        if conf.ALLOW_AUI_FLOATING:
            menu = wx.Menu()
            auiPerspectives = self.auiConfigurations.keys()
            auiPerspectives.sort()
            perspectivesMenu = wx.Menu()
            item = wx.MenuItem(perspectivesMenu, -1, conf.DEFAULT_PERSPECTIVE, "Load startup default perspective", wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, self.OnAUIPerspectives, item)
            perspectivesMenu.AppendItem(item)
            for indx, key in enumerate(auiPerspectives):
                if key == conf.DEFAULT_PERSPECTIVE:
                    continue
                item = wx.MenuItem(perspectivesMenu, -1, key, "Load user perspective %d"%indx, wx.ITEM_RADIO)
                perspectivesMenu.AppendItem(item)
                self.Bind(wx.EVT_MENU, self.OnAUIPerspectives, item)

            menu.AppendMenu(wx.ID_ANY, "&AUI Perspectives", perspectivesMenu)
            self.perspectives_menu = perspectivesMenu

            item = wx.MenuItem(menu, -1, 'Save Perspective', 'Save AUI perspective')
            item.SetBitmap(em_images.catalog['saveperspective'].GetBitmap())
            menu.AppendItem(item)
            self.Bind(wx.EVT_MENU, self.OnSavePerspective, item)

            item = wx.MenuItem(menu, -1, 'Delete Perspective', 'Delete AUI perspective')
            item.SetBitmap(em_images.catalog['deleteperspective'].GetBitmap())
            menu.AppendItem(item)
            self.Bind(wx.EVT_MENU, self.OnDeletePerspective, item)

            menu.AppendSeparator()

            item = wx.MenuItem(menu, -1, 'Restore Tree Expansion', 'Restore the initial tree expansion state')
            item.SetBitmap(em_images.catalog['expansion'].GetBitmap())
            menu.AppendItem(item)
            self.Bind(wx.EVT_MENU, self.OnTreeExpansion, item)

            self.mainmenu.Append(menu, '&Options')
        
        # Make a Help menu
        menu = wx.Menu()

        helpItem = menu.Append(-1, '&关于BPD百星', 'wxPython RULES!!!')
        wx.App.SetMacAboutMenuItemId(helpItem.GetId())
        
        self.Bind(wx.EVT_MENU, self.OnHelpAbout, helpItem)
        
        self.mainmenu.Append(menu, '&帮助')
        self.SetMenuBar(self.mainmenu)

            

    #---------------------------------------------    
    def RecreateTree(self, evt=None):
        # Catch the search type (name or content)
        expansionState = self.tree.GetExpansionState()

        current = None
        item = self.tree.GetSelection()
        if item:
            prnt = self.tree.GetItemParent(item)
            if prnt:
                current = (self.tree.GetItemText(item),
                           self.tree.GetItemText(prnt))
                    
        self.tree.Freeze()
        self.tree.DeleteAllItems()
        self.root = self.tree.AddRoot("管理")
        self.tree.SetItemImage(self.root, 10)
        self.tree.SetItemPyData(self.root, 1)

                    
        firstChild = None
        selectItem = None
        
        for category, items in conf._treeList:
            if items:
                child = self.tree.AppendItem(self.root, category, image=15)
                self.tree.SetItemPyData(child, 0)
                if not firstChild: firstChild = child
                for childItem in items:
                    image = childItem[1]
                    if DoesModifiedExist(childItem[0]):
                        image = childItem[1]
                    theItem = self.tree.AppendItem(child, childItem[0], image=image)
                    self.tree.SetItemPyData(theItem, childItem[2])
                    self.treeMap[childItem] = theItem
                    if current and (childItem, category) == current:
                        selectItem = theItem
                        
                    
        if firstChild:
            self.tree.Expand(firstChild)
        if filter:
            self.tree.ExpandAll()
        elif expansionState:
            self.tree.SetExpansionState(expansionState)
        if selectItem:
            self.skipLoad = True
            self.tree.SelectItem(selectItem)
            self.skipLoad = False
        
        self.tree.Thaw()
        self.searchItems = {}

        
    def WriteText(self, text):
        if text[-1:] == '\n':
            text = text[:-1]
        wx.LogMessage(text)

    def write(self, txt):
        self.WriteText(txt)

    #---------------------------------------------
    def OnItemExpanded(self, event):
        item = event.GetItem()
        wx.LogMessage("OnItemExpanded: %s" % self.tree.GetItemText(item))
        event.Skip()

    #---------------------------------------------
    def OnItemCollapsed(self, event):
        item = event.GetItem()
        wx.LogMessage("OnItemCollapsed: %s" % self.tree.GetItemText(item))
        event.Skip()

    #---------------------------------------------
    def OnTreeLeftDown(self, event):
        # reset the overview text if the tree item is clicked on again
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if item == self.tree.GetSelection():
            self.SetView(self.tree.GetItemText(item)+" Overview", self.curView)
        event.Skip()

    #---------------------------------------------
    def OnSelChanged(self, event):
        if self.dying or not self.loaded or self.skipLoad:
            return
        
        item = event.GetItem()
        
        mid = self.tree.GetItemIdentity(item)
        self.LoadMudule(mid)


    #---------------------------------------------
    def LoadMudule(self, mId):
        if mId == 100:  #退出
            self.Close()
        else:
            try:
                wx.BeginBusyCursor()
                self.pnl.Freeze()
                
                os.chdir(self.cwd)
                
                self.statModules = modules.Modules("%s/%s"%("ui", conf._modules[mId][0]), conf._modules[mId][1])
                
                self.ActiveModuleChanged()
    
            finally:
                wx.EndBusyCursor()
                self.pnl.Thaw()
        
        

    def ReloadStat(self):
        if self.statModules.name != __name__:
            self.RunModule()
    
    def ActiveModuleChanged(self):
        self.pnl.Freeze()        
        self.ReloadStat()
        self.pnl.Thaw()
        
        #---------------------------------------------
    def ShutdownStatModule(self):
        if self.statPage is not None:
            # inform the window that it's time to quit if it cares
            if hasattr(self.statPage, "ShutdownStat"):
                self.statPage.ShutdownStat()
            self.nb.RemovePage(0)
            wx.YieldIfNeeded() # in case the page has pending events
            self.statPage = None               
    #---------------------------------------------
    def RunModule(self):
        """Runs the active module"""
        module = self.statModules.GetActive()
       
        self.ShutdownStatModule()
        
        if module is not None:
            wx.LogMessage("Running stat module...")
            self.statPage = module.Load(self.nb, self)
            self.SetView(self.statModules.caption, self.statPage)
        
    #---------------------------------------------
    def SetView(self, name, mView):
        self.nb.AddPage(mView,name ,0)

    #---------------------------------------------
    # Menu methods
    def OnFileExit(self, *event):
        self.Close()






    def OnTreeExpansion(self, event):
        self.tree.SetExpansionState(self.expansionState)
        
 
    def OnHelpAbout(self, event):
        from about import AboutBox
        about = AboutBox(self) 
        about.ShowModal()
        about.Destroy()


        
    #---------------------------------------------
    def OnCloseWindow(self, event):
        retCode = MessageBox("确认退出系统","退出")
        if retCode == wx.YES:
    
            config = GetConfig()
            config.Write('ExpansionState', str(self.tree.GetExpansionState()))
            config.Write('AUIPerspectives', str(self.auiConfigurations))
            config.Flush()
            statlog.StatLog.close_log_file() 
            self.Destroy()
            
        else:
            pass


    #---------------------------------------------
    def OnIdle(self, event):
        if self.otherWin:
            self.otherWin.Raise()
            self.statPage = self.otherWin
            self.otherWin = None


    #---------------------------------------------
    def OnDemoMenu(self, event):
        try:
            selectedDemo = self.treeMap[self.mainmenu.GetLabel(event.GetId())]
        except:
            selectedDemo = None
        if selectedDemo:
            self.tree.SelectItem(selectedDemo)
            self.tree.EnsureVisible(selectedDemo)



    #---------------------------------------------
    def OnIconfiy(self, evt):
        wx.LogMessage("OnIconfiy: %s" % evt.Iconized())
        evt.Skip()

    #---------------------------------------------
    def OnMaximize(self, evt):
        wx.LogMessage("OnMaximize")
        evt.Skip()

    #---------------------------------------------
    def OnActivate(self, evt):
        wx.LogMessage("OnActivate: %s" % evt.GetActive())
        evt.Skip()

    #---------------------------------------------
    def OnAppActivate(self, evt):
        wx.LogMessage("OnAppActivate: %s" % evt.GetActive())
        evt.Skip()
        







