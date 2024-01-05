# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/4/4 10:17
# @File: urls.py
from django.urls import path

from cloud.views import CloudView

urlpatterns = [
    path('operate/set', CloudView.as_view()),
]