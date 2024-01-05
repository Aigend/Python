# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:48
# @File:urls.py
from django.urls import path

from sensor.views import SensorView

urlpatterns = [
    path('allinfo/set', SensorView.as_view()),
    # 报警上下限的值是固定的，需要通过转负值触发
    # path('alarminfo/set', sensor_views.sensor_alarm_data),
    path('kill_process/set', SensorView.as_view()),
]
