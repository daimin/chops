#!/usr/bin/env python
# -*- coding:UTF-8 -*-   
#encoding=utf-8
from django.http import HttpResponse
from django.template import loader, Context
from lanote.models import Diary

def archive(request):
    diarys = Diary.objects.all().order_by("-updatetime")
    t = loader.get_template("archive.html")
    c = Context({ 'diarys': diarys })
    return HttpResponse(t.render(c))

def index(request):
    t = loader.get_template("index.html")
    ctx = Context()
    return HttpResponse(t.render(ctx))
    