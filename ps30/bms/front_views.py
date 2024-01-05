# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2022/11/20 14:12
# @File: front_views.py
import json
import multiprocessing
import os
import re
import sys
import time
from multiprocessing import Queue

import psutil
from django.http import JsonResponse
from django.views import View

from bms import bms_q, bms_process_pool
from bms.bms_data import BmsData
from bms.bms_process import front_start_can_send_process
from utils.log import log as logger


class FrontBmsView(View):
    bms_update_data = {}

    def get(self, request):
        data = {
            'result_code': '0',
            'message': 'OK',
        }
        info = request.GET.get('kill', "")
        if re.match('can\d+', info):
            can_node = re.match('can\d+', info).group()
            if can_node in bms_process_pool and bms_process_pool[can_node].is_alive():
                logger.info(f"<BMS>:{can_node} process pid {bms_process_pool[can_node].pid} kill start")
                proc = psutil.Process(bms_process_pool[can_node].pid)
                proc.kill()
                bms_q.pop(can_node)
                bms_process_pool.pop(can_node)
                FrontBmsView.bms_update_data.pop(can_node)
                time.sleep(3)
        elif re.match('all', info):
            for can_node, procs in list(bms_process_pool.items()):
                logger.info(f"<BMS>:{can_node} process pid {procs.pid} kill start")
                proc = psutil.Process(bms_process_pool[can_node].pid)
                proc.kill()
                bms_q.pop(can_node)
                bms_process_pool.pop(can_node)
                FrontBmsView.bms_update_data.pop(can_node)
                time.sleep(3)
        else:
            data["data"] = FrontBmsView.bms_update_data
        return JsonResponse(data)

    def post(self, request, typ):
        recv_json = json.loads(request.body)
        logger.info(f"<BMS> <rec_update_bms_basic_info>:type:{typ} Post data:{recv_json}")
        brn_node = recv_json.get('branch_info', {}).get('branch')
        can_node = recv_json.get('branch_info', {}).get('can')
        if not can_node:
            logger.error(f"<BMS>:支路{brn_node} Post请求中未携带{brn_node}所使用的can口信息")
            return JsonResponse(
                {'result_code': "3",
                 'message': f'<Warning>:支路{brn_node} Post请求中未携带{brn_node}所使用的can口信息', })
        can_node = re.search(".*?\d+", can_node).group()
        res = os.popen(r"ls /sys/class/net | grep can")  # 检查can要在设备列表中才继续执行
        if can_node not in set(node.strip() for node in res.readlines()):
            logger.error(f"<BMS>:current env, {can_node} not in device can list")
            return JsonResponse(
                {'result_code': "3", 'message': f'<Warning>:{can_node} not in device can list', })
        deal_front_bms_data(can_node, typ, recv_json)
        res = deal_front_bms_data_request(brn_node, can_node, typ)
        if isinstance(res, JsonResponse):
            return res
        logger.info(f"<BMS>:<{typ}>post request, send {typ} data success")
        return JsonResponse({'result_code': "0", 'message': 'OK', })


def deal_front_bms_data_request(brn_node, can_node, typ):
    """

    :param brn_node:
    :param can_node:
    :param typ:
    :return:
    """
    check_vars = ["battery_pack_id",
                  "gb_battery_pack_id",
                  "bms_software_ver",
                  "bms_hardware_ver",
                  "bms_protocal_version", ]
    for var in check_vars:
        if var not in FrontBmsView.bms_update_data.get(can_node):
            logger.error(f"<BMS>:{can_node} data not contain battery basic data, return error")
            return JsonResponse({'result_code': "3",
                                 'message': f'Warning:{can_node} send data not contain battery basic data, error!'})
    try:
        bms_instant = BmsData(FrontBmsView.bms_update_data.get(can_node))
        bms_instant.bms_data_init()
    except ValueError:
        _, exc_value, _ = sys.exc_info()
        logger.error(f"<BMS>:<{typ}>Post请求实时信息数据初始化异常:{str(exc_value)}")
        return JsonResponse({'result_code': "3", 'message': f'<Warning>:{can_node} data convert happen error!', })
    if typ in ["all", "basic"] or can_node not in bms_process_pool or not bms_process_pool[can_node].is_alive():
        bms_q[can_node] = Queue()
        alive = False
        if can_node in bms_process_pool and bms_process_pool[can_node].is_alive():
            alive = True
        process = multiprocessing.Process(target=front_start_can_send_process,
                                          args=(brn_node, can_node,
                                                bms_instant.board,
                                                bms_process_pool, bms_q[can_node], typ, alive))
        process.daemon = True
        process.start()
        bms_process_pool[can_node] = process
        logger.info(f"<BMS>:<{typ}>{can_node}--->>>{brn_node} BMS pid:{process.pid}")
    bms_q[can_node].put(bms_instant.board)
    time.sleep(1)
    return


def deal_front_bms_data(can_node, typ, recv_json):
    """

    :param can_node:
    :param typ:
    :param recv_json:
    :return:
    """
    if can_node not in FrontBmsView.bms_update_data:
        FrontBmsView.bms_update_data[can_node] = {}
    FrontBmsView.bms_update_data[can_node].update(recv_json.get('branch_info'))
    if typ == "basic":
        FrontBmsView.bms_update_data[can_node].update(recv_json.get('bms_basic_info', {}))
    elif typ == "realtime":
        FrontBmsView.bms_update_data[can_node].update(recv_json.get('bms_realtime_info', {}))
    elif typ == "alarm":
        FrontBmsView.bms_update_data[can_node].update(recv_json.get('bms_alarm_info', {}))
    elif typ == "status":
        FrontBmsView.bms_update_data[can_node].update(recv_json.get('bms_status_info', {}))
    elif typ == "config":
        FrontBmsView.bms_update_data[can_node].update(recv_json.get('bms_config_info', {}))
    elif typ == "volt":
        FrontBmsView.bms_update_data[can_node].update(recv_json.get('bms_volt_info', {}))
    elif typ == "temp":
        FrontBmsView.bms_update_data[can_node].update(recv_json.get('bms_temp_info', {}))
    elif typ == "all":
        FrontBmsView.bms_update_data[can_node].update(recv_json.get('bms_basic_info', {}))
        FrontBmsView.bms_update_data[can_node].update(recv_json.get('bms_config_info', {}))
        FrontBmsView.bms_update_data[can_node].update(recv_json.get('bms_status_info', {}))
        FrontBmsView.bms_update_data[can_node].update(recv_json.get('bms_realtime_info', {}))
        FrontBmsView.bms_update_data[can_node].update(recv_json.get('bms_alarm_info', {}))
        FrontBmsView.bms_update_data[can_node].update(recv_json.get('bms_volt_info', {}))
        FrontBmsView.bms_update_data[can_node].update(recv_json.get('bms_temp_info', {}))
