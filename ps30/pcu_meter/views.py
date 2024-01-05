# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:47
# @File:views.py
import json
import multiprocessing
import sys
import time
from multiprocessing import Queue

import psutil
from django.http import JsonResponse
from django.views.generic import View

from pcu_meter.pcu_meter_data import PCU_METER_MAP
from pcu_meter.pcu_meter_msg import PcuMeterMsg
from pcu_meter.pcu_meter_utils import start_meter_modbus_process
from utils.constant import SERIAL_NODE
from utils.log import log
from utils.tools import check_serial_port_available


# pcu_meter_q = Queue()
# pcu_meter_param = {}
# pcu_meter_success_flag = False
# pcu_meter_prc = ""


class PcuMeterView(View):

    pcu_meter_q = Queue()
    pcu_meter_param = {}
    pcu_meter_prc = ""
    pcu_meter_success_flag = False

    def get(self, request, *args, **kwargs):
        data = {
            'result_code': '0',
            'message': 'OK',
        }
        if isinstance(PcuMeterView.pcu_meter_prc, multiprocessing.Process) and PcuMeterView.pcu_meter_prc.is_alive():
            log.info(f"<PCU_Meter>:process pid {PcuMeterView.pcu_meter_prc.pid} kill start")
            PcuMeterView.pcu_meter_prc.terminate()
            PcuMeterView.pcu_meter_prc.join(timeout=10)
            PcuMeterView.pcu_meter_success_flag = False
            # SERIAL_NODE.pop("pcu_meter")
            time.sleep(1)
        return JsonResponse(data)

    def post(self, request):
        result = {
            'result_code': '0',
            'message': 'OK'
        }
        json_param = json.loads(request.body)
        # log.debug(f"<PCU_Meter>:Post发送的电表的数据:{json_param}")
        try:
            meter_covert_key_to_msg(json_param)
            result['data'] = PcuMeterView.pcu_meter_param
        except ValueError:
            _, exc_value, _ = sys.exc_info()
            log.error(f"<PCU_Meter>:Post请求实时信息数据初始化异常:{str(exc_value)}")
            return JsonResponse({'result_code': "3", 'message': f'<PCU_Meter>:数据初始化异常，请排查报错的数据类型, {exc_value}', })
        pcu_meter_obj = PcuMeterMsg()
        pcu_meter_obj.set_meter_real_value(PcuMeterView.pcu_meter_param)
        pcu_meter_obj.meter_data_init()
        # 获取 pcu_meter 对应的串口
        if not check_serial_port_available("PCU_Meter"):
            log.error(f"<PCU_Meter>:电表未获取到对应的串口信息，请确认硬件环境:{SERIAL_NODE.get('pcu_meter')}")
            return JsonResponse({'result_code': "3", 'message': "<PCU_Meter>:电表未获取到对应的串口信息，请确认硬件环境", })
        if PcuMeterView.pcu_meter_success_flag:
            PcuMeterView.pcu_meter_q.put((pcu_meter_obj.slave_1_data,
                                          pcu_meter_obj.slave_2_data,
                                          pcu_meter_obj.slave_3_data,
                                          pcu_meter_obj.slave_4_data))
            time.sleep(3)
            return JsonResponse(result)
        # log.info(f"<PCU_Meter>:pcu_meter port is {SERIAL_NODE['pcu_meter']}")
        PcuMeterView.pcu_meter_prc = multiprocessing.Process(target=start_meter_modbus_process,
                                                             args=(PcuMeterView.pcu_meter_q,
                                                                   SERIAL_NODE.get("pcu_meter")))
        PcuMeterView.pcu_meter_prc.daemon = True
        PcuMeterView.pcu_meter_prc.start()
        psutil.Process(PcuMeterView.pcu_meter_prc.pid).cpu_affinity([2])
        PcuMeterView.pcu_meter_q.put((pcu_meter_obj.slave_1_data,
                                      pcu_meter_obj.slave_2_data,
                                      pcu_meter_obj.slave_3_data,
                                      pcu_meter_obj.slave_4_data))
        PcuMeterView.pcu_meter_success_flag = True
        time.sleep(8)
        log.info(f"<PCU_Meter>:pcu_meter has connect success first, pid:{PcuMeterView.pcu_meter_prc.pid}")
        # log.info("<PCU_Meter>:post request, send real time data success")
        return JsonResponse(result)



# def handle(request, typ):
#     """
#
#     :param request:
#     :param typ:
#     :return:
#     """
#     result = {
#         'result_code': '0',
#         'message': 'OK'
#     }
#     if request.method == 'POST':
#         json_param = json.loads(request.body)
#         log.debug(f"<PCU_Meter>:Post发送的电表的数据:{json_param}")
#         try:
#             meter_covert_key_to_msg(json_param)
#         except ValueError:
#             _, exc_value, _ = sys.exc_info()
#             log.error(f"<PCU_Meter>:Post请求实时信息数据初始化异常:{str(exc_value)}")
#             return JsonResponse({'result_code': "3", 'message': f'<PCU_Meter>:数据初始化异常，请排查报错的数据类型, {exc_value}', })
#         global pcu_meter_q, pcu_meter_param, pcu_meter_prc, pcu_meter_success_flag
#         pcu_meter_obj = PcuMeterMsg()
#         pcu_meter_obj.set_meter_real_value(pcu_meter_param)
#         pcu_meter_obj.meter_data_init()
#         if pcu_meter_success_flag:
#             pcu_meter_q.put((pcu_meter_obj.slave_1_data,
#                              pcu_meter_obj.slave_2_data,
#                              pcu_meter_obj.slave_3_data,
#                              pcu_meter_obj.slave_4_data))
#             time.sleep(3)
#         else:
#             # 获取 pcu_meter 对应的串口
#             check_serial_port_available("PCU_Meter")
#             if not SERIAL_NODE.get("pcu_meter"):
#                 log.error(f"<PCU_Meter>:电表未获取到对应的串口信息，请确认硬件环境:{SERIAL_NODE}")
#                 return JsonResponse({'result_code': "3", 'message': "<PCU_Meter>:电表未获取到对应的串口信息，请确认硬件环境", })
#             log.info(f"<PCU_Meter>:pcu_meter port is {SERIAL_NODE['pcu_meter']}")
#             pcu_meter_prc = multiprocessing.Process(target=start_meter_modbus_process,
#                                                     args=(pcu_meter_q, SERIAL_NODE.get("pcu_meter")))
#             pcu_meter_prc.daemon = True
#             pcu_meter_prc.start()
#             psutil.Process(pcu_meter_prc.pid).cpu_affinity([2])
#             pcu_meter_q.put((pcu_meter_obj.slave_1_data,
#                              pcu_meter_obj.slave_2_data,
#                              pcu_meter_obj.slave_3_data,
#                              pcu_meter_obj.slave_4_data))
#             pcu_meter_success_flag = True
#             time.sleep(8)
#             log.info(f"<PCU_Meter>:pcu_meter has connect success first, pid:{pcu_meter_prc.pid}")
#         if typ == 'allinfo':
#             log.info("<PCU_Meter>:post request, send real time data success")
#             return JsonResponse(result)
#         else:
#             result['result_code'] = '1'
#             result['message'] = '<PCU_Meter>:type error'
#             return JsonResponse(result)
#     else:
#         result['result_code'] = '3'
#         result['message'] = '<PCU_Meter>:request not POST'
#         return JsonResponse(result)


def meter_covert_key_to_msg(post_body):
    """
        把key值和定义的变量进行映射，架构不变的情况下，修改映射关系即可
    :param post_body:
    :return:
    """
    for meter_num, meter_val in post_body.items():
        if meter_num in ['meter0', 'meter1', 'meter2', 'meter3'] and isinstance(meter_val, dict):
            meter_info = meter_val.get('meter_info', {})
            if isinstance(meter_info, dict):
                for k, v in meter_info.items():
                    if k in PCU_METER_MAP:
                        PcuMeterView.pcu_meter_param[PCU_METER_MAP[k]] = v
                    else:
                        log.warning(f"<PCU_Meter>:key id:{k},未在电表的key map中找到对应关系, 数据无需发送")
    # log.debug(f"<PCU_Meter>:映射处理后的电表数据:{pcu_meter_param}")

# def meter_kill_process(request):
#     data = {
#         'result_code': '0',
#         'message': 'OK',
#     }
#     global pcu_meter_prc, pcu_meter_success_flag
#     if isinstance(pcu_meter_prc, multiprocessing.Process) and pcu_meter_prc.is_alive():
#         log.info(f"<PCU_Meter>:process pid {pcu_meter_prc.pid} kill start")
#         pcu_meter_prc.terminate()
#         pcu_meter_prc.join(timeout=10)
#         pcu_meter_success_flag = False
#         SERIAL_NODE.pop("pcu_meter")
#         time.sleep(1)
#     return JsonResponse(data)
