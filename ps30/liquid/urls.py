# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:48
# @File:urls.py
from django.urls import path

from liquid.views import LiquidView

urlpatterns = [
    path('allinfo/set', LiquidView.as_view()),
    path('kill_process/set', LiquidView.as_view()),
    # re_path('(?P<typ>allinfo)/set', LiquidView.as_view()),
    # re_path('(?P<typ>alarminfo)/set', LiquidView.as_view()),
    # path('test/set', LiquidView.as_view())
]
