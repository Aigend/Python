#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: wenlong.jin
@File: urls.py
@Project: ps30
@Time: 2023/7/3 09:59
"""
from django.urls import path
from icc.views import IccView

urlpatterns = [
    path('allinfo/set', IccView.as_view()),
    path('alarminfo/set', IccView.as_view()),
]