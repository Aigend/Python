# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 20:47
# @File:views.py
import json
import time

from django.http import JsonResponse

from oss_welkin.oss_utils import get_oss_alarm_data, get_oss_real_time_data, get_oss_event_data
from oss_welkin.tk_utils import get_tk_data_real_time
from utils.log import log


def rec_realtime_data(request):
    """
    请求实时数据
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
    station_id = body.get('resource_id')
    site = body.get("site")
    if not station_id or not site:
        log.error(f"<OSS_TK>:station_id and site is null")
        response['message'] = 'station_id and site is null'
        return JsonResponse(response)
    for key in body['keys']:
        key = str(key)
        res = get_oss_real_time_data(station_id, key) if site == "oss" else get_tk_data_real_time(station_id, key)
        response['data']['point_data'].append(res)
    log.info(f"<OSS>:Response:{response}")
    return JsonResponse(response)


def rec_alarm_data(request):
    """
    请求告警数据
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
    station_id = body.get('resource_id')
    site = body.get("site")
    state = body.get("state")
    if not station_id or not site or not state:
        log.error(f"<OSS_TK>:station_id and site is null")
        response['message'] = 'station_id and site is null'
        return JsonResponse(response)
    state = True if int(state) > 0 else False
    for key in body['keys']:
        res = get_oss_alarm_data(station_id, str(key), state)
        response['data']['point_data'].append(res)
    log.info(f"<OSS>:Response:{response}")
    return JsonResponse(response)


def rec_event_data(request):
    """

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
    # 根据不同业务补充
    key_map = {
        "rid": "500018",  # 用于换电事件中过滤订单事件
        "branch_id": "107002"  # 用于充电事件中过滤特定支路的事件
    }
    body = json.loads(request.body)
    station_id = body.get('resource_id')
    site = body.get("site")
    timestamp = int(body.get("timestamp", 0))
    _k, _v = None, None
    for k, v in key_map.items():
        if k in body:
            _k = v
            _v = str(body.get(k, ""))
            break
    if not station_id or not site:
        log.error(f"<OSS_TK>:station_id and site is null")
        response['message'] = 'station_id and site is null'
        return JsonResponse(response)
    for key in body['keys']:
        select = {"key": _k, "value": _v} if _k and _v else {}
        res = get_oss_event_data(station_id, str(key), select, timestamp)
        if res:
            response['data']['point_data'].append(res)
        else:
            response['data']['point_data'].append({})
    log.info(f"<OSS>:Response:{response}")
    return JsonResponse(response)
