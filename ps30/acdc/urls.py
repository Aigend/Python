# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:48
# @File:urls.py
from django.urls import path

from acdc.views import AcdcView

urlpatterns = [
    path('kill_process/set', AcdcView.as_view()),
    path('<typ>/set', AcdcView.as_view()),
]