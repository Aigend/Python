# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:47
# @File:views.py
import json
import multiprocessing
import time
from multiprocessing import Queue

import psutil
from django.http import JsonResponse
from django.views import View

from aec.aec_msg import aec_init_back_process
from utils.log import log
from utils.tools import net_is_used


class AecView(View):
    procs = {}
    send_q = Queue()
    receive_q = Queue()
    send_tag = {"hb", "ai-model-version", 'bbsa', 'bsa', 'pip', 'ppp', 'rsdv_pip', 'vip', 'wl', 'rsds', 'wpv'}

    flag = False

    def get(self, request):
        data = {
            'result_code': '0',
            'message': 'OK',
            'data': {}
        }
        # 为了避免报错，需要控制关闭的顺序，不要用字典遍历kill，先关闭send
        send = AecView.procs.get("send")
        if isinstance(send, multiprocessing.Process) and send.is_alive():
            data['data']['send'] = send.pid
            psutil.Process(send.pid).terminate()
        receive = AecView.procs.get("receive")
        if isinstance(receive, multiprocessing.Process) and receive.is_alive():
            data['data']['receive'] = receive.pid
            psutil.Process(receive.pid).terminate()
        log.info(f"<AEC>: kill aec sub process {data['data']}")
        AecView.flag = False
        time.sleep(1)
        return JsonResponse(data)

    def post(self, request):
        receive_q = Queue()
        req = json.loads(request.body)
        log.info(f"<AEC>:Post data:{req}")
        res = {
            'result_code': '0',
            'message': "OK",
        }
        # /kylin/aec/allinfo/set
        if "alarminfo" in request.path:  # 暂时不进行处理
            return JsonResponse(res)
        for info, data in req.items():
            log.info(f'=========={info}==========')
            _k = info.lower()
            log.info(f'=========={_k}==========')
            if _k in AecView.send_tag:
                AecView.send_q.put({_k: data})
        if not AecView.flag and net_is_used(8800):
            res['message'] = 'environment 8800 port is used， aec has started'
            return JsonResponse(res)
        aec_init_back_process(AecView.procs, AecView.receive_q,AecView.send_q)
        
        AecView.flag = True
        res['data'] = req
        log.info(res)
        
        return JsonResponse(res)

