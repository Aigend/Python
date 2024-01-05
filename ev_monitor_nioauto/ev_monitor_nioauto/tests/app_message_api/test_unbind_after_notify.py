#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    notify后，让手机退出登陆状态
    http://showdoc.nevint.com/index.php?s=/13&page_id=60

"""
import json
import time
import allure
import pytest

from utils.assertions import assert_equal
# from utils.httptool import request as rq
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

    @pytest.fixture(scope="class", autouse=False)
    def prepare_bind(self, env, prepare, request):
        '''
        用户登陆|退出APP时，调用binding|unbinding 接口
        http://showdoc.nevint.com/index.php?s=/13&page_id=1071

        绑定和解绑客户端是针对用户而言的，每个用户可以绑定多个客户端，通过这样的机制能保证，推送给这个用户的时候，各个设备都可以收到相应的推送。同理，设备解绑之后将不再收到发送给此用户的信息。

        '''

        inputs = {
            "host": prepare['host_app'],
            "path": "/api/1/message/bind_client",
            "method": "POST",
            "headers": {
                "authorization": prepare['authorization'],
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "sign": "",
                "app_id": prepare['app_id_phone']
            },
            "data": {
                'client_id': prepare['client_id_app'],
                'nonce': 'nondceafadfdasfadfa'
            }
        }

        response = hreq.request(env, inputs)
        with allure.step('校验response'):
            assert response.get("result_code") == 'success'
        time.sleep(1)

        def fin():
            inputs = {
                "host": prepare['host_app'],
                "uri": "/api/1/message/unbind_client",
                "method": "POST",
                "headers": {
                    "authorization": prepare['authorization'],
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                "params": {
                    "region": "cn",
                    "lang": "zh-cn",
                    "app_id": prepare['app_id_phone']
                },
                "data": {
                    'client_id': prepare['client_id_app'],
                    'nonce': 'nondceafadfdasfadfa'
                }
            }

            response = hreq.request(env, inputs)
            with allure.step('校验response'):
                assert response.get("result_code") == 'success'

        request.addfinalizer(fin)

    @pytest.mark.skip('deprecated')
    def test_unbind_after_notify(self,env, prepare, prepare_bind):
        '''
        # 已废弃
        notify后，让手机退出登陆状态
        http://showdoc.nevint.com/index.php?s=/13&page_id=60

        需要手机先bind  '''
        inputs = {
            "host": prepare['host_app_in'],
            "path": "/api/1/in/message/unbind_after_notify",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "sign": "zh-cn",
                "app_id": "10013"
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCG',
                'async': False,
                'user_id': prepare['account_id'],
                'ttl': 100000,
                'target_app_ids': prepare['app_id_phone'],
                'do_push': True,
                'included_device_ids': prepare['device_id_app'],
                'scenario': 'fs_system',
                # 'channel': 'apns',  # for ios
                # "category": "activity",  # 可以default， activity，red_packet等字段，分别推到手机的通知条目，活动条目，积分红包条目

                'payload': json.dumps({"target_link": "http://www.niohome.com", "description": "description 6", "title": "title 6"}),
            }
        }

        response = hreq.request(env, inputs)
        with allure.step('校验response'):
            expect = {
                "data": {
                    "details": [
                        {
                            "client_id": prepare['client_id_app'],
                            "result": "success",
                            "device_id": prepare['device_id_app'],
                            "user_id": prepare['account_id'],
                            "app_id": prepare['app_id_phone']
                        }
                    ]
                },
                "success": 1,
                "failure": 0,
                "result_code": "success"
            }
            response['data'].pop('message_id', '')
            response.pop('request_id', '')
            response.pop('server_time', '')
            assert_equal(response, expect)

