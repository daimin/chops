#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
'''
Created on 2012-11-19

@author: daimin
'''

import wx

import conf
import error_panel

from functions import *

class Modules:
    """
    Dynamically manages the original/modified versions of a demo
    module
    """
    def __init__(self, name, caption):
        self.modActive = -1
        self.name = name
        self.caption = caption
        
        #              (dict , source ,  filename , description   , error information )        
        #              (  0  ,   1    ,     2     ,      3        ,          4        )        
        self.modules = [[dict(),  ""    ,    ""     , "<original>"  ,        None],
                        [dict(),  ""    ,    ""     , "<modified>"  ,        None]]
        
        for i in [conf.modOriginal, conf.modModified]:
            self.modules[i][0]['__file__'] = \
                os.path.join(os.getcwdu(), GetOriginalFilename(name))
            
        # load original module
        if name.find(".") <> -1:
            name = name.replace(".", '/')
        
        self.LoadFromFile(conf.modOriginal, GetOriginalFilename(name))
        self.SetActive(conf.modOriginal)

        # load modified module (if one exists)
        if DoesModifiedExist(name):
            self.LoadFromFile(conf.modModified, GetModifiedFilename(name))


    def LoadFromFile(self, modID, filename):
        self.modules[modID][2] = filename
        
        file = open(filename, "rt")
        self.LoadFromSource(modID, file.read())
        file.close()


    def LoadFromSource(self, modID, source):
        self.modules[modID][1] = source
        self.LoadDict(modID)


    def LoadDict(self, modID):
        if self.name != __name__:
            source = self.modules[modID][1]
            description = self.modules[modID][2]
            description = description.encode(sys.getfilesystemencoding())
            
            try:
                code = compile(source, description, "exec")        
                exec code in self.modules[modID][0]
            except:
                self.modules[modID][4] = error_panel.StatError(sys.exc_info())
                self.modules[modID][0] = None
            else:
                self.modules[modID][4] = None


    def SetActive(self, modID):
        if modID != conf.modOriginal and modID != conf.modModified:
            raise LookupError
        else:
            self.modActive = modID


    def GetActive(self):
        dict = self.modules[self.modActive][0]
        if dict is None:
            return None
        else:
            return ModuleDictWrapper(dict)


    def GetActiveID(self):
        return self.modActive

    
    def GetSource(self, modID = None):
        if modID is None:
            modID = self.modActive
        return self.modules[modID][1]


    def GetFilename(self, modID = None):
        if modID is None:
            modID = self.modActive
        return self.modules[self.modActive][2]


    def GetErrorInfo(self, modID = None):
        if modID is None:
            modID = self.modActive
        return self.modules[self.modActive][4]


    def Exists(self, modID):
        return self.modules[modID][1] != ""


    def UpdateFile(self, modID = None):
        """Updates the file from which a module was loaded
        with (possibly updated) source"""
        if modID is None:
            modID = self.modActive

        source = self.modules[modID][1]
        filename = self.modules[modID][2]

        try:        
            file = open(filename, "wt")
            file.write(source)
        finally:
            file.close()


    def Delete(self, modID):
        if self.modActive == modID:
            self.SetActive(0)

        self.modules[modID][0] = None
        self.modules[modID][1] = ""
        self.modules[modID][2] = ""
            
#---------------------------------------------------------------------------

class ModuleDictWrapper:
    """Emulates a module with a dynamically compiled __dict__"""
    def __init__(self, dict):
        self.dict = dict
        
    def __getattr__(self, name):
        if name in self.dict:
            return self.dict[name]
        else:
            raise AttributeError
