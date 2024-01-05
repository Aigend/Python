# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/1/12 16:50
# @File: views.py
import json
import multiprocessing
import sys
import time
from multiprocessing import Queue

import psutil
from django.http import JsonResponse
from django.views import View

from meter.meter_data import METER_MAP
from meter.meter_msg import MeterMsg
from meter.meter_utils import start_meter_modbus_process
from utils.constant import SERIAL_NODE
from utils.log import log
from utils.tools import check_serial_port_available


class MeterView(View):

    meter_q = Queue()
    meter_param = {}
    meter_success_flag = False
    meter_prc = ""

    def get(self, request, *args, **kwargs):
        data = {
            'result_code': '0',
            'message': 'OK',
        }
        if isinstance(MeterView.meter_prc, multiprocessing.Process) and MeterView.meter_prc.is_alive():
            log.info(f"<Meter>:process pid {MeterView.meter_prc.pid} kill start")
            MeterView.meter_prc.terminate()
            MeterView.meter_prc.join(timeout=10)
            MeterView.meter_success_flag = False
            SERIAL_NODE.pop("meter")
            time.sleep(1)
        return JsonResponse(data)

    def post(self, request):
        result = {
            'result_code': '0',
            'message': 'OK'
        }
        json_param = json.loads(request.body)
        # log.debug(f"<Meter>:Post发送的电表的数据:{json_param}")
        try:
            meter_covert_key_to_msg(json_param)
            result['data'] = MeterView.meter_param
        except ValueError:
            _, exc_value, _ = sys.exc_info()
            log.error(f"<Meter>:Post请求实时信息数据初始化异常:{str(exc_value)}")
            return JsonResponse({'result_code': "3", 'message': f'<Meter>:数据初始化异常，请排查报错的数据类型, {exc_value}', })
        meter_obj = MeterMsg()
        meter_obj.set_meter_real_value(MeterView.meter_param)
        meter_obj.meter_data_init()
        # 获取 meter 对应的串口
        if not check_serial_port_available("Meter"):
            log.error(f"<Meter>:电表未获取到对应的串口信息，请确认硬件环境:{SERIAL_NODE.get('Meter')}")
            return JsonResponse({'result_code': "3", 'message': "<Meter>:电表未获取到对应的串口信息，请确认硬件环境", })
        if MeterView.meter_success_flag:
            MeterView.meter_q.put((meter_obj.slave_1_data,
                                   meter_obj.slave_2_data))
            time.sleep(3)
            # log.info("<Meter>:post request, send real time data success")
            return JsonResponse(result)
        MeterView.meter_prc = multiprocessing.Process(target=start_meter_modbus_process,
                                                      args=(MeterView.meter_q, SERIAL_NODE.get("meter")))
        MeterView.meter_prc.daemon = True
        MeterView.meter_prc.start()
        psutil.Process(MeterView.meter_prc.pid).cpu_affinity([2])
        MeterView.meter_q.put((meter_obj.slave_1_data,
                               meter_obj.slave_2_data))
        MeterView.meter_success_flag = True
        time.sleep(8)
        log.info(f"<Meter>:meter has connect success first, pid:{MeterView.meter_prc.pid}")
        # log.info("<Meter>:post request, send real time data success")
        return JsonResponse(result)


def meter_covert_key_to_msg(post_body):
    """
        把key值和定义的变量进行映射，架构不变的情况下，修改映射关系即可
    :param post_body:
    :return:
    """
    for meter_num, meter_val in post_body.items():
        if meter_num in ['meter0', 'meter1', ] and isinstance(meter_val, dict):
            meter_info = meter_val.get('meter_info', {})
            if isinstance(meter_info, dict):
                for k, v in meter_info.items():
                    if k in METER_MAP:
                        MeterView.meter_param[METER_MAP[k]] = v
                    else:
                        log.warning(f"<Meter>:key id:{k},未在电表的key map中找到对应关系, 数据无需发送")
    # log.debug(f"<Meter>:映射处理后的电表数据:{meter_param}")
