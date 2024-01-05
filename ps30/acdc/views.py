# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:47
# @File:views.py
import json
import multiprocessing
import re
import time
from multiprocessing import Queue

import psutil
from django.http import JsonResponse
from django.views import View

from acdc.acdc_data import acdc_key_to_variable
from acdc.acdc_msg import AcdcMsg
from acdc.acdc_process import run, analyze
from utils.constant import ACDC_CAN_NODE
from utils.log import log


class AcdcView(View):
    acdc_data_info = {}  # 保存发送的key值
    acdc_msg_info = {}  # 保存各支路要发送的数据
    acdc_child_pro = ""
    acdc_data_pro = ""
    ac_q = Queue()
    pt_q = Queue()

    def get(self, request):
        data = {
            "result_code": "0",
            "message": "OK",
        }
        info = request.GET.get('kill', "")
        if re.match('acdc\d+', info):
            node = int(re.search("acdc(\d+)", info).group(1))  # 0-29
            addr = 0x20 + node
            if addr in AcdcView.acdc_msg_info:
                AcdcView.acdc_msg_info.pop(addr)
                AcdcView.ac_q.put(AcdcView.acdc_msg_info)
        elif re.match('all', info):
            AcdcView.acdc_msg_info = {}
            AcdcView.ac_q.put(AcdcView.acdc_msg_info)
            # if isinstance(AcdcView.acdc_child_pro, multiprocessing.Process) and AcdcView.acdc_child_pro.is_alive():
            #     log.info(f"<ACDC>:recv process pid {AcdcView.acdc_child_pro.pid} kill start")
            #     AcdcView.acdc_child_pro.terminate()
            #     AcdcView.acdc_child_pro.join(timeout=10)
            #     AcdcView.acdc_data_info.clear()
            # if isinstance(AcdcView.acdc_data_pro, multiprocessing.Process) and AcdcView.acdc_data_pro.is_alive():
            #     log.info(f"<ACDC>:analyze process pid {AcdcView.acdc_data_pro.pid} kill start")
            #     AcdcView.acdc_data_pro.terminate()
            #     AcdcView.acdc_data_pro.join(timeout=10)
            time.sleep(1)
        elif re.match('module\d+', info):
            module = int(re.search("module(\d+)", info).group(1))  # 0-9
            start = module * 3
            for i in range(3):
                addr = 0x20 + start + i
                if addr in AcdcView.acdc_msg_info:
                    log.info(f"<ACDC>:remove module{module} acdc{start + i} data")
                    AcdcView.acdc_msg_info.pop(addr)
                    AcdcView.ac_q.put(AcdcView.acdc_msg_info)
            # AcdcView.ac_q.put(AcdcView.acdc_msg_info)
        else:
            log.error("<ACDC>:kill acdc_child_pro process not exists ")
            data["result_code"] = "2"
            data["message"] = "illegal request"
        log.info(f"<ACDC>:kill {info}")
        return JsonResponse(data)

    def post(self, request, typ):
        recv_json = json.loads(request.body)
        node = 0
        for branch, branch_json in recv_json.items():
            tmp = deal_acdc_data(branch_json, {})
            node = int(re.search("acdc(\d+)", branch).group(1))  # 0-29
            data = tmp if typ == "front-info" else acdc_key_to_variable(node, tmp)
            if not AcdcView.acdc_data_info.get(node):
                AcdcView.acdc_data_info[node] = {}
            AcdcView.acdc_data_info[node].update(data)
            deal_acdc_data_request(node)
        log.info(f"<ACDC>:update acdc{node} data success")
        return JsonResponse({"result_code": "0", "message": "OK", "data": AcdcView.acdc_data_info.get(node)})


def deal_acdc_data(rec_json, glob_json):
    """

    :param rec_json:
    :param glob_json:
    :return:
    """
    if isinstance(rec_json, dict):
        for name, val in rec_json.items():
            if isinstance(val, dict):
                deal_acdc_data(val, glob_json)
            else:
                glob_json[name] = val
    return glob_json


def deal_acdc_data_request(branch):
    """

    :param branch:
    :param branch_json:
    :return:
    """
    acdc_msg = AcdcMsg(AcdcView.acdc_data_info[branch], branch)
    addr = 0x20 + branch
    AcdcView.acdc_msg_info.update({addr: acdc_msg})
    AcdcView.ac_q.put(AcdcView.acdc_msg_info)
    if isinstance(AcdcView.acdc_child_pro, str) or (isinstance(AcdcView.acdc_child_pro, multiprocessing.Process)
                                                    and not AcdcView.acdc_child_pro.is_alive()):
        AcdcView.acdc_child_pro = multiprocessing.Process(target=run,
                                                          args=(AcdcView.ac_q, AcdcView.pt_q, ACDC_CAN_NODE), )
        AcdcView.acdc_child_pro.daemon = True
        AcdcView.acdc_child_pro.start()
        psutil.Process(AcdcView.acdc_child_pro.pid).cpu_affinity([1])
        log.info(f"<ACDC>:can:{ACDC_CAN_NODE} ACDC can子进程pid:{AcdcView.acdc_child_pro.pid} 第一次创建{branch}")
        #time.sleep(5)
        time.sleep(2)

    if isinstance(AcdcView.acdc_data_pro, str) or (isinstance(AcdcView.acdc_data_pro, multiprocessing.Process)
                                                   and not AcdcView.acdc_data_pro.is_alive()):
        AcdcView.acdc_data_pro = multiprocessing.Process(target=analyze,
                                                         args=(AcdcView.ac_q, AcdcView.pt_q), )
        AcdcView.acdc_data_pro.daemon = True
        AcdcView.acdc_data_pro.start()
        psutil.Process(AcdcView.acdc_data_pro.pid).cpu_affinity([1])
        log.info(f"<ACDC>:创建{branch} ACDC 处理数据子进程pid:{AcdcView.acdc_data_pro.pid}")
        #time.sleep(5)
        time.sleep(2)
