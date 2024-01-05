# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 9:34
# @File:views.py
import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from utils.constant import PROJECT_DIR


def show_front_view(request):
    return render(request, 'index.html', {})


def download_log(request):
    path = os.path.join(PROJECT_DIR, "logs", "all.log")
    if not os.path.exists(path):
        return JsonResponse({"error": "all.log not exist"})
    file = open(path, 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="all.log"'
    return response


def show_info(request):
    path = os.getcwd()
    return JsonResponse({'path': path})


def show(request):
    return render(request, 'index.html', {})


def bad_request(request, exception, template_name='errors/page_400.html'):
    return render(request, template_name)


def permission_denied(request, exception, template_name='errors/page_403.html'):
    return render(request, template_name)


def page_not_found(request, exception, template_name='errors/page_404.html'):
    return render(request, template_name)


def server_error(request, exception, template_name='errors/page_500.html'):
    return render(request, template_name)
