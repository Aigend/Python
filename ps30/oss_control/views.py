# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:rosa.xiao
# @Time:2023/12/1 20:48
# @File:views.py
import json
import time

from django.http import JsonResponse

from oss_control.oss_control_utils import generateVirtualKey, remote_control
from utils.log import log

def rec_genereateVirtualKey_data(request):
    """
    请求换电鉴权消息
    :param request:
    :return:
    """
    response = {
        'datetime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        'result_code': "0",
        'message': "OK",
        'data': {
            'point_data': []
        }
    }
    body = json.loads(request.body)
    log.info(body)
    res = generateVirtualKey(body)
    response['data']['point_data'].append(res)
    log.info(f"<OSS>:Response:{response}")
    return JsonResponse(response)

def rec_remote_control_data(request):
    """
    请求电池指令
    :param request:
    :return:
    """
    response = {
        'datetime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        'result_code': "0",
        'message': "",
        'data': {
            'point_data': []
        }
    }
    body = json.loads(request.body)
    log.info(body)
    station_id = body.get('resource_id')
    control_cmd = body.get('control_cmd')
    if not station_id :
        log.error(f"<OSS_TK>:station_id is null")
        response['message'] = 'station_id is null'
        return JsonResponse(response)
    res = remote_control(station_id,control_cmd)
    response['data']['point_data'].append(res)
    log.info(f"<api><rep>:{response}")
    return JsonResponse(response)


