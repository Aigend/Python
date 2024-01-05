#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: wenlong.jin
@File: middleware.py.py
@Project: ps30
@Time: 2023/7/3 15:21
"""
import time


def timeit_middleware(get_response):
    def middleware(request):
        start = time.time()
        response = get_response(request)
        end = time.time()
        print("请求花费时间: {}秒".format(end - start))
        return response

    return middleware


from django.shortcuts import redirect
from django.conf import settings


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = settings.LOGIN_URL
        # 开放白名单，比如['/login/', '/admin/']
        self.open_urls = [self.login_url] + getattr(settings, 'OPEN_URLS', [])

    def __call__(self, request):
        if not request.user.is_authenticated and request.path_info not in self.open_urls:
            print("@@:"+ self.login_url + '?next=' + request.get_full_path())
            return redirect(self.login_url + '?next=' + request.get_full_path())
        response = self.get_response(request)
        return response
