#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
'''
Created on 2012-11-23

@author: daimin
所有查询的代码
'''
import db
import conf

customsql = ""

def get_printer_ids():
    ids = []
    conn = db.Db.getConn()
    cur = conn.cursor() 
    query = "select id from printer"
    cur.execute(query)
    result = cur.fetchall()
    for pid in result:
        ids.append(pid[0])
    conn.commit()
    cur.close()
    return ids
    
def get_printer_customs():
    cnames = []
    conn = db.Db.getConn()
    cur = conn.cursor() 
    query = "select name from customs"
    cur.execute(query)
    result = cur.fetchall()
    for cname in result:
        cnames.append(cname[0])
    conn.commit()
    cur.close()
    return cnames

def get_printer_archives_types():
    atypes = []
    conn = db.Db.getConn()
    cur = conn.cursor() 
    query = "select name from archives_type"
    cur.execute(query)
    result = cur.fetchall()
    for aname in result:
        atypes.append(aname[0])
    conn.commit()
    cur.close()
    return atypes

def get_printer_admins():
    adminnames = []
    conn = db.Db.getConn()
    cur = conn.cursor() 
    query = "select name from admin"
    cur.execute(query)
    result = cur.fetchall()
    for aname in result:
        adminnames.append(aname[0])
    conn.commit()
    cur.close()
    return adminnames


if __name__ == "__main__":
    print get_printer_ids()
    