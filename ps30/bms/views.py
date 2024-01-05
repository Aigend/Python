# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:47
# @File:views.py
import json
import multiprocessing
import re
import sys
import time
from multiprocessing import Queue

import psutil
from django.http import JsonResponse
from django.views import View

from bms import bms_q, bms_process_pool
from bms.bms_data import BmsData
from bms.bms_process import start_can_send_process
from bms.bms_utils import bms_convert_key_to_var
from utils.constant import BMS_CAN_NODE
from utils.constant import CAN_INSTANCE
from utils.log import log
from utils.tools import deal_recv_data


class BmsView(View):

    bms_data_info = {}  # 保存发送的key值

    def get(self, request):
        data = {
            'datatime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'result_code': '0',
            'message': 'OK',
        }
        info = request.GET.get('kill', "")
        if re.match('bms\d+', info):
            branch = re.match('bms\d+', info).group()
            if bms_process_pool.get(branch, "") and bms_process_pool.get(branch).is_alive():
                log.info(f"<BMS>:{branch} process pid {bms_process_pool.get(branch).pid} kill start")
                bms_process_pool.get(branch).terminate()
                bms_process_pool.get(branch).join(timeout=10)
                bms_q.pop(branch)
                bms_process_pool.pop(branch)
                BmsView.bms_data_info.pop(branch)
                for can_name, brn_name in list(CAN_INSTANCE.items()):
                    if brn_name == branch:
                        CAN_INSTANCE.pop(can_name)
        elif re.match('all', info):
            for brn, procs in list(bms_process_pool.items()):
                log.info(f"<BMS>:{brn} process pid {procs.pid} kill start")
                procs.terminate()
                procs.join(timeout=10)
                bms_q.pop(brn)
                bms_process_pool.pop(brn)
                BmsView.bms_data_info.pop(brn)
                for can_name, brn_name in list(CAN_INSTANCE.items()):
                    if brn_name == brn:
                        CAN_INSTANCE.pop(can_name)
        else:
            data['result_code'] = '2'
            data['message'] = 'illegal request, kill process parameter not correct'
        return JsonResponse(data)

    def post(self, request, typ):
        recv_json = json.loads(request.body)
        branch = list(recv_json.keys())[0]
        branch_json = recv_json.get(branch)
        can_node = BMS_CAN_NODE.get(branch)
        if not can_node:
            log.error(f"<BMS>:<{typ}>未在django配置文件中找到{branch}所使用的can口信息")
            return JsonResponse(
                {'result_code': "3", 'message': f'<BMS>:未在django配置文件中找到{branch}所使用的can口信息', })
        if not BmsView.bms_data_info.get(branch):
            BmsView.bms_data_info[branch] = {}
        key_temp_json = deal_recv_data(branch_json, {})
        var_temp_json = key_temp_json if typ == "front-info" else bms_convert_key_to_var(branch, key_temp_json)
        BmsView.bms_data_info[branch].update(var_temp_json)
        res = deal_bms_data_request(BmsView.bms_data_info[branch], branch, can_node, typ)
        if isinstance(res, JsonResponse):
            return res
        res = {
            "datatime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'result_code': "0",
            'message': 'OK',
            "data": BmsView.bms_data_info[branch]
        }
        return JsonResponse(res)


def deal_bms_data_request(branch_json, branch, can_node, typ):
    """

    :param branch_json:
    :param branch:
    :param can_node:
    :param typ:
    :return:
    """
    # 检查数据的有效性，避免只发报警数据，基本数据都不存在的情景
    check_vars = ["battery_pack_id",
                  "gb_battery_pack_id",
                  "bms_software_ver",
                  "bms_hardware_ver",
                  "bms_protocal_version", ]
    for var in check_vars:
        if var not in branch_json:
            log.error(f"<BMS>:branch {branch} data not contain battery basic data, return error")
            return JsonResponse({'result_code': "3",
                                 'message': f'<BMS>:branch {branch} data not contain battery basic data, return error', })
    try:
        bms_instant = BmsData(branch_json)
        bms_instant.bms_data_init()
    except ValueError:
        _, exc_value, _ = sys.exc_info()
        log.error(f"<BMS>:<{typ}>Post请求实时信息数据初始化异常:{str(exc_value)}")
        return JsonResponse({'result_code': "3",
                             'message': f'<BMS>:{branch}数据初始化异常，请排查报错的数据类型, {exc_value}', })
    for brn, _ in list(bms_process_pool.items()):
        # log.debug(f"{brn} process alive status:{bms_process_pool[brn].is_alive()}")
        if brn == branch and bms_process_pool[brn].is_alive():
            bms_q[brn].put(bms_instant.board)
            #time.sleep(2)
            return
        elif brn == branch and not bms_process_pool[brn].is_alive():
            bms_process_pool.pop(brn)
            bms_q.pop(brn)
            for can_name, brn_name in list(CAN_INSTANCE.items()):
                if brn_name == brn:
                    CAN_INSTANCE.pop(can_name)
    else:
        if not CAN_INSTANCE.get(can_node):
            CAN_INSTANCE[can_node] = branch
            bms_q[branch] = Queue()
            process = multiprocessing.Process(target=start_can_send_process,
                                              args=(branch, can_node,
                                                    bms_instant.board,
                                                    bms_q[branch]))
            process.daemon = True
            process.start()
            psutil.Process(process.pid).cpu_affinity([0])
            bms_process_pool[branch] = process
            #time.sleep(15)
            time.sleep(1)
            log.info(f"<BMS>:<{typ}>创建{branch} can:{can_node} BMS子进程pid:{str(process.pid)}")
            return
        else:
            branch_can = CAN_INSTANCE[can_node]
            bms_q[branch_can].put(bms_instant.board)
            return
