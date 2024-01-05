# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:47
# @File:views.py
import json
import sys

from django.http import JsonResponse
from django.views import View

from sensor import sensor_msg
from sensor.sensor_data import key_map
from utils.constant import SERIAL_NODE
from utils.log import log
from utils.tools import check_serial_port_available


class SensorView(View):
    sensor_param = {}
    sensor_obj = sensor_msg.SensorMsg()

    def get(self, request):
        data = {
            'result_code': '0',
            'message': 'OK',
        }
        if SensorView.sensor_obj.start_server_flag:
            log.info("<Sensor>:pid threading close start")
            SensorView.sensor_obj.start_server_flag = False
            SensorView.sensor_param.clear()
            # SERIAL_NODE.pop("sensor")
            SensorView.sensor_obj.stop_sensor_server()
        return JsonResponse(data)

    def post(self, request):
        data = {
            'result_code': '0',
            'message': 'OK',
            'data': {}
        }
        param = json.loads(request.body)
        # log.debug(f"<Sensor>:Post请求的数据为:{str(param)}")
        try:
            sensor_covert_key_to_msg(param)
        except ValueError:
            _, exc_value, _ = sys.exc_info()
            log.error(f"<Sensor>:Post请求实时信息数据初始化异常:{str(exc_value)}")
            return JsonResponse(
                {'result_code': "3", 'message': f'<Sensor>:数据初始化异常，请排查报错的数据类型, {exc_value}', })
        ch1_sensor_temperature = int(
            float(SensorView.sensor_param.get('ch1_sensor_temperature', 0)) * 10)  # 把实际数值放大10倍变成整数
        ch1_sensor_humidity = int(float(SensorView.sensor_param.get('ch1_sensor_humidity', 0)) * 10)  # 把实际数值放大10倍变成整数
        ch1_sensor_temperature = sensor_data_covert(ch1_sensor_temperature, "ch1_sensor_temperature", data)
        ch1_sensor_humidity = sensor_data_covert(ch1_sensor_humidity, "ch1_sensor_humidity", data)
        ch2_sensor_temperature = int(
            float(SensorView.sensor_param.get('ch2_sensor_temperature', 0)) * 10)  # 把实际数值放大10倍变成整数
        ch2_sensor_humidity = int(float(SensorView.sensor_param.get('ch2_sensor_humidity', 0)) * 10)  # 把实际数值放大10倍变成整数
        ch2_sensor_temperature = sensor_data_covert(ch2_sensor_temperature, "ch2_sensor_temperature", data)
        ch2_sensor_humidity = sensor_data_covert(ch2_sensor_humidity, "ch2_sensor_humidity", data)
        if not check_serial_port_available("Sensor"):
            log.error(f'<Sensor>:串口不可用, 请确认硬件环境是否配置异常:{SERIAL_NODE.get("sensor")}')
            return JsonResponse({
                'result_code': '2',
                'message': '<Sensor>:串口不可用, 请确认硬件环境是否配置异常', })
        if not SensorView.sensor_obj.start_server_flag:
            SensorView.sensor_obj.port = SERIAL_NODE.get("sensor")
            # log.info(f"<Sensor>:sensor port is {SensorView.sensor_obj.port}")
            SensorView.sensor_obj.start_sensor_server()
            SensorView.sensor_obj.start_server_flag = True
            log.info("<Sensor>:pid threading create success")
        SensorView.sensor_obj.set_meter_RegParam(0x0001, ch1_sensor_temperature)  # 湿度
        SensorView.sensor_obj.set_meter_RegParam(0x0002, ch1_sensor_humidity)  # 温度
        SensorView.sensor_obj.set_meter_RegParam(0x0003, ch2_sensor_temperature)  # 湿度
        SensorView.sensor_obj.set_meter_RegParam(0x0004, ch2_sensor_humidity)  # 温度
        log.info("<Sensor>:post request, send real time data success")
        return JsonResponse(data)


def sensor_covert_key_to_msg(post_body):
    """
        把key值和定义的变量进行映射，架构不变的情况下，修改映射关系即可
    :param post_body:
    :return:
    """
    body = post_body.get("temp_humi_sensor", {}).get("sensor_info", {})
    body.update(post_body.get("temp_humi_sensor", {}).get("alarm_info", {}))
    for k, v in body.items():
        if k in key_map:
            SensorView.sensor_param[key_map[k]] = v
        else:
            log.warning(f"<Sensor>:id {k},未在Sensor的key map中找到对应关系")
    # log.debug(f"<Sensor>:最终发送的温湿度的数据:{str(sensor_param)}")


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
    # log.debug(f"<Sensor>:{module}数据,负数转换后的数据:{hex(result)}")
    data['data'][module] = result
    return result
