#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    app收到了notify后回复
    http://showdoc.nevint.com/index.php?s=/13&page_id=1073
"""
import json
import time

import allure
import pytest
from utils.http_client import TSPRequest as hreq


# @pytest.mark.skip("manual")
class TestMeesageAPI(object):
    @pytest.fixture(scope='class', autouse=False)
    def prepare(self, env, mysql):
        user = 'nmp'
        data = {}
        data['host_app'] = env['host']['app']
        data['host_app_in'] = env['host']['app_in']
        data['app_id_phone'] = '10002' if user == 'li' else '10001'  # 10001 andriod， 10002 ios
        data['account_id'] = env['vehicles'][user]['account_id']
        data['phone'] = env['vehicles'][user]['phone']
        data['client_id'] = env['vehicles'][user]['client_id']
        data['client_id_app'] = env['vehicles'][user][f'client_id_app_{data["app_id_phone"]}']
        data['authorization'] = env['vehicles'][user][f'token_{data["app_id_phone"]}']
        data['device_id_app'] = env['vehicles'][user]['device_id_app']
        data['vehicle_id'] = env['vehicles'][user]['vehicle_id']
        # data['app_version'] = mysql['nmp_app'].fetch('clients', {'client_id': data['client_id_app'], 'app_id': data['app_id_phone']})[0]['app_version']
        return data

    @pytest.fixture(scope='function', autouse=False)
    def prepare_message_id(self, env, prepare):
        inputs = {
            "host": prepare['host_app_in'],
            "path": "/api/1/in/message/notify",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "hash_type": "md5",
                "region": "cn",
                "lang": "zh-cn",
                "app_id": "10013",
                "sign": ""
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCG',
                'async': False,
                'user_ids': prepare['account_id'],
                'ttl': 100000,
                'target_app_ids': prepare['app_id_phone'],
                'do_push': True,
                'scenario': 'fs_system',
                # 'channel': 'apns',  # apns for ios 不填的话默认是找最合适的方法推，例如先检测可不可以mqtt推，再尝试其他方法推送
                # 如手机在线并保持常亮的话，会是mqtt推送，否则按照苹果小米等不同手机类型推到不同平台，再由平台push
                # "category": "activity",  # 可以default， activity，red_packet等字段，分别推到手机的通知条目，活动条目，积分红包条目
                'payload': json.dumps({"target_link": "http://www.niohome.com", "description": "Description for test", "title": "Title for test"}),
            }
        }
        response = hreq.request(env, inputs)
        message_id = response['data'].pop('message_id', '')
        time.sleep(1)
        return message_id

    def test_report(self, env, prepare, mysql, prepare_message_id):
        """
        app收到了notify后回复
        http://showdoc.nevint.com/index.php?s=/13&page_id=1073
        """

        inputs = {
            "host": prepare['host_app'],
            "path": "/api/1/message/report",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
            },
            "params": {
                "hash_type": "md5",
                "region": "cn",
                "lang": "zh-cn",
                "sign": "",
                "app_id": prepare['app_id_phone']
            },
            "data": {
                'client_id': prepare['client_id_app'],
                'message_id': prepare_message_id,
                'ts': int(time.time())
            }
        }

        response = hreq.request(env, inputs)
        with allure.step("校验result_code"):
            assert response.get("result_code") == "success"

        # time.sleep(1)
        # with allure.step("校验mysql"):
        #     state = mysql['nmp_app'].fetch('message_state', {'message_id': prepare_message_id})[-1]['state']
        #     assert_equal(state, 10000)
