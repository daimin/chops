#!/usr/bin/env python
# -*- coding:gbk -*-
#encoding=gbk
log_dir = "/data0/log/"
#log_dir = "D:/www/pyscripts/log/"

mysqlhost="localhost"
database='pk_mahjong'
username='root'
password='123456'
#password='daimin'
# Is display exception info? 
PK_LOG = False
# RMB to game money
MONEY_RATE = 1000000


ROBOT_NAME_PREFIX   = "_i.robot_"       #��������ǰ׺ 

##################�ֻ���Ϣ����######################
OPERATORS_TYPES = [1,2,3]             # 1���й��ƶ� 2 ���й���ͨ 3���й�����
    
NETWORK_TYPES = [1,2,3]               # 1��WIFI 2��3G 3��2G



######################��Ӫ������#################################
#[1,"1-59��"],[2,"1-5����"],[3,"5-10����"],[4,"10-30����"],[5,"30-60����"],
#[6,"60-120����"],[7,"120�C240����"],[8,"240�C360����"],[9,"360��������"]
ONLINE_TIME_TYPES = [1,2,3,4,5,6,7,8,9]