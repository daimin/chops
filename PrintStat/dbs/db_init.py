#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
'''
Created on 2012-11-23

@author: daimin
'''
import db
import conf

customsql = ""

def init_customs():
    conn = db.Db.getConn()
    cur = conn.cursor() 
    cur.execute(conf.ADMIN_TAB) 
    cur.execute(conf.CUSTOM_TAB)
    cur.execute(conf.ARCHIVES_TYPE_TAB) 
    cur.execute(conf.PRINTER_TAB) 

    cur.execute(conf.DAILY_STAT_TAB) 
    conn.commit()
    cur.close()
    
if __name__ == "__main__":
    init_customs()
    