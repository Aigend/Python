# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : mysite
# @File    : views.py
# @Date    : 2022/07/30:10:37
# @Author  : jinwenlong@oppo.com
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.views import View


class IndexView(View):

    def get(self, request):
        return HttpResponse('get...')

    def post(self, request):
        return HttpResponse('post...')


def index(request):
    return HttpResponse('index...')


def find1(request, std):
    print(type(std))
    return HttpResponse('find1...')


def find2(request, std, name):
    print(type(std))
    print(type(name))
    return HttpResponse('find2...')


def slugStr(request, slugStr):
    return HttpResponse('<h1>{}</h1>'.format(slugStr))
    # 浏览器输入：http://127.0.0.1:8000/swe-123;lkl-=，页面则显示对应的swe-123;lkl-=


def uu(request, uu):
    return HttpResponse('<h1>{}</h1>'.format(uu))
    # 浏览器输入：http://127.0.0.1:8000/uuid码，页面则显示对应的uuid码。如：5acba24c-abdd-4ee1-b991-a90d3406d2a8


def home(request, home):
    return HttpResponse('<h1>{}</h1>'.format(home))
    # 浏览器输入：http://127.0.0.1:8000/html/index.html，页面则显示对应的html/index.html


def page_not_found(request, exception):
    return render_to_response('404.html')


def page_error(request):
    return render(request, '500.html')