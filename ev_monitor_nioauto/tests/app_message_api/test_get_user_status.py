#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    查询用户状态API，首先通过userId查找与其绑定的clientId然后根据clients表中该clientId的状态确定userId的状态。
    http://showdoc.nevint.com/index.php?s=/13&page_id=25097

    * 只要有一个是ONLINE就返回ONLINE

"""

import allure
import pytest
import random
import string
import time
from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq


class TestMeesageAPI(object):
    @pytest.fixture(scope='class', autouse=False)
    def prepare(self, env, ):
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
        # data['client_info'] = mysql['nmp_app'].fetch('clients', {'client_id': data['client_id_app'], 'app_id': data['app_id_phone']})[0]
        # data['app_version'] = data['client_info']['app_version']
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
        inputs = {
            "host": host,
            "method": "POST",
            "path": "/acc/2/login",
            "headers": {'content-type': 'application/x-www-form-urlencoded',
                        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
                        },
            "params": {
                'region': 'cn',
                'lang': 'zh-cn',
                'app_id': app_id,
                'nonce': int(time.time()),
                'sign': ""
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
        with allure.step(f"请求/acc/2/login接口：{inputs}"):
            response_dict = hreq.request(env, inputs)
        with allure.step(f"请求结果断言：{response_dict}"):
            assert response_dict['result_code'] == "success"
            assert response_dict['data']
        with allure.step(f"返回请求所需token：Bearer {response_dict['data']['access_token']}"):
            return f"Bearer {response_dict['data']['access_token']}"

    @pytest.fixture(scope="class", autouse=False)
    def prepare_bind(self, env, prepare, request, account_login):
        '''
        用户登陆|退出APP时，调用binding|unbinding 接口
        http://showdoc.nevint.com/index.php?s=/13&page_id=1071
        绑定和解绑客户端是针对用户而言的，每个用户可以绑定多个客户端，通过这样的机制能保证，推送给这个用户的时候，各个设备都可以收到相应的推送。同理，设备解绑之后将不再收到发送给此用户的信息。
        '''
        token = account_login
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/message/bind_client",
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

        response = hreq.request(env, inputs)
        assert_equal(response['result_code'], 'success')
        time.sleep(1)

        def fin():
            unbind_client_inputs = {
                "host": env['host']['app_in'],
                "path": "/api/1/message/unbind_client",
                "method": "POST",
                "headers": {
                    "authorization": token,
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
                },
                "params": {
                    "region": "cn",
                    "lang": "zh-cn",
                    "sign": "",
                    "app_id": prepare['app_id_phone']
                },
                "data": {
                    'client_id': prepare['client_id_app'],
                    'nonce': ''.join(random.sample(string.ascii_letters, 11))
                }
            }

            unbind_response = hreq.request(env, unbind_client_inputs)
            assert_equal(unbind_response['result_code'], 'success')

        request.addfinalizer(fin)

    def test_get_user_status(self, env, prepare):
        """
        查询用户状态API，首先通过userId查找与其绑定的clientId然后根据clients表中该clientId的状态确定userId的状态。
        只要有一个是ONLINE就返回ONLINE
        http://showdoc.nevint.com/index.php?s=/13&page_id=25097
        """
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/in/message/get_user_status",
            "method": "GET",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "app_id": prepare['app_id_phone'],
                "user_id": prepare['account_id'],
                "sign": "",
            }
        }

        response = hreq.request(env, inputs)
        assert response['result_code'] == 'success'
