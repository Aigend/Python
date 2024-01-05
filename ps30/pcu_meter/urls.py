# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:48
# @File:urls.py
from django.urls import path

from pcu_meter.views import PcuMeterView

urlpatterns = [
    path('kill_process/set', PcuMeterView.as_view()),
    path('allinfo/set', PcuMeterView.as_view())
    # path('<str:typ>/set', PcuMeterView.as_view())
    # re_path('(?P<typ>allinfo)/set', pcu_meter_views.handle),
    # re_path('(?P<typ>alarminfo)/set', pcu_meter_views.handle),
]
