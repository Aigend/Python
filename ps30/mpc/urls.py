"""
@Project: ps30
@File: urls.py
@Author: wenlong.jin
@Time: 2023/11/14 10:51
@version: 1.0.0
@Description:
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path

from mpc.views import MpcView

urlpatterns = [
    path('allinfo/set', MpcView.as_view()),
]