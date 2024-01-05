#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    类似update_payload,更新已经notify的消息history_XX表里的数据
    http://showdoc.nevint.com/index.php?s=/13&page_id=5932

"""
import json
import random
import string
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
        # user = 'li'
        data['app_id_phone'] = '10002' if user == 'li' else '10001'  # 10001 andriod， 10002 ios
        data['account_id'] = env['vehicles'][user]['account_id']
        data['phone'] = env['vehicles'][user]['phone']
        data['phone_code'] = env['vehicles'][user]['phone_code']
        data['client_id'] = env['vehicles'][user]['client_id']
        data['client_id_app'] = env['vehicles'][user][f'client_id_app_{data["app_id_phone"]}']
        data['authorization'] = env['vehicles'][user][f'token_{data["app_id_phone"]}']
        data['device_id_app'] = env['vehicles'][user]['device_id_app']
        data['vehicle_id'] = env['vehicles'][user]['vehicle_id']
        data['client_info'] = mysql['nmp_app'].fetch('clients', {'client_id': data['client_id_app'], 'app_id': data['app_id_phone']})[0]
        data['app_version'] = data['client_info']['app_version']
        # data['app_version'] = '3.10.1' #hognzhenbi
        # data['app_version'] = '3.9.9' #liliu
        return data

    @pytest.fixture(scope='class', autouse=False)
    def account_login(self, env, prepare):
        """
        /acc/2/login
        接口文档：http://showdoc.nevint.com/index.php?s=/123&page_id=3160
        """
        mobile = prepare['phone']
        vc_code = prepare['phone_code']
        app_id = prepare['app_id_phone']
        country_code = '86'
        host = env['host']['app_in']
        http = {
            "host": host,
            "method": "POST",
            "uri": "/acc/2/login",
            "headers": {'content-type': 'application/x-www-form-urlencoded',
                        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
                        },
            "params": {
                'region': 'cn',
                'lang': 'zh-cn',
                'app_id': app_id,
                'nonce': int(time.time()),
            },
            "data": {
                'mobile': mobile,
                'verification_code': vc_code,
                'country_code': country_code,
                'authentication_type': 'mobile_verification_code',
                'device_id': app_id,
                "terminal": '{"name":"我的华为手机","model":"HUAWEI P10"}',
            },
        }
        with allure.step(f"请求/acc/2/login接口：{http}"):
            response_dict = rq(http['method'], url=http['host'] + http['uri'], params=http['params'], data=http['data'], headers=http['headers']).json()
        with allure.step(f"请求结果断言：{response_dict}"):
            assert response_dict['result_code'] == "success"
            assert response_dict['data']
        with allure.step(f"返回请求所需token：Bearer {response_dict['data']['access_token']}"):
            return f"Bearer {response_dict['data']['access_token']}"

    @pytest.fixture(scope="class", autouse=False)
    def prepare_bind(self, prepare, request, account_login):
        '''
        用户登陆|退出APP时，调用binding|unbinding 接口
        http://showdoc.nevint.com/index.php?s=/13&page_id=1071
        绑定和解绑客户端是针对用户而言的，每个用户可以绑定多个客户端，通过这样的机制能保证，推送给这个用户的时候，各个设备都可以收到相应的推送。同理，设备解绑之后将不再收到发送给此用户的信息。
        '''
        token = account_login
        http = {
            "host": prepare['host_app'],
            "uri": "/api/1/message/bind_client",
            "method": "POST",
            "headers": {
                "authorization": token,
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
                'nonce': ''.join(random.sample(string.ascii_letters, 11))
            }
        }

        response = rq(http['method'], url=http['host'] + http['uri'], params=http['params'], data=http['data'], headers=http['headers']).json()
        assert_equal(response['result_code'], 'success')
        time.sleep(1)

        def fin():
            http = {
                "host": prepare['host_app'],
                "uri": "/api/1/message/unbind_client",
                "method": "POST",
                "headers": {
                    "authorization": token,
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
                    'nonce': ''.join(random.sample(string.ascii_letters, 11))
                }
            }

            response = rq(http['method'], url=http['host'] + http['uri'], params=http['params'], data=http['data'], headers=http['headers']).json()
            assert_equal(response['result_code'], 'success')

        request.addfinalizer(fin)

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

    def test_update_msg(self, prepare, prepare_bind, prepare_message_id, mysql):
        """
        类似update_payload,更新已经notify的消息history_XX表里的数据
        http://showdoc.nevint.com/index.php?s=/13&page_id=5932

        """

        table = 'history_' + str(prepare['account_id'])[-3:]

        old_payload = mysql['nmp_app'].fetch(table, {'message_id': prepare_message_id}, ['payload'])[0]['payload']

        http = {
            "host": prepare['host_app_in'],
            "uri": "/api/1/in/message/update_msg",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                'app_id': '10006',
                "user_id": prepare['account_id'],
                'message_id': prepare_message_id,
                'payload': json.dumps({"target_link": "http://www.niohome.com", "description": "change description 6", "title": "change title 6"}),

            },
            "expect": {
                "result_code": "success",
            }
        }
        response = rq(http['method'], url=http['host'] + http['uri'], headers=http['headers'],
                      params=http['params']).json()

        check_response(response, http)

        with allure.step("校验mysql"):
            new_payload = mysql['nmp_app'].fetch(table, {'message_id': prepare_message_id}, ['payload'])[0]['payload']
            assert_equal(new_payload == old_payload, False)

def check_response(response, http):
    with allure.step('校验response'):
        response.pop('request_id', '')
        response.pop('server_time', '')
        assert_equal(response, http['expect'])
