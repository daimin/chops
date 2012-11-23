#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
'''
Created on 2012-11-19

@author: daimin
'''

# 模块类别
_modules = {
  0 : ("GridSimple","简单表格"),
  1 : ("GridSimple","简单表格"),
  2 : ("",""),
          
}

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
        ('报表列表',9,1),  # 节点名称,图标序列号,模块ID
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
        ('服务器管理',13,10),
        ('退出',14,100),
        ]),   
]




APP_NAME = "BPD百星打印中心日结登记系统"
# 框架的宽度和高度
FRAME_WIDTH = 1024
FRAME_HEIGHT = 768
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

#数据库配置 -------------------------------------------------------------

DB_FILE = "../data/printstat.db"


CUSTOM_TAB = "create table if not exists `customs`(name varchar(40) not null default '',\
 `date` date not null default '0000-00-00',primary key(`name`))"

PRINTER_TAB = "create table if not exists `printer`(\
id varchar(40) not null default '', \
`type` varchar(40) not null default '',\
ANUM varchar(40) not null default '',\
sqlnum varchar(20) not null default '',\
`date` date not null default '0000-00-00'\
,primary key(`id`))"

ARCHIVES_TYPE_TAB = "create table if not exists `archives_type`(name varchar(20) not null default '',primary key(name))"

ADMIN_TAB = "create table if not exists `admin`(name not null default '',password not null default '',primary key(name))"

DAILY_STAT_TAB = \
"create table if not exists `daily_stat`(\
id integer primary key autoincrement,\
`date` date not null default '0000-00-00',\
PID varchar(40) not null default '',\
customname varchar(40) not null default '',\
archives_type varchar(20) not null default '',\
num integer not null default 0,\
post_time datetime not null default '0000-00-00 00:00:00',\
finish_time datetime not null default '0000-00-00 00:00:00',\
init_num integer not null default 0,\
finish_num integer not null default 0,\
adminname varchar(40) not null default '',\
scrap_num integer not null default 0,\
memo TEXT not null default ''\
)"



