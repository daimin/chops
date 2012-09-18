#!/usr/bin/env python
# -*- coding:UTF-8 -*-   
#encoding=utf-8
'''
Created on 2012-9-18

@author: daimin
'''
from django.db import models
from django.contrib import admin

class Diary(models.Model):
    """日记
    """
    title        = models.CharField(max_length = 150)
    content      = models.TextField()
    createtime   = models.DateTimeField()
    updatetime   = models.DateTimeField()
    weather      = models.CharField(max_length = 20)
    up_img       = models.URLField(max_length = 240)
    up_img_thumb = models.URLField(max_length = 240)
    author       = models.CharField(max_length = 40)
    type         = models.IntegerField(max_length = 4)
    
class User(models.Model):
    """用户
    """
    email    = models.EmailField(max_length = 80)
    password = models.CharField(max_length = 20)
    nickname = models.CharField(max_length = 40)
    reg_date = models.CharField(max_length = 40)

    

admin.site.register(Diary)
admin.site.register(User)