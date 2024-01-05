# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/1/12 16:50
# @File: urls.py
from django.urls import path

from meter.views import MeterView

urlpatterns = [
    path('allinfo/set', MeterView.as_view()),
    path('kill_process/set', MeterView.as_view()),
]
