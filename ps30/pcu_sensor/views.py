# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/1/12 15:41
# @File: views.py
import json
import sys

from django.http import JsonResponse
from django.views import View

from pcu_sensor import pcu_sensor_msg
from pcu_sensor.pcu_sensor_data import PCU_SENSOR_MAP
from utils.constant import SERIAL_NODE
from utils.log import log
from utils.tools import check_serial_port_available


class PcuSensorView(View):

    sensor_param = {}
    
    sensor_obj = pcu_sensor_msg.PcuSensorMsg()
    
    def get(self, request):
        data = {
            'result_code': '0',
            'message': 'OK',
        }
        if self.sensor_obj.start_server_flag:
            log.info("<PCU_Sensor>:pid threading close start")
            self.sensor_obj.start_server_flag = False
            self.sensor_param.clear()
            # SERIAL_NODE.pop("pcu_sensor")
            self.sensor_obj.stop_sensor_server()
        return JsonResponse(data)

    def post(self, request):
        data = {
            'result_code': '0',
            'message': 'OK',
            'data': {}
        }
        param = json.loads(request.body)
        # log.debug(f"<PCU_Sensor>:Post请求的数据为:{str(param)}")
        try:
            sensor_covert_key_to_msg(param)
        except ValueError:
            _, exc_value, _ = sys.exc_info()
            log.error(f"<PCU_Sensor>:Post请求实时信息数据初始化异常:{str(exc_value)}")
            return JsonResponse({'result_code': "3", 'message': f'<PCU_Sensor>:数据初始化异常，请排查报错的数据类型, {exc_value}', })
        c_chan11_hum_value = int(float(self.sensor_param.get('c_chan11_hum_value', 0)) * 10)  # 把实际数值放大10倍变成整数
        c_chan11_tem_value = int(float(self.sensor_param.get('c_chan11_tem_value', 0)) * 10)  # 把实际数值放大10倍变成整数
        c_chan12_hum_value = int(float(self.sensor_param.get('c_chan12_hum_value', 0)) * 10)  # 把实际数值放大10倍变成整数
        c_chan12_tem_value = int(float(self.sensor_param.get('c_chan12_tem_value', 0)) * 10)  # 把实际数值放大10倍变成整数
        c_chan11_hum_value = sensor_data_covert(c_chan11_hum_value, "c_chan11_hum_value", data)
        c_chan11_tem_value = sensor_data_covert(c_chan11_tem_value, "c_chan11_tem_value", data)
        # 查看pcu 代码 pcu 传给主控的数据固定为0，这里传值给PCU没实际意义
        c_chan12_hum_value = sensor_data_covert(c_chan12_hum_value, "c_chan12_hum_value", data)
        c_chan12_tem_value = sensor_data_covert(c_chan12_tem_value, "c_chan12_tem_value", data)
        if not check_serial_port_available("PCU_Sensor"):
            log.error(f'<PCU_Sensor>:串口不可用, 请确认硬件环境是否配置异常:{SERIAL_NODE.get("pcu_sensor")}')
            return JsonResponse({
                'result_code': '2',
                'message': '<PCU_Sensor>:串口不可用, 请确认硬件环境是否配置异常', })
        if not self.sensor_obj.start_server_flag:
            # SERIAL_NODE["pcu_sensor"] = "COM4"  # 调试使用
            self.sensor_obj.port = SERIAL_NODE.get("pcu_sensor")
            # log.info(f"<PCU_Sensor>:pcu sensor port is {self.sensor_obj.port}")
            self.sensor_obj.start_sensor_server()
            self.sensor_obj.start_server_flag = True
            log.info("<PCU_Sensor>:pid threading create success")
        self.sensor_obj.set_meter_RegParam(0x0001, c_chan11_hum_value)  # 湿度
        self.sensor_obj.set_meter_RegParam(0x0002, c_chan11_tem_value)   # 温度
        self.sensor_obj.set_meter_RegParam(0x0003, c_chan12_hum_value)  # 湿度
        self.sensor_obj.set_meter_RegParam(0x0004, c_chan12_tem_value)   # 温度
        # log.info("<PCU_Sensor>:post request, send real time data success")
        return JsonResponse(data)


def sensor_covert_key_to_msg(post_body):
    """
        把key值和定义的变量进行映射，架构不变的情况下，修改映射关系即可
    :param post_body:
    :return:
    """
    body = post_body.get("pcu_temp_humi_sensor", {}).get("sensor_info", {})
    body.update(post_body.get("pcu_temp_humi_sensor", {}).get("alarm_info", {}))
    for k, v in body.items():
        if k in PCU_SENSOR_MAP:
            PcuSensorView.sensor_param[PCU_SENSOR_MAP[k]] = v
        else:
            log.warning(f"<PCU_Sensor>:id {k},未在PCU Sensor的key map中找到对应关系")
    # log.info(f"<PCU_Sensor>:最终发送的温湿度的数据:{PcuSensorView.sensor_param}")


def sensor_data_covert(req, module, data, num=16):
    """
    把负数进行转换后发送字节数据
    :param req:
    :param module:
    :param data:
    :param num:
    :return:
    """
    if req >= 0:
        data['data'][module] = req
        return req

    def reverse_func(st):
        t = []
        for s in st:
            if s == "0":
                t.append("1")
            else:
                t.append("0")
        return "".join(t)
    temp = abs(req)
    bin_org = str(bin(int(temp))).replace('0b', '')
    bin_org_str = ''.join(bin_org)
    while len(bin_org_str) < int(num):
        bin_org_str = '0' + bin_org_str
    reverse_binary = reverse_func(bin_org_str)
    result = int(reverse_binary, 2) + 1
    # log.info(f"<PCU_Sensor>:{module}数据,负数转换后的数据:{hex(result)}")
    data['data'][module] = result
    return result
