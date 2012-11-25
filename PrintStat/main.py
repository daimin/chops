#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
'''
Created on 2012-11-19

@author: daimin
'''
import os 

import ui.statapp

def main():
    try:
        appPath = os.path.dirname(__file__)
        os.chdir(appPath)
    except:
        pass
    app = ui.statapp.StatApp(False)
    
    app.MainLoop()
    

if __name__ == '__main__':
    main()
