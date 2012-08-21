#!/usr/bin/python
# -*- coding:GBK -*-   
#encoding=GBK


import os
import sys
import MySQLdb 
import datetime
from config import *
from os.path import *


"""
"""
def connect_database(host2, db2, user2, passwd2) :
    try: conn = MySQLdb.connect(db = db2, host = host2, user = user2, passwd = passwd2, charset="gbk", unix_socket="/var/lib/mysql/mysql.sock")
    except MySQLdb.Error,e:
        print "Cannot connect to server"
        print "Error code:", e.args[0]
        print "Error message:", e.args[1]
        return 0
    return conn

if __name__ == "__main__":
    
    #reload(sys)
    #sys.setdefaultencoding('utf-8')
    
    
    conn = connect_database(mysqlhost, database, username, password)
    if  conn == 0 :
        print "connect to database error!"
        sys.exit (1)
    cur = conn.cursor()
    logfile = open("langs.txt",'r')
        
    lines = logfile.readlines()
    for line in lines:
        line = line.strip()
        code = line[0:line.index(" ")]
        cap = line[line.index(" ")+1:]
        cur.execute("replace into langcode(`code`,`caption`) values('%s','%s')" % (code , cap))
    conn.commit() 
    cur.close()
    conn.close()
    
    
    
    

    

   
    
