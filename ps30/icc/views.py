#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: wenlong.jin
@File: views.py
@Project: ps30
@Time: 2023/7/3 09:59
"""
import json
import multiprocessing
import re
import time

from django.http import JsonResponse
from django.views import View

from icc import icc_process_pool, icc_q
from icc.icc_mqtt import start_icc_mqtt_process
from utils.log import log


class IccView(View):

    def post(self, request):
        data = {
            'result_code': '0',
            'message': "OK"
        }
        body = json.loads(request.body)
        node = list(body.keys())[0]
        req = body.get(node, {})
        icc = int(re.match(r"icc(\d+)", node).group(1))
        if node not in icc_process_pool or not icc_process_pool[node].is_alive():
            process = multiprocessing.Process(target=start_icc_mqtt_process,
                                              args=(icc_q[node], icc))
            process.daemon = True
            process.start()
            icc_process_pool[node] = process
            time.sleep(2)
            log.warning(f"<ICC>:创建{node} 子进程pid:{str(process.pid)} success")
        return JsonResponse(data)
