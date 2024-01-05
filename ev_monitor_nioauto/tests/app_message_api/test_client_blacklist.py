#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    当app不再被使用时，把该app加入黑名单，notify消息时不再推送给该app
    http://showdoc.nevint.com/index.php?s=/13&page_id=6294
"""

import allure
import pytest

from utils.assertions import assert_equal
from utils.httptool import request as rq
from utils.http_client import TSPRequest as hreq


class TestMeesageAPI(object):
    @pytest.fixture(scope='class', autouse=False)
    def prepare(self, env, mysql):
        data = {}
        user = 'nmp'
        data['client_id'] = env['vehicles'][user]['client_id']
        return data

    def test_client_blacklist_add(self, prepare, env, mysql):
        with allure.step('add blacklist'):
            inputs = {
                "host": env['host']['app_in'],
                "path": "/api/1/in/message/client_blacklist",
                "method": "POST",
                "headers": {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                "params": {
                    "app_id": "10000",
                    "sign": "",
                },
                "data": {
                    'client_ids': prepare['client_id'],
                    'action': 'add'
                }
            }
            response = hreq.request(env, inputs)
        with allure.step('校验response'):
            assert_equal(response['result_code'], 'success')
