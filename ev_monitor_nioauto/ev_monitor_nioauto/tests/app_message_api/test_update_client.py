#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    用于信息上报给服务端，同时也是一种主动报活的机制，使得服务端将该客户端标记为活跃状态
    http://showdoc.nevint.com/index.php?s=/13&page_id=1070
"""

import allure
import pytest

from utils.assertions import assert_equal
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
        data['app_version'] = mysql['nmp_app'].fetch('clients', {'client_id': data['client_id_app'], 'app_id': data['app_id_phone']})[0]['app_version']
        return data

    def test_update_client(self, env, mysql, prepare):
        '''
        用于信息上报给服务端，同时也是一种主动报活的机制，使得服务端将该客户端标记为活跃状态
        http://showdoc.nevint.com/index.php?s=/13&page_id=1070

        * 当前支持更新 device_token 和 app_version
        * NMP Client Logic https://confluence.nioint.com/display/CVS/NMP+Client+Logic

        '''
        old_update_time = mysql['nmp_app'].fetch('clients', {'client_id': prepare['client_id_app'], 'app_version': prepare['app_version']})[0]['update_time']
        inputs = {
            "host": prepare['host_app'],
            "path": "/api/1/message/update_client",
            "method": "POST",
            "headers": {
                "authorization": prepare['authorization'],
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
            },
            "params": {
                "region": "cn",
                "hash_type": "md5",
                "lang": "zh-cn",
                "sign": "zh-cn",
                "app_id": prepare['app_id_phone']
            },
            "data": {
                'app_version': prepare['app_version'],
                'client_id': prepare['client_id_app'],
                'nonce': 'nondceafadfdasfadfa',
                'push_type': 'hwpush',
                'device_token': ' '
            }
        }

        response = hreq.request(env, inputs)
        with allure.step('校验response'):
            assert response.get("result_code") == 'success'

        with allure.step("校验mysql"):
            new_update_time = mysql['nmp_app'].fetch('clients', {'client_id': prepare['client_id_app'], 'app_version': prepare['app_version']})[0]['update_time']
            assert_equal(new_update_time != old_update_time, True)
