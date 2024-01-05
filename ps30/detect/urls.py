#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/15 11:33
# @Author  : wenlong.jin@nio.com
# @File    : urls.py
# @Software: ps20
from django.urls import path

from detect.views import DetectView

urlpatterns = [
    path('allinfo/set', DetectView.as_view()),
    path('kill_process/set', DetectView.as_view()),
]