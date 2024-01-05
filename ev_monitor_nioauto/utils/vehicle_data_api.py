#!/usr/bin/env python
# coding=utf-8

"""
:file: test_evm_api.py
:author: zhiqiang.zhu
:Description: evm api
"""

import allure
import requests
from utils.commonlib import show_json

def evm_query_vehicle(host, vid, msg_type, ts):
    evm_query_vehicle_url = host + "/api/1/in/data/vehicle/" + vid + "/history"
    querystring = {
        "vehicle_id": vid,  # 3377,   #
        "start_time": ts - 10,  # 1487597732,  #一年对应的时间戳是31536000，一小时对应的时间戳是3600，开始时间结束时间间隔最大一年
        "end_time": ts + 10,  # 查询结束时间
        "size": 3,  # random.randint(0, 1000),  #数据大小, 大于0，小于或等于1000
        "start_index": 0,  # random.randint(0, 100),  #大于或等于0
        "type": msg_type,  # 查询数据类型, 必填
        "total_size": True  # 是否查数据总数, 默认：否
    }
    headers = {
        'content-type': "application/x-www-form-urlencoded",
    }
    r = requests.request("GET", evm_query_vehicle_url, params=querystring, headers=headers)
    assert r.status_code == 200, "从Cassandra中查询历史数据失败"
    # r = requests.get(evm_query_vehicle_url, data=pay_load)
    # log('DEBUG', 'Response is:\n{0}'.format(show_json(r.text)))
    with allure.step('查看Cassandra中的{0}消息:'.format(msg_type)):
        allure.attach(show_json(r.json()), "{0}内容：".format(msg_type), )
    # log('DEBUG', 'Response is:\n{0}'.format(show_json(r.json)))
    return r.json()


def vehicle_evm_msg(host, attribution, msg_type, ack, ts):
    url = host + "/api/1/in/data/vehicle/evm_msg"
    querystring = {
        "app_id": 10016,
        "lang": "zh-cn",
        "attribution": attribution,
        "type": msg_type,
        "ack": ack,
        "start_time": ts - 2000,  # 1487597732,  #一年对应的时间戳是31536000，一小时对应的时间戳是3600，开始时间结束时间间隔最大一年
        "end_time": ts + 2000,  # 查询结束时间
        "size": 3,  # 数据大小, 大于0，小于或等于1000
    }
    headers = {
        'content-type': "application/x-www-form-urlencoded",
    }
    r = requests.request("GET", url, params=querystring, headers=headers)
    response = r.json()
    # log('INFO', 'evm_msg response is:\n{0}'.format(show_json(response)))
    with allure.step('查看Cassandra中的{0}消息:'.format(msg_type)):
        allure.attach(show_json(r.json()), "{0}内容：".format(msg_type))

    return r.json()
