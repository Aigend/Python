# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:48
# @File:urls.py
from django.urls import path

from oss_welkin import views as kafka_views

urlpatterns = [
    path('realtime/set', kafka_views.rec_realtime_data),
    path('alarm/set', kafka_views.rec_alarm_data),
    path('event/set', kafka_views.rec_event_data),
]