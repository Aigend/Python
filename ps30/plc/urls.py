# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:48
# @File:urls.py
from django.urls import path

from plc.views import PlcView

urlpatterns = [
    path('allinfo/set', PlcView.as_view()),
    path('alarminfo/set', PlcView.as_view()),
    path('kill_process/set', PlcView.as_view()),
]