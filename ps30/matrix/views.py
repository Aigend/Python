# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:47
# @File:views.py
import json

import requests
from django.http import JsonResponse
from django.views import View

from utils.log import log


class MatrixView(View):

    def post(self, request):
        data = {
            'result_code': '0',
            'message': "OK",
        }
        body = json.loads(request.body)
        log.info(f"<Matrix>:Post body data:{body}")
        data['data'] = body
        url = "http://192.168.1.10:8091/update/matrix/data"
        request_headers = {
            'Content-Type': 'application/json'
        }
        res = requests.post(url=url, data=json.dumps(body), headers=request_headers)
        data['matrix_request_detail'] = res.status_code
        return JsonResponse(data)

