# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:rosa.xiao
# @Time:2023/12/1 20:48
# @File:urls.py
from django.urls import path

from oss_control import views as oss_control_views

urlpatterns = [
    path('generateVirtualKey/set', oss_control_views.rec_genereateVirtualKey_data),
    path('remote_control/set', oss_control_views.rec_remote_control_data),
]
