#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
'''
Created on 2012-11-21

@author: daimin
'''
import os
import datetime
import sqlite3
import hashlib

admins = ["刘一","陈二","张三","李四","王五","赵六","孙七","周八","吴九","郑十"]

archives_type = ['图纸','图表','文本']
if __name__ == "__main__":
    cx = sqlite3.connect("../data/printstat.db")
    cur = cx.cursor() 
    
    #cu.execute("insert into catalog values(0, 0, 'name1')") 
    #cu.execute("insert into catalog values(1, 0, 'hello')") 
    #cx.commit()
    #cu.execute("select * from catalog") 
    #print cu.fetchall() 
    #cu.close()
    #cx.close()
    dt = datetime.datetime.now()
    curday = dt.strftime('%Y-%m-%d')
    
    for i in range(1,100):
        sqlnum = "%03d"%(i)
        ptype = "针孔"
        if i % 3 == 0:
            ptype = "激光"
        IDNAME =  "BEIXING-GZ%s" %(sqlnum)
        try:
            sql = "insert into printer(id,`type`,anum,sqlnum,date) values('%s','%s','%s','%s','%s')" %(IDNAME,ptype,IDNAME,sqlnum,curday)
            cur.execute(sql)
        except:
            pass
    cx.commit()
    
    default_pass = hashlib.md5('123')
    for aname in admins:
        sql = "insert into admin(name,`password`) values('%s','%s')" %(aname,default_pass)
        cur.execute(sql)
    cx.commit()
    
    for atype in archives_type:
        sql = "insert into archives_type(name) values('%s')" %(atype) 
        cur.execute(sql)
    cx.commit()

    
    for i in range(1,44):
        sqlnum = "%03d"%(i)
        CNAME =  "CUSTOM-%s" %(sqlnum)

        sql = "insert into customs(name,`date`) values('%s','%s')" %(CNAME,curday)
        cur.execute(sql)
    cx.commit()
    
    
    cx.commit()
    cur.close()
    cx.close()