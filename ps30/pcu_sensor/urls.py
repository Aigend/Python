# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/1/12 15:40
# @File: urls.py
from django.urls import path

from pcu_sensor.views import PcuSensorView

urlpatterns = [
    path('allinfo/set', PcuSensorView.as_view()),
    path('kill_process/set', PcuSensorView.as_view()),
]