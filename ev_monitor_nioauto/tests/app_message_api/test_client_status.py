#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    检查client状态 [ONLINE|OFFLINE], 用于判断服务是否立即发送信息（notification/command）到客户端
    http://showdoc.nevint.com/index.php?s=/13&page_id=2508
"""

import allure
from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq


def test_client_status(env, cmdopt):
    if cmdopt == 'test':
        client_id = "byUWb9stOBL3_bzI4YeqE7mB584QXmcShMP8yBJZIuU="
        update_time = 1508407450000
    else:
        client_id = "ChBV77cPTx4u6_zOvqV8wSTnEAEYuwEgkk4oAA=="
        update_time = 1500541345000
    inputs = {
        "host": env['host']['app_in'],
        "path": "/api/1/in/message/client_status",
        "method": "GET",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "params": {
            "app_id": "10000",
            'client_ids': client_id,
            'sign': "",
        },
    }
    response = hreq.request(env, inputs)
    with allure.step('校验response'):
        expect = {
            "client_status": [
                {
                    "client_id": client_id,
                    "status": "OFFLINE",
                    "update_time": update_time
                }
            ],
            'result_code': 'success'
        }
        response.pop('request_id', '')
        response.pop('server_time', '')
        assert_equal(response, expect)
