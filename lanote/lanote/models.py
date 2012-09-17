'''
Created on 2012-9-18

@author: daimin
'''
from django.db import models
from django.contrib import admin

class BlogPost(models.Model):
    title     = models.CharField(max_length=150)
    body      = models.TextField()
    timestamp = models.DateTimeField()

admin.site.register(BlogPost)