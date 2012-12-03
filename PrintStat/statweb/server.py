#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8

import sys,os
os.chdir("..")
sys.path.append(os.getcwd()) 
os.chdir("statweb")

import web
import web.webapi
import xml.dom.minidom  


import dbs.query

import conf

from functions import *

urls = (
        '/', 'index',
        '/put_data', 'putData',
        '/display', 'display'
)

class index:
    def GET(self):
        web.header('Content-Type', 'text/xml')
        xmltext = '<?xml version="1.0" encoding="utf-8"?>'
        xmltext = "%s<data>" %(xmltext)
        
        xmltext = '%s<items name="printer">' %(xmltext)
        xmltext = "%s%s" %(xmltext, array2xml(dbs.query.get_printer_ids()))
        xmltext = "%s</items>" %(xmltext)
        
        xmltext = '%s<items name="custom">' %(xmltext)
        xmltext = "%s%s" %(xmltext, array2xml(dbs.query.get_printer_customs()))
        xmltext = "%s</items>" %(xmltext)
        
        xmltext = '%s<items name="archives_type">' %(xmltext)
        xmltext = "%s%s" %(xmltext, array2xml(dbs.query.get_printer_archives_types()))
        xmltext = "%s</items>" %(xmltext)
        
        xmltext = '%s<items name="admin">' %(xmltext)
        xmltext = "%s%s" %(xmltext, array2xml(dbs.query.get_printer_admins()))
        xmltext = "%s</items>" %(xmltext)
        
        xmltext = "%s</data>" %(xmltext)

        dbs.query.close()
        return xmltext

class putData:
    def POST(self):
        inputData = web.input()
        xmldata = inputData.popitem()[0]
        
        if xmldata:
             doc = xml.dom.minidom.parseString(xmldata)  
             for node in doc.getElementsByTagName("xinghao"):
                 print node.firstChild.nodeValue
             for node in doc.getElementsByTagName("num"):
                 print node.firstChild.nodeValue
        
        return xmldata
        
    def GET(self):
        return self.POST()
    
class display:
    def GET(self):
        web.header('Content-Type', 'text/html;charset=UTF-8')
        result = dbs.query.get_daily_stat()
        htmltxt = '<!DOCTYPE html><!--STATUS OK--><html><head><style type="text/css">\
        body{font-size:12px;} .tab{margin:0 auto;border:1px solid #000;}.tab th{background:#ccc;}.tab td1{background:#cdc;}</style></head><body>'
        htmltxt = '%s<table cellpadding="3" cellspacing="1" class="tab" border="0" style="width:900px;">' %(htmltxt)
        htmltxt = '%s<tr><th>ID</th><th>打印机编号</th><th>客户名称</th><th>档案类型</th><th>打印数量</th><th>发送时间</th><th>完成时间\
        </th><th>初始值</th><th>完成值</th><th>纸张报废数</th><th>录入日期</th><th>录入人</th></tr>' %(htmltxt)
        for did,date,PID,customname,archives_type,num,post_time,finish_time,init_num,finish_num,adminname,scrap_num in result:
            htmltxt = '%s<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%d</td><td>%d</td><td>%s</td><td>%s</td></tr>'\
             %(htmltxt,did,PID,customname,archives_type,num,post_time,finish_time,init_num,finish_num,scrap_num,date,adminname)
        htmltxt = "%s</body></html>" %(htmltxt)   
        return htmltxt
        
        

if __name__ == "__main__":
    

    sys.argv.append(conf.APP_PORT)
    app = web.application(urls, globals())
    app.run()