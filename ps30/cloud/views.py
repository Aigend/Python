# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/4/4 10:17
# @File: views.py
from django.http import JsonResponse
from django.views import View


class CloudView(View):

    def get(self, request):
        return JsonResponse({'result_code': "0", 'message': "Cloud 功能待开发", })

    def post(self, request):
        return JsonResponse({'result_code': "0", 'message': "Cloud 功能待开发", })