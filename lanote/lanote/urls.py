#!/usr/bin/env python
# -*- coding:UTF-8 -*-   
#encoding=utf-8
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
        
    url( r'^js/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': './js/' }
    ),
 
    url( r'^css/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': './css/' }
    ),
 
    url( r'^images/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': './images/' }
    ),
    
    url(r'^$', archive),
)
