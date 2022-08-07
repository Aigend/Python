# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : mysite
# @File    : urls.py
# @Date    : 2022/07/30:12:34
# @Author  : jinwenlong@oppo.com
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', admin.site.urls),
]