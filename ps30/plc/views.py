# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:47
# @File:views.py
import json
import psutil
import multiprocessing
import time
from multiprocessing import Queue, Process

from django.http import JsonResponse
from django.views import View

from plc.plc_key import plc_key_data_init
from plc.plc_rep_msg import generate_PLC_STATUS_REP_STRUCT
from plc.plc_utils import start_plc_server_receive
from utils.constant import PLC_NODE
from utils.log import log
from utils.tools import check_ip_address_available


class PlcView(View):

    plc_q = Queue()
    plc_p = ""
    plc_pid = ""

    def get(self, request):
        data = {
            'result_code': '0',
            'message': 'OK',
        }
        if isinstance(PlcView.plc_p, multiprocessing.Process) and PlcView.plc_p.is_alive():
            log.info(f"<PLC>:process pid {PlcView.plc_pid} kill start")
            psutil.Process(PlcView.plc_p.pid).terminate()
            time.sleep(5)
            data['detail'] = f'plc process pid {PlcView.plc_pid} kill success'
        return JsonResponse(data)

    def post(self, request):
        res = {
            'result_code': '0',
            'message': "OK"
        }
        log.info("<PLC>:receive plc post req")
        body = json.loads(request.body)
        reply_json, data = plc_key_data_init(body)
        res["data"] = data
        reply_struct = generate_PLC_STATUS_REP_STRUCT(reply_json)
        while not PlcView.plc_q.empty():
            PlcView.plc_q.get()
        PlcView.plc_q.put(reply_struct)
        #time.sleep(1)
        if not PlcView.plc_p or not (isinstance(PlcView.plc_p, multiprocessing.Process) and PlcView.plc_p.is_alive()):
            if not check_ip_address_available(PLC_NODE['ip'], PLC_NODE['port']):
                log.error(f'<PLC>:hard environment happen error, ip{PLC_NODE["ip"]} can not connect')
                res['result_code'] = '2'
                res['message'] = f'<PLC>:hard environment happen error, ip{PLC_NODE["ip"]} can not connect'
                return JsonResponse(res)
            PlcView.plc_p = Process(target=start_plc_server_receive, args=(PlcView.plc_q, ))
            PlcView.plc_p.daemon = True
            PlcView.plc_p.start()
            PlcView.plc_pid = PlcView.plc_p.pid
            log.info(f"<PLC>:plc child process create success, pid:{PlcView.plc_p.pid}")
            #time.sleep(4)
        return JsonResponse(res)

