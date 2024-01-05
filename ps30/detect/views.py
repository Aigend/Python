#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/15 11:33
# @Author  : wenlong.jin@nio.com
# @File    : views.py
# @Software: ps20
import json
from django.http import JsonResponse
from django.views import View

from detect.detect_msg import DetectMsg
from utils.constant import SERIAL_NODE
from utils.log import log


class DetectView(View):

    msg = DetectMsg()
    detect_param = {}

    def deal_detect_data(self, rec_json, detect_param):
        if isinstance(rec_json, dict):
            for name, val in rec_json.items():
                if isinstance(val, dict):
                    self.deal_detect_data(val, detect_param)
                elif isinstance(val, int) or (isinstance(val, str) and val.isnumeric()):
                    detect_param[name] = val
                else:
                    log.info("<Detect>:post data type not support")

    def get(self, request):
        data = {
            'result_code': '0',
            'message': 'OK',
        }
        if DetectView.msg.start_server_flag:
            log.info("<Detect>:pid threading close ...")
            DetectView.msg.start_server_flag = False
            DetectView.detect_param.clear()
            SERIAL_NODE.pop("detect")
            DetectView.msg.stop_detect_server()
        return JsonResponse(data)

    def post(self, request):
        res = {
            'result_code': '0',
            'message': 'OK',
        }
        param = json.loads(request.body)
        self.deal_detect_data(param, DetectView.detect_param)
        if not DetectView.msg.start_server_flag:
            SERIAL_NODE["detect"] = "/dev/ttyUSB0"  # 调试使用
            if SERIAL_NODE.get("detect"):
                DetectView.msg.port = SERIAL_NODE.get("detect")
                log.info(f"<Detect>:detect port is {DetectView.msg.port}")
                DetectView.msg.start_detect_server()
                DetectView.msg.start_server_flag = True
                log.info("<Detect>:pid threading create success")
            else:
                log.error(f'<Detect>:串口不可用, 请确认硬件环境是否配置异常:{SERIAL_NODE}')
                return JsonResponse(
                    {'result_code': "2", 'message': f'<Detect>:串口不可用, 请确认硬件环境是否配置异常', })
        DetectView.msg.init_data(DetectView.detect_param)
        log.info("<Detect>:post request, send real time data success")
        return JsonResponse(res)