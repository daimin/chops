#!/usr/bin/env python
# -*- coding:gbk -*-
#encoding=gbk
#log_dir = "/data0/log/"
log_dir = "D:/www/pyscripts/log/"

mysqlhost="localhost"
database='pk_mahjong'
username='root'
#password='123456'
password='daimin'
# Is display exception info? 
PK_LOG = False
# RMB to game money
MONEY_RATE = 1000000


ROBOT_NAME_PREFIX   = "_i.robot_"       #机器人名前缀 

##################手机信息定义######################
OPERATORS_TYPES = [1,2,3]             # 1：中国移动 2 ：中国联通 3：中国电信
    
NETWORK_TYPES = [1,2,3]               # 1：WIFI 2：3G 3：2G



######################运营分析类#################################
#[1,"1-59秒"],[2,"1-5分钟"],[3,"5-10分钟"],[4,"10-30分钟"],[5,"30-60分钟"],
#[6,"60-120分钟"],[7,"120–240分钟"],[8,"240–360分钟"],[9,"360分钟以上"]
ONLINE_TIME_TYPES = [1,2,3,4,5,6,7,8,9]
