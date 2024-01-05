# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:48
# @File:urls.py
from django.urls import path

# from aec.views import AecView, McsView

from aec.views import AecView

urlpatterns = [
    path('kill_process/set', AecView.as_view()),
    path('allinfo/set', AecView.as_view()),
    path('alarminfo/set', AecView.as_view()),
]
