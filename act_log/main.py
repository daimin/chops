#!/usr/bin/python
# -*- coding:gbk -*-   
#encoding=gbk
#author=daimin
"""

主运行文件

"""
import os
import sys
from os.path import *
from do_parse_log import *


if __name__ == "__main__":

    #reload(sys)
    #sys.setdefaultencoding('gbk')
    parse()
    print "######### Parse Success!!! #################"
