#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: wenlong.jin
@File: urls.py
@Project: ps30
@Time: 2023/6/30 16:07
"""
from django.urls import path, re_path
from mysite import views
from django.urls import reverse

# URLconf的命名空间
# 实中很显然会有5个、10个、更多的app同时存在一个项目中。Django是如何区分这些app之间的URL name

# namespace
app_name = 'tasks'

urlpatterns = [
    # Create a task
    path('create/', views.task_create, name='task_create'),

    # Retrieve task list
    path('', views.task_list, name='task_list'),

    # Retrieve single task object
    re_path(r'^(?P<pk>\d+)/$', views.task_detail, name='task_detail'),

    # Update a task
    re_path(r'^(?P<pk>\d+)/update/$', views.task_update, name='task_update'),

    # Delete a task
    re_path(r'^(?P<pk>\d+)/delete/$', views.task_delete, name='task_delete'),

    path("signal/", views.hello_my_signal, name='hello_my_signal'),
]