"""
@Project: ps30
@File: views.py
@Author: wenlong.jin
@Time: 2023/11/29 10:50
@version: 1.0.0
@Description:
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import multiprocessing
import time
from multiprocessing import Pipe

import psutil
from django.http import JsonResponse
from django.views import View

from cdc.cdc_can import cdc_run
from utils.constant import CDC_CAN_NODE
from utils.log import log


# 有点问题，暂时不需要
class CdcView(View):
    acdc_data_info = {}
    cdc_child_pro = ""
    out_pipe, in_pipe = Pipe()

    def post(self, request):
        if isinstance(CdcView.cdc_child_pro, str) or (isinstance(CdcView.cdc_child_pro, multiprocessing.Process)
                                                      and not CdcView.cdc_child_pro.is_alive()):
            CdcView.cdc_child_pro = multiprocessing.Process(target=cdc_run,
                                                            args=(CdcView.out_pipe, CdcView.in_pipe, CDC_CAN_NODE), )
            CdcView.cdc_child_pro.daemon = True
            CdcView.cdc_child_pro.start()
            psutil.Process(CdcView.cdc_child_pro.pid).cpu_affinity([1])
            log.info(f"<CDC>:can:{CdcView} CDC can子进程pid:{CdcView.cdc_child_pro.pid}")
            time.sleep(5)
        res = ""
        if not CdcView.cdc_q.empty():
            res = CdcView.cdc_q.get()
        return JsonResponse(
            {"result_code": "0", "message": f"Cdc process pid {CdcView.cdc_child_pro.pid}", "data": res})
