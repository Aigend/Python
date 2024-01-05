#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    重置client_id连接状态
    http://showdoc.nevint.com/index.php?s=/13&page_id=7365


"""

import allure
import pytest
from utils.http_client import TSPRequest as hreq


class TestMeesageAPI(object):
    @pytest.fixture(scope='class', autouse=False)
    def prepare(self, env, mysql):
        data = {}

        data['host_app'] = env['host']['app']
        data['host_app_in'] = env['host']['app_in']
        user = 'nmp'
        data['app_id_phone'] = '10002' if user == 'li' else '10001'  # 10001 andriod， 10002 ios
        data['account_id'] = env['vehicles'][user]['account_id']
        data['phone'] = env['vehicles'][user]['phone']
        data['client_id'] = env['vehicles'][user]['client_id']
        data['client_id_app'] = env['vehicles'][user][f'client_id_app_{data["app_id_phone"]}']
        data['authorization'] = env['vehicles'][user][f'token_{data["app_id_phone"]}']
        data['device_id_app'] = env['vehicles'][user]['device_id_app']
        data['vehicle_id'] = env['vehicles'][user]['vehicle_id']
        return data

    def test_reset_client_status(self, env, prepare):
        """
        重置client_id连接状态
        http://showdoc.nevint.com/index.php?s=/13&page_id=7365
        """
        inputs = {
            "host": prepare['host_app_in'],
            "path": "/api/1/in/message/reset_client_status",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "hash_type": "md5",
                "sign": "",
                "region": "cn",
                "lang": "zh-cn",
                "app_id": "10006"
            },
            "data": {
                'client_id': prepare['client_id_app'],
                'nonce': 'nondceafadfdasfadfa',
            }
        }

        response = hreq.request(env, inputs)
        with allure.step("校验result_code"):
            assert response.get("result_code") == "success"
