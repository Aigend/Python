# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/3/29 13:02
# @File: urls.py
from django.urls import path, re_path

from sct.views import SctView

urlpatterns = [
    # path('kill_process/set', SctView.as_view()),
    path('allinfo/set', SctView.as_view()),
    path('alarminfo/set', SctView.as_view()),
]