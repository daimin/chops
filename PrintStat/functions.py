#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
'''
Created on 2012-11-19

@author: daimin
'''
import os,sys

import wx
import conf


images = None

def opj(path):
    """Convert paths to the platform-specific separator"""
    st = apply(os.path.join, tuple(path.split('/')))
    # HACK: on Linux, a leading / gets lost...
    if path.startswith('/'):
        st = '/' + st
    return st


def GetDataDir():
    """
    Return the standard location on this platform for application data
    """
    sp = wx.StandardPaths.Get()
    return sp.GetUserDataDir()


def GetModifiedDirectory():
    """
    Returns the directory where modified versions of the demo files
    are stored
    """
    return os.path.join(GetDataDir(), "modified")


def GetModifiedFilename(name):
    """
    Returns the filename of the modified version of the specified demo
    """
    if not name.endswith(".py"):
        name = name + ".py"
    return os.path.join(GetModifiedDirectory(), name)


def GetOriginalFilename(name):
    """
    Returns the filename of the original version of the specified demo
    """
    if not name.endswith(".py"):
        name = name + ".py"

    if os.path.isfile(name):
        return name
    
    originalDir = os.getcwd()
    listDir = os.listdir(originalDir)
    # Loop over the content of the demo directory
    for item in listDir:
        if not os.path.isdir(item):
            # Not a directory, continue
            continue
        dirFile = os.listdir(item)
        # See if a file called "name" is there
        if name in dirFile:        
            return os.path.join(item, name)

    # We must return a string...
    return ""


def DoesModifiedExist(name):
    """Returns whether the specified demo has a modified copy"""
    if os.path.exists(GetModifiedFilename(name)):
        return True
    else:
        return False


def GetConfig():
    if not os.path.exists(GetDataDir()):
        os.makedirs(GetDataDir())

    config = wx.FileConfig(
        localFilename=os.path.join(GetDataDir(), "options"))
    return config


def SearchDemo(name, keyword):
    """ Returns whether a demo contains the search keyword or not. """
    fid = open(GetOriginalFilename(name), "rt")
    fullText = fid.read()
    fid.close()
    if type(keyword) is unicode:
        fullText = fullText.decode('iso8859-1')
    if fullText.find(keyword) >= 0:
        return True

    return False    


def HuntExternalDemos():
    """
    Searches for external demos (i.e. packages like AGW) in the wxPython
    demo sub-directories. In order to be found, these external packages
    must have a __demo__.py file in their directory.
    """

    externalDemos = {}
    originalDir = os.getcwd()
    listDir = os.listdir(originalDir)
    # Loop over the content of the demo directory
    for item in listDir:
        if not os.path.isdir(item):
            # Not a directory, continue
            continue
        dirFile = os.listdir(item)
        # See if a __demo__.py file is there
        if "__demo__.py" in dirFile:
            # Extend sys.path and import the external demos
            sys.path.append(item)
            externalDemos[item] = __import__("__demo__")

    if not externalDemos:
        # Nothing to import...
        return {}

    # Modify the tree items and icons
    index = 0
    for category, demos in conf._treeList:
        # We put the external packages right before the
        # More Windows/Controls item
        if category == "More Windows/Controls":
            break
        index += 1

    # Sort and reverse the external demos keys so that they
    # come back in alphabetical order
    keys = externalDemos.keys()
    keys.sort()
    keys.reverse()

    # Loop over all external packages
    for extern in keys:
        package = externalDemos[extern]
        # Insert a new package in the _treeList of demos
        conf._treeList.insert(index, package.GetDemos())
        # Get the recent additions for this package
        conf._treeList[0][1].extend(package.GetRecentAdditions())
        # Extend the demo bitmaps and the catalog
        conf._demoPngs.insert(index+1, extern)
        images.catalog[extern] = package.GetDemoBitmap()

    # That's all folks...
    return externalDemos


def LookForExternals(externalDemos, demoName):
    """
    Checks if a demo name is in any of the external packages (like AGW) or
    if the user clicked on one of the external packages parent items in the
    tree, in which case it returns the html overview for the package.
    """

    pkg = overview = None
    # Loop over all the external demos
    for key, package in externalDemos.items():
        # Get the tree item name for the package and its demos
        treeName, treeDemos = package.GetDemos()
        # Get the overview for the package
        treeOverview = package.GetOverview()
        if treeName == demoName:
            # The user clicked on the parent tree item, return the overview
            return pkg, treeOverview
        elif demoName in treeDemos:
            # The user clicked on a real demo, return the package
            return key, overview

    # No match found, return None for both
    return pkg, overview