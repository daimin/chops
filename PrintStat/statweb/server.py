#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8

import sys,os
os.chdir("..")
sys.path.append(os.getcwd()) 
os.chdir("statweb")

import web



import dbs.query

import conf

from functions import *

urls = (
    '/', 'index'
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

        return xmltext

if __name__ == "__main__":
    

    sys.argv.append(conf.APP_PORT)
    app = web.application(urls, globals())
    app.run()