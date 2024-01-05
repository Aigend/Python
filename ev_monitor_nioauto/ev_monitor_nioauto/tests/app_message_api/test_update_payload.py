#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    用于notify后更新数据库里的history_XX表的payload字段
    http://showdoc.nevint.com/index.php?s=/13&page_id=5860

"""
import json
import time
import allure
import pytest

from utils.assertions import assert_equal
from utils.httptool import request as rq

@pytest.mark.skip('deprecated')
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
        # data['app_version'] = '3.10.1' #hognzhenbi
        # data['app_version'] = '3.9.9' #liliu
        return data

    @pytest.fixture(scope='function', autouse=False)
    def prepare_message_id(self, prepare):
        http = {
            "host": prepare['host_app_in'],
            "uri": "/api/1/in/message/notify",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "app_id": "10013"
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
        response = rq(http['method'], url=http['host'] + http['uri'],
                      params=http['params'], data=http['data'], headers=http['headers']).json()
        message_id = response['data'].pop('message_id', '')
        time.sleep(1)
        return message_id

    def test_update_payload(self, prepare, mysql, prepare_message_id):
        """
        用于notify后更新数据库里的history_XX表的payload字段
        http://showdoc.nevint.com/index.php?s=/13&page_id=5860
        """

        table = 'history_' + str(prepare['account_id'])[-3:]
        old_payload = mysql['nmp_app'].fetch(table, {'message_id': prepare_message_id})[0]['payload']

        http = {
            "host": prepare['host_app'],
            "uri": "/api/1/message/update_payload",
            "method": "POST",
            "headers": {
                "authorization": prepare['authorization'],
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
            },
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "app_id": prepare['app_id_phone']
            },
            "data": {
                'client_id': prepare['client_id_app'],
                'message_id': prepare_message_id,

                'new_payload': json.dumps({"target_link": "http://www.niohome.com", "description": "change description 5", "title": "change title 5"}),
            },
            "expect": {
                "result_code": "success",
            }
        }

        response = rq(http['method'], url=http['host'] + http['uri'],
                      params=http['params'], data=http['data'], headers=http['headers']).json()
        check_response(response, http)

        with allure.step("校验mysql"):
            new_payload = mysql['nmp_app'].fetch(table, {'message_id': prepare_message_id})[0]['payload']
            assert_equal(new_payload == old_payload, False)

def check_response(response, http):
    with allure.step('校验response'):
        response.pop('request_id', '')
        response.pop('server_time', '')
        assert_equal(response, http['expect'])
