# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/3/29 13:02
# @File: views.py
import json
import multiprocessing
import re
import time

from django.http import JsonResponse
from django.views import View

from sct import sct_q, sct_process_pool
from sct.sct_data import change_sct_key_to_var
from sct.sct_mqtt import start_sct_mqtt_process
from sct.sct_msg import SctMsg
from utils.log import log


class SctView(View):

    sct_json = {}

    def post(self, request):
        data = {
            'result_code': '0',
            'message': "OK"
        }
        body = json.loads(request.body)
        for node, req in body.items():
            sct = int(re.match("sct(\d+)", node).group(1))
            tmp = deal_sct_recv_data(req, {})
            var = change_sct_key_to_var(sct, tmp)
            if not SctView.sct_json.get(node):
                SctView.sct_json[node] = {}
            update_sct_node_json(SctView.sct_json[node], var)
            data["data"] = SctView.sct_json[node]
            obj = SctMsg(SctView.sct_json[node], sct)
            sct_q[node].put({"all": obj.sct_all_serialize, "status": obj.sct_status_serialize})
            if node not in sct_process_pool or not sct_process_pool[node].is_alive():
                process = multiprocessing.Process(target=start_sct_mqtt_process,
                                                  args=(sct_q[node], sct))
                process.daemon = True
                process.start()
                sct_process_pool[node] = process
                time.sleep(2)
                log.info(f"<SCT>:创建{node} 子进程pid:{str(process.pid)} success")
        return JsonResponse(data)


def deal_sct_recv_data(data, rec):
    """

    :param data:
    :param rec:
    :return:
    """
    if isinstance(data, dict):
        for name, val in data.items():
            if isinstance(val, dict):
                deal_sct_recv_data(val, rec)
            else:
                rec[name] = val
    return rec


def update_sct_node_json(res, req):
    """

    :param res:
    :param req:
    :return:
    """
    for info, values in req.items():
        if info not in res:
            res[info] = {}
        res[info].update(values)



