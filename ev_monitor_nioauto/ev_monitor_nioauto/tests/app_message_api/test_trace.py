#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    查看消息发送状态
    http://showdoc.nevint.com/index.php?s=/13&page_id=876


    1:服务收到消息   2501:加入发送队列    5001:消息从服务端发出去往客户端，如果是发给第三方如小米，苹果时，则已收到了第三方接口的返回   10000:收到客户端回应
    * 这几个状态码不一定全有，只能提供参考。，特别是notify_all时，可能有些状态码会丢。
    * 调用notify接口时，手机如果没在线且mqtt时，只有1，2501， 如果在线会返回1，2501，5001， 10000四个状态。只调用一次notify，如果手机没收到，也不会重复notify，但会在消息列表里显示。
    * 调用command接口时，CGW不在线，只返回1
    * 调用notify_hu接口时，CDC不在线，返回1，2501，CDC恢复在线，会增加5001，10000
    * notify 小米的时候，根据设备登陆NIOApp的活跃程度（即每天的连接数，连接数每天会变动）的一定倍数关系来确定当天能够接受多少条push信息。
        所以如果小米设备连接不活跃的话，可能给的push配额会比较少导致5001 exceed quota error

"""
import json
import time
import allure
import pytest

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq


@pytest.mark.skip("manual")
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
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
            },
            "params": {
                "hash_type": "sha256",
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
                "path": "/api/1/message/unbind_client",
                "method": "POST",
                "headers": {
                    "authorization": prepare['authorization'],
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
                },
                "params": {
                    "hash_type": "sha256",
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

        request.addfinalizer(fin)

    @pytest.fixture(scope='function', autouse=False)
    def prepare_message_id(self, env, prepare):
        inputs = {
            "host": prepare['host_app_in'],
            "path": "/api/1/in/message/notify",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
            },
            "params": {
                "hash_type": "sha256",
                "region": "cn",
                "lang": "zh-cn",
                "sign": "",
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
        response = hreq.request(env, inputs)
        with allure.step('校验response'):
            assert response.get("result_code") == 'success'
        message_id = response['data'].pop('message_id', '')
        time.sleep(1)
        return message_id

    def test_trace(self,env, prepare, prepare_bind, prepare_message_id):
        """
        查看消息发送状态
        http://showdoc.nevint.com/index.php?s=/13&page_id=876
        1:服务收到消息   2501:加入发送队列    5001:消息从服务端发出去往客户端    10000:收到客户端回应
        调用notify接口时，手机如果没在线，只有1，2501， 如果在线会返回1，2501，5001， 10000四个状态
        调用command接口时，CGW不在线，只返回1
        调用notify_hu接口时，CDC不在线，返回1，2501，CDC恢复在线，会增加5001，10000

        """

        inputs = {
            "host": prepare['host_app_in'],
            "path": "/api/1/in/message/trace",
            "method": "GET",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "app_id": "10000",
                'message_id': prepare_message_id,
                "hash_type": "sha256",
                "sign": "",
                'nonce': 'MrVIRwkCLBKySgCG'
            },
        }

        response = hreq.request(env, inputs)
        with allure.step('校验response'):
            assert response.get("result_code") == 'success'
        data = response.pop('data')
        assert_equal(len(data) > 0, True)