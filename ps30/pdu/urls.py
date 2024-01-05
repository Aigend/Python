# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/2/1 9:24
# @File: urls.py
from django.urls import path

from pdu.views import PduView

urlpatterns = [
    path('kill_process/set', PduView.as_view()),
    path('allinfo/set', PduView.as_view()),
]