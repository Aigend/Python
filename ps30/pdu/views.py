# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/2/1 9:24
# @File: views.py
import json
import multiprocessing
import time
from multiprocessing import Queue

import psutil
from django.http import JsonResponse
from django.views import View

from pdu.pdu_mqtt import start_mqtt_send_process
from utils.log import log
from utils.tools import deal_recv_data


class PduView(View):

    pdu_rep_json = {}
    pdu_start_server_flag = False
    pdu_proc = ""
    pdu_q = Queue()
    data = {
        'result_code': '0',
        'message': "OK"
    }

    def get(self, request):
        if isinstance(PduView.pdu_proc, multiprocessing.Process) and PduView.pdu_proc.is_alive():
            psutil.Process(PduView.pdu_proc.pid).terminate()
            psutil.Process(PduView.pdu_proc.pid).wait()
            PduView.pdu_proc = ""
            PduView.pdu_rep_json = {}
            PduView.pdu_start_server_flag = False
            log.info("<PDU>:terminate pdu subprocess success")
            time.sleep(5)
        PduView.data['detail'] = 'terminate pdu subprocess success'
        return JsonResponse(PduView.data)

    def post(self, request):
        body = json.loads(request.body)
        rec = deal_recv_data(body, {})
        PduView.pdu_rep_json.update(rec)
        if not PduView.pdu_start_server_flag:
            PduView.pdu_proc = multiprocessing.Process(target=start_mqtt_send_process, args=(PduView.pdu_q, ))
            PduView.pdu_proc.daemon = True
            PduView.pdu_proc.start()
            log.info(f"<PDU>:create PDU mqtt client back process {PduView.pdu_proc.pid} success")
            PduView.pdu_start_server_flag = True
        PduView.pdu_q.put(PduView.pdu_rep_json)
        log.info("<PDU>:update PDU data success...")
        time.sleep(2)
        PduView.data['detail'] = PduView.pdu_rep_json
        return JsonResponse(PduView.data)



