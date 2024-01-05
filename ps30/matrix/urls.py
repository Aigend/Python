# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:48
# @File:urls.py
from django.urls import path

from matrix.views import MatrixView

urlpatterns = [
    path('allinfo/set', MatrixView.as_view()),
]