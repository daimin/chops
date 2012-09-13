#!/usr/bin/python
# -*- coding: gbk -*-
#encoding=gbk
#author=daimin
'''
Created on 2012-8-22

@author: daimin
'''
import MySQLdb
from common import *
from config import *

class Db(object):
    '''
    classdocs
    '''
    conn = None
    
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    @staticmethod
    def get_conn() :
        """连接数据库
        """
        if Db.conn == None:
            try: 
                Db.conn = MySQLdb.connect(db = database, host = mysqlhost, user = username, passwd = password, charset="gbk", unix_socket="/var/lib/mysql/mysql.sock")
            except MySQLdb.Error,e:
                pk_log("Cannot connect to server")
                pk_log("Error code:", e.args[0])
                pk_log("Error message:", e.args[1])
                return 0
        return Db.conn
        
    @staticmethod
    def close():
        """关闭数据库
        """
        if Db.conn <> None:
            Db.conn.commit()
            Db.conn.close()
        