# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:48
# @File:urls.py
from django.urls import path
from bms.views import BmsView
from bms.front_views import FrontBmsView

urlpatterns = [
    # 清理进程
    path('kill_process/set', BmsView.as_view()),
    path('front/kill_process/set', FrontBmsView.as_view()),
    path('info/set/', FrontBmsView.as_view()),
    path('<str:typ>/set', BmsView.as_view()),
    # 下面的用于前端仿真工具使用
    path('<str:typ>', FrontBmsView.as_view()),

]
