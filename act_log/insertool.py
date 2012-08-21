#!/usr/bin/python
# -*- coding:GBK -*-   
#encoding=GBK


import os
import sys
import MySQLdb 
import datetime
import time
from config import *
from os.path import *
import codecs

CSV_DATE_FORMAT = '%Y-%m-%d %H:%M'

def trim(str):
    return str.strip()

def connect_database(host2, db2, user2, passwd2) :
    try: conn = MySQLdb.connect(db = db2, host = host2, user = user2, passwd = passwd2, charset="utf8", unix_socket="/var/lib/mysql/mysql.sock")
    except MySQLdb.Error,e:
        print "Cannot connect to server"
        print "Error code:", e.args[0]
        print "Error message:", e.args[1]
        return 0
    return conn

#插入pay_detail中的关键PID
def updatePay_detail(cur):
    cur.execute("select username,paytime from pay_detail")
    for username,paytime in cur.fetchall():
        pid = username+paytime.strftime('%Y%m%d%H%M%S')
        print pid
        cur.execute("update pay_detail set pid='"+pid+"' where username='"+username+"'")

if __name__ == "__main__":
    
    #reload(sys)
    #sys.setdefaultencoding('gbk')
    
    
    conn = connect_database(mysqlhost, database, username, password)
    if  conn == 0 :
        print "connect to database error!"
        sys.exit (1)
    cur = conn.cursor()
    
    logfile = codecs.open("Book_alinopay.csv",'r','GBK')
    linestrs = logfile.readlines()
    ccount = 0
    for line in linestrs:
        line = trim(line)
        litems = line.split(",")
        ord =   trim(litems[0])
        ctime = trim(litems[1])
        money = trim(litems[2])

        username = ""
        nickname = ""
        # get the create time.
        ptime = time.strptime(ctime, CSV_DATE_FORMAT)
        screatetime = time.strftime('%Y-%m-%d %H:%M:%S', ptime)
        screatedate = time.strftime('%Y-%m-%d',ptime)
        ords = ord.split("_")
        if len(ords) >= 2:
            username = ords[2]
        if username <> '':
            pid = username+time.strftime('%Y%m%d%H%M%S',ptime)
            cur.execute("select nickname from userinfo where username='%s'" % (username))
            row = cur.fetchone()
            if row:
                nickname = row[0]
            #获取nickname
            sql = "insert into pay_detail(`pid`,`username`,`nickname`,mney,paytime) values('%s','%s','%s',%d,'%s')" % (pid,username,nickname,int(money),screatetime)
            try:
                cur.execute(sql)
                ccount = ccount + 1
            except:
               pass
        print 'total insert %d item' %(ccount)
    #updatePay_detail(cur)
    
    conn.commit() 
    cur.close()
    conn.close()
    
    
    
    

    

   
    
