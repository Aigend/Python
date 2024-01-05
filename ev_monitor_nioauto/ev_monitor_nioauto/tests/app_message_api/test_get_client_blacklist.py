#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    获取client黑名单。黑名单作用是当app不再被使用时，把该app加入黑名单，notify消息时不再推送给该app
    http://showdoc.nevint.com/index.php?s=/13&page_id=6318
"""

import allure
from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq


def test_get_client_blacklist(env):
    """
    获取client黑名单
    """
    with allure.step('get blacklist'):
        client_id = env['vehicles']["nmp"]['client_id']
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/in/message/get_client_blacklist",
            "method": "GET",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                "app_id": "10000",
                'client_ids': client_id,
                'sign': "",
            }
        }

        response = hreq.request(env, inputs)
        with allure.step('校验response'):
            response.pop('request_id', '')
            response.pop('server_time', '')
            expect = {'data': {client_id: True}, 'debug_msg': '', 'result_code': 'success'}
            assert_equal(response, expect)
