#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
'''
Created on 2012-11-23

@author: daimin

实现数据库链接的单例
'''
import sqlite3
import conf

class Db(object):
    conn = None
    @staticmethod
    def getConn():
        if Db.conn == None:
            Db.conn = sqlite3.connect(conf.DB_FILE)
        return Db.conn
    
    @staticmethod
    def close():
        if Db.conn <> None:
            Db.conn.close()
            Db.conn = None
