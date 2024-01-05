"""
@Project: ps30
@File: views.py
@Author: wenlong.jin
@Time: 2023/11/14 10:52
@version: 1.0.0
@Description:
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import multiprocessing
import time
from multiprocessing import Queue, Process

import psutil
from django.http import JsonResponse
from django.views import View

from mpc.utils import start_mpc_process
from utils.log import log


class MpcView(View):
    mpc_start_server_flag = False
    mpc_proc = ""
    mpc_q = Queue()
    data = {
        'result_code': '0',
        'message': "OK"
    }

    def get(self, request):
        if isinstance(MpcView.mpc_proc, multiprocessing.Process) and MpcView.mpc_proc.is_alive():
            psutil.Process(MpcView.mpc_proc.pid).terminate()
            psutil.Process(MpcView.mpc_proc.pid).wait()
            MpcView.mpc_proc = ""
            MpcView.mpc_start_server_flag = False
            log.info("<MPC>:terminate mpc subprocess success")
            time.sleep(1)
        MpcView.data['message'] = "OK"
        return JsonResponse(MpcView.data)

    def post(self, request):
        """
        模拟MPC，目前只实现停止充电，未实现的功能待补充
        :param request:
        :return:
        """
        body = json.loads(request.body)
        branch = body.get('branch')
        if not branch:
            MpcView.data['message'] = "<MPC>:未设置MPC停止充电的branch信息，无法进行后续操作"
            log.error(MpcView.data['message'])
            return JsonResponse(MpcView.data)
        if not MpcView.mpc_start_server_flag:
            MpcView.mpc_proc = Process(target=start_mpc_process, args=(MpcView.mpc_q,))
            MpcView.mpc_proc.daemon = True
            MpcView.mpc_proc.start()
            log.info(f"<MPC>:create MPC mqtt client back process {MpcView.mpc_proc.pid} success")
            MpcView.mpc_start_server_flag = True
        MpcView.mpc_q.put(branch)
        log.info(f"<MPC>:bms{branch}停止充电")
        MpcView.data['message'] = "OK"
        return JsonResponse(MpcView.data)
