"""
@Project: ps30
@File: urls.py
@Author: wenlong.jin
@Time: 2023/11/29 10:50
@version: 1.0.0
@Description:
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path

from cdc import views as cdc_views

urlpatterns = [
    path('allinfo/set', cdc_views.rec_realtime_data),
]