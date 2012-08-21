﻿#!/usr/bin/python
# -*- coding:UTF-8 -*-   
#encoding=utf-8


import os
import sys
import MySQLdb 
import datetime
from config import *
from os.path import *



def connect_database(host2, db2, user2, passwd2) :
    try: conn = MySQLdb.connect(db = db2, host = host2, user = user2, passwd = passwd2, charset="utf8", unix_socket="/var/lib/mysql/mysql.sock")
    except MySQLdb.Error,e:
        print "Cannot connect to server"
        print "Error code:", e.args[0]
        print "Error message:", e.args[1]
        return 0
    return conn
    
def up_pay_user(cur):
    cur.execute('select username,count(username) as ucount from pay_detail group by username')
    for username,ucount in cur.fetchall():
        #sql = "select pay_time from userinfo where username='%s'" % (username)
        sql = "update userinfo set pay_time=%d where username='%s'" % (ucount,username)
        cur.execute(sql)
        #onerow = cur.fetchone()
        #if onerow:
        #    print onerow[0]
        
def getPid(username, iap_time):
    return username + iap_time.strftime('%Y%m%d%H%M%S')


def up_payboard(cur):
    cur.execute("update payboard set mney=0")
    cur.execute('select sum(mney) as smney,DATE_FORMAT(min(paytime),"%Y-%m-%d") as first_pay_time,username,nickname,paytime from pay_detail group by username')
    for smney,first_pay_time,username,nickname,paytime in cur.fetchall():
        pid = getPid(username,paytime)
        sql = "select count(username) as ucount from payboard where username='%s'" % (username)
        cur.execute(sql)
        ucount = cur.fetchone()
        if ucount <> None:
            if int(ucount[0]) <= 0:
                sql = "insert into payboard(`pid`,`username`,`nickname`,`mney`,`first_pay_time`) values('%s','%s','%s',%f,'%s')" %(pid,username,nickname,smney,first_pay_time)
            else:
                sql = "update payboard set mney=mney+%f where username='%s'" %(smney, username)
            cur.execute(sql)
        #cur.execute("update payboard set first_pay_time='%s' where username='%s'" %(first_pay_time,username))
            
def insert_retention_rate(cur):
    now = datetime.datetime.now()
    for i in range(0,30):
        pday = now - datetime.timedelta(days = i )
        psday =  pday.strftime("%Y-%m-%d")
        sql = "insert into retention_rate(regdate,1_num,2_num,3_num,4_num,5_num,6_num,7_num,8_num) \
        values('%s',0,0,0,0,0,0,0,0)" % (psday)
        cur.execute(sql)
    
if __name__ == "__main__":
    
    #reload(sys)
    #sys.setdefaultencoding('utf-8')
    
    
    conn = connect_database(mysqlhost, database, username, password)
    if  conn == 0 :
        print "connect to database error!"
        sys.exit (1)
    cur = conn.cursor()
    up_payboard(cur)
    #up_pay_user(cur)
    #insert_retention_rate(cur)
        
        
    conn.commit()
    
    cur.close()
    conn.close()
    
    
    
    

    

   
    
