#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
'''
Created on 2012-11-19

@author: daimin
'''
'''
目录树
'''

tree_menu_name = "管理"

_statPngs = ["overview", "recent", "frame", "dialog", "moredialog", "core",
             "book", "customcontrol", "morecontrols", "layout", "process", "clipboard",
             "images", "miscellaneous","exit","expansion"]

_treeList = [
    # new stuff
    ('报表管理', [
        ('报表列表',9,1),  # 节点名称,图标序列号,ID
        ]),

    ('设备管理', [
        ('添加设备', 4,2),
        ('设备列表',9,3),
        ]),
             
    ('客户管理', [
        ('添加客户',4,4),
        ('客户列表',9,5),
        ]), 
                         
    ('档案类型管理', [
        ('添加档案类型',4,6),
        ('档案类型列表',9,7)
        ]),
             
    ('操作员管理', [
        ('添加操作员',4,8),
        ('操作员列表',9,9)
        ]),   
                       
    ('系统管理', [
        ('退出',14,10),
        ]),   
]



APP_NAME = "BPD百星打印中心日结登记系统"
#---------------------------------------------------------------------------------
ALLOW_AUI_FLOATING = False
DEFAULT_PERSPECTIVE = "Default Perspective"

#---------------------------------------------------------------------------
# Constants for module versions

modOriginal = 0
modModified = 1
modDefault = modOriginal

#---------------------------------------------------------------------------

log_dir = "log/"

#---------------------------------------------------------------------------
ENVIRONMENT = "DEV"
#---------------------------------------------------------------------------

mainOverview = """<html><body>
<h2>wxPython</h2>

<p> wxPython is a <b>GUI toolkit</b> for the Python programming
language.  It allows Python programmers to create programs with a
robust, highly functional graphical user interface, simply and easily.
It is implemented as a Python extension module (native code) that
wraps the popular wxWindows cross platform GUI library, which is
written in C++.

<p> Like Python and wxWindows, wxPython is <b>Open Source</b> which
means that it is free for anyone to use and the source code is
available for anyone to look at and modify.  Or anyone can contribute
fixes or enhancements to the project.

<p> wxPython is a <b>cross-platform</b> toolkit.  This means that the
same program will run on multiple platforms without modification.
Currently supported platforms are 32-bit Microsoft Windows, most Unix
or unix-like systems, and Macintosh OS X. Since the language is
Python, wxPython programs are <b>simple, easy</b> to write and easy to
understand.

<p> <b>This demo</b> is not only a collection of test cases for
wxPython, but is also designed to help you learn about and how to use
wxPython.  Each sample is listed in the tree control on the left.
When a sample is selected in the tree then a module is loaded and run
(usually in a tab of this notebook,) and the source code of the module
is loaded in another tab for you to browse and learn from.

"""
