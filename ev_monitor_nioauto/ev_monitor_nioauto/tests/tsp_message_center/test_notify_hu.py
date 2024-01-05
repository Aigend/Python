# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_notify_hu.py
# @Author : qiangwei.zhang
# @time: 2022/04/06
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:li.liu2
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    推送信息到CDC，例如手机发送导航到CDC
    接口文档：http://showdoc.nevint.com/index.php?s=/13&page_id=60
    数据准备：
        * 需要先bind client
        * 支持按照Client ID／Device ID 进行推送。
        * 支持消息分类
        * 支持只记录历史，不推送的功能。或者只推送，不记录历史的功能。
        * 支持推送到HU 特定App 的功能。
        * CDC如果不在线，则state 只有1，2501。 app消息平台监测到在CDC在线后，会把信息推送到CDC，此时状态增加5001，10001
    车机app版本限制：
    'include_app_versions': json.dumps({"more_than": 1, "less_than": 11, "equal": 100}),
    'app_package_name': 'com.nio.nomi',
    校验点：
        * 限制包名为com.nio.nomi的app版本大于等于 1 <= V < 11或者V = 100
        * app_package_name和include_app_versions未非必填字段，只有两个都填写才能生效
        * more_than less_than大于0
        * 版本号为整数
    查询版本接口：infortainment_fundamental_test库cdc_app_version表，数据来源fota app更新，如果无版本会返回 -1
    测试案例：
        # 1.app_version在范围内, 不等于某个值
        # 2.app_version不在范围内，等于某个值
        # 3.app_version不在范围内
        # 4.不限制版本情况，只传app_package_name，
        # 5.不限制版本情况，只传include_app_versions，
        # 6.两个都不传（不校验版本）
        # 7.app_version在范围内，more_than等于app_version
        # 8.app_version不在范围内，less_than等于app_version
"""
import json
import math
import time
import random
import allure
import pytest

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq

path = "/api/1/in/message/notify_hu"


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

    @pytest.fixture(scope='class', autouse=False)
    def prepare_app_version(self, env):
        user = 'nmp'
        package_name = 'com.nio.nomi'
        http_app_version = {
            "host": env["host"]["tsp_in"],
            "path": "/api/1/in/infotainment/nomi/config/get_app_version",
            "method": "GET",
            "params": {"vehicle_id": env['vehicles'][user]['vehicle_id'],
                       "package_name": package_name,
                       "hash_type": 'md5',
                       "sign": '',
                       'app_id': '10001'}
        }
        response_app = hreq.request(env, http_app_version)
        real_version = int(response_app['data'])
        return package_name, real_version

    def test_notify_hu_app_version_limit_case(self, env):
        case_name = '1.在范围内, 不等于某个值'
        user = 'nmp'
        except_value = 'success'
        vid = env['vehicles'][user]['vehicle_id']
        account_id = env['vehicles'][user]['account_id']
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/in/message/notify_hu",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "region": "cn",
                "hash_type": "sha256",
                "sign": "",
                "lang": "zh-cn",
                "app_id": "10000"
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCG',
                'async': False,
                'ttl': 100000,
                'target_app_ids': '30010',
                # 'target_app_ids': '30007',
                'do_push': True,
                'device_ids': vid,
                'scenario': 'hu_poi',
                'payload': json.dumps(
                    {
                        "user_id": account_id,
                        "data": json.dumps(
                            {
                                "type": "poi",
                                "source": "nioapp",
                                "longitude": 116.465546,
                                "latitude": 40.02179,
                                "city": "北京市",
                                "region": "朝阳区",
                                "name": "望京诚盈中心",
                                "address": "朝阳区望京广顺北大街与来广营西路交汇处"
                            }, ensure_ascii=False)
                    }, ensure_ascii=False)
            },
        }
        with allure.step(f"请求{inputs['path']}接口{case_name}"):
            response = hreq.request(env, inputs)
            assert_equal(except_value, response['data']['details'][0]['result'])

    def test_notify_hu_app_version_limit_case1(self, env, prepare_app_version):
        case_name = '1.在范围内, 不等于某个值'
        package_name, real_version = prepare_app_version
        user = 'nmp'

        except_value = 'success'
        vid = env['vehicles'][user]['vehicle_id']
        account_id = env['vehicles'][user]['account_id']
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/in/message/notify_hu",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "region": "cn",
                "hash_type": "md5",
                "sign": "",
                "lang": "zh-cn",
                "app_id": "80001"
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCG',
                'async': False,
                'ttl': 100000,
                'target_app_ids': '30010',
                'do_push': True,
                'device_ids': vid,
                'scenario': 'hu_poi',
                'include_app_versions': json.dumps({"more_than": random.randint(real_version - math.floor(real_version / 2), real_version - math.floor(real_version / 3)),
                                                    "less_than": random.randint(real_version + math.ceil(real_version / 3), real_version + math.ceil(real_version / 2)),
                                                    "equal": real_version + 1}),
                'app_package_name': package_name,
                'payload': json.dumps({"user_id": account_id,
                                       "data": json.dumps(
                                           {"type": "poi", "source": "nioapp", "longitude": 116.465546, "latitude": 40.02179, "city": "北京市", "region": "朝阳区", "name": "望京诚盈中心",
                                            "address": "朝阳区望京广顺北大街与来广营西路交汇处"}, ensure_ascii=False)}),
            },
        }
        with allure.step(f"请求{inputs['path']}接口{case_name}"):
            response = hreq.request(env, inputs)
            assert_equal(except_value, response['data']['details'][0]['result'])
        # 校验 todo 增加message_state校验

        """可以让cdc在线，校验有没有收到信息，例如：
        2020-08-06 15:37:54,024 [mqtt.py:294] DEBUG: pkg_name:com.nio.nomi
        2020-08-06 15:37:54,025 [mqtt.py:294] DEBUG: data:{"type":"poi","source":"nioapp","longitude":116.465546,"latitude":40.02179,"city":"北京市","region":"朝阳区","name":"望京诚盈中心","a朝阳区望京广顺北大街与来广营西路交汇处"}
        2020-08-06 15:37:54,025 [mqtt.py:294] DEBUG: user_id:212409581
        {"more_than":1002002,"less_than":1003002,"equal":1003003}
        """

    def test_notify_hu_app_version_limit_case2(self, env, prepare_app_version):
        case_name = '2.不在范围内，等于某个值'
        except_value = 'success'
        package_name, real_version = prepare_app_version
        user = 'nmp'
        vid = env['vehicles'][user]['vehicle_id']
        account_id = env['vehicles'][user]['account_id']
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/in/message/notify_hu",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "region": "cn",
                "hash_type": "md5",
                "sign": "",
                "lang": "zh-cn",
                "app_id": "80001"
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCG',
                'async': False,
                'ttl': 100000,
                'target_app_ids': '30010',
                'do_push': True,
                'device_ids': vid,
                'scenario': 'hu_poi',
                'include_app_versions': json.dumps({"more_than": random.randint(real_version + math.ceil(real_version / 5), real_version + math.ceil(real_version / 4)),
                                                    "less_than": random.randint(real_version + math.ceil(real_version / 3), real_version + math.ceil(real_version / 2)),
                                                    "equal": real_version}),
                'app_package_name': package_name,
                'payload': json.dumps({"user_id": account_id,
                                       "data": json.dumps(
                                           {"type": "poi", "source": "nioapp", "longitude": 116.465546, "latitude": 40.02179, "city": "北京市", "region": "朝阳区", "name": "望京诚盈中心",
                                            "address": "朝阳区望京广顺北大街与来广营西路交汇处"}, ensure_ascii=False)}),
            },
        }

        with allure.step(f"请求{inputs['path']}接口{case_name}"):
            response = hreq.request(env, inputs)
            assert_equal(except_value, response['data']['details'][0]['result'])
        # 校验

    def test_notify_hu_app_version_limit_case3(self, env, prepare_app_version):
        case_name = '3.不在范围内'
        except_value = 'app_version_not_match'
        package_name, real_version = prepare_app_version
        user = 'nmp'
        vid = env['vehicles'][user]['vehicle_id']
        account_id = env['vehicles'][user]['account_id']
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/in/message/notify_hu",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "region": "cn",
                "hash_type": "md5",
                "sign": "",
                "lang": "zh-cn",
                "app_id": "80001"
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCG',
                'async': False,
                'ttl': 100000,
                'target_app_ids': '30010',
                'do_push': True,
                'device_ids': vid,
                'scenario': 'hu_poi',
                'include_app_versions': json.dumps({"more_than": random.randint(real_version + math.ceil(real_version / 5), real_version + math.ceil(real_version / 4)),
                                                    "less_than": random.randint(real_version + math.ceil(real_version / 3), real_version + math.ceil(real_version / 2)),
                                                    "equal": real_version + 1}),
                'app_package_name': package_name,
                'payload': json.dumps({"user_id": account_id,
                                       "data": json.dumps(
                                           {"type": "poi", "source": "nioapp", "longitude": 116.465546, "latitude": 40.02179, "city": "北京市", "region": "朝阳区", "name": "望京诚盈中心",
                                            "address": "朝阳区望京广顺北大街与来广营西路交汇处"}, ensure_ascii=False)}),
            },
        }

        with allure.step(f"请求{inputs['path']}接口{case_name}"):
            response = hreq.request(env, inputs)
            assert_equal(except_value, response['data']['details'][0]['result'])

    def test_notify_hu_app_version_limit_case4(self, env, prepare_app_version):
        case_name = '4.不限制版本情况，只传app_package_name'
        except_value = 'success'
        package_name, real_version = prepare_app_version
        user = 'nmp'
        vid = env['vehicles'][user]['vehicle_id']
        account_id = env['vehicles'][user]['account_id']
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/in/message/notify_hu",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "md5",
                "sign": "",
                "app_id": "80001"
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCG',
                'async': False,
                'ttl': 100000,
                'target_app_ids': '30010',
                'do_push': True,
                'device_ids': vid,
                'scenario': 'hu_poi',
                'app_package_name': package_name,
                'payload': json.dumps({"user_id": account_id,
                                       "data": json.dumps(
                                           {"type": "poi", "source": "nioapp", "longitude": 116.465546, "latitude": 40.02179, "city": "北京市", "region": "朝阳区", "name": "望京诚盈中心",
                                            "address": "朝阳区望京广顺北大街与来广营西路交汇处"}, ensure_ascii=False)}),
            },
        }

        with allure.step(f"请求{inputs['path']}接口{case_name}"):
            response = hreq.request(env, inputs)
            assert_equal(except_value, response['data']['details'][0]['result'])

    def test_notify_hu_app_version_limit_case5(self, env, prepare_app_version):
        case_name = '5.不限制版本情况，只传include_app_versions'
        except_value = 'success'
        package_name, real_version = prepare_app_version
        user = 'nmp'
        vid = env['vehicles'][user]['vehicle_id']
        account_id = env['vehicles'][user]['account_id']
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/in/message/notify_hu",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "md5",
                "sign": "",
                "app_id": "80001"
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCG',
                'async': False,
                'ttl': 100000,
                'target_app_ids': '30010',
                'do_push': True,
                'device_ids': vid,
                'scenario': 'hu_poi',
                'include_app_versions': json.dumps({"more_than": random.randint(real_version + math.ceil(real_version / 5), real_version + math.ceil(real_version / 4)),
                                                    "less_than": random.randint(real_version + math.ceil(real_version / 3), real_version + math.ceil(real_version / 2)),
                                                    "equal": real_version}),
                'payload': json.dumps({"user_id": account_id,
                                       "data": json.dumps(
                                           {"type": "poi", "source": "nioapp", "longitude": 116.465546, "latitude": 40.02179, "city": "北京市", "region": "朝阳区", "name": "望京诚盈中心",
                                            "address": "朝阳区望京广顺北大街与来广营西路交汇处"}, ensure_ascii=False)}),
            },
        }

        with allure.step(f"请求{inputs['path']}接口{case_name}"):
            response = hreq.request(env, inputs)
            assert_equal(except_value, response['data']['details'][0]['result'])

    def test_notify_hu_app_version_limit_case6(self, env, prepare_app_version):
        case_name = '6.两个都不传（不校验版本）'
        except_value = 'success'
        package_name, real_version = prepare_app_version
        user = 'nmp'
        vid = env['vehicles'][user]['vehicle_id']
        account_id = env['vehicles'][user]['account_id']
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/in/message/notify_hu",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "md5",
                "sign": "",
                "app_id": "80001"
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCG',
                'async': False,
                'ttl': 100000,
                'target_app_ids': '30010',
                'do_push': True,
                'device_ids': vid,
                'scenario': 'hu_poi',
                'payload': json.dumps({"user_id": account_id,
                                       "data": json.dumps(
                                           {"type": "poi", "source": "nioapp", "longitude": 116.465546, "latitude": 40.02179, "city": "北京市", "region": "朝阳区", "name": "望京诚盈中心",
                                            "address": "朝阳区望京广顺北大街与来广营西路交汇处"}, ensure_ascii=False)}),
            },
        }

        with allure.step(f"请求{inputs['path']}接口{case_name}"):
            response = hreq.request(env, inputs)
            assert_equal(except_value, response['data']['details'][0]['result'])

    def test_notify_hu_app_version_limit_case7(self, env, prepare_app_version):
        case_name = '7.在范围内，more_than等于app_version'
        except_value = 'success'
        package_name, real_version = prepare_app_version
        user = 'nmp'
        vid = env['vehicles'][user]['vehicle_id']
        account_id = env['vehicles'][user]['account_id']
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/in/message/notify_hu",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "md5",
                "sign": "",
                "app_id": "80001"
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCG',
                'async': False,
                'ttl': 100000,
                'target_app_ids': '30010',
                'do_push': True,
                'device_ids': vid,
                'scenario': 'hu_poi',
                'include_app_versions': json.dumps({"more_than": real_version,
                                                    "less_than": random.randint(real_version + math.ceil(real_version / 3), real_version + math.ceil(real_version / 2)),
                                                    "equal": real_version}),
                'app_package_name': package_name,
                'payload': json.dumps({"user_id": account_id,
                                       "data": json.dumps(
                                           {"type": "poi", "source": "nioapp", "longitude": 116.465546, "latitude": 40.02179, "city": "北京市", "region": "朝阳区", "name": "望京诚盈中心",
                                            "address": "朝阳区望京广顺北大街与来广营西路交汇处"}, ensure_ascii=False)}),
            },
        }

        with allure.step(f"请求{inputs['path']}接口{case_name}"):
            response = hreq.request(env, inputs)
            assert_equal(except_value, response['data']['details'][0]['result'])

    def test_notify_hu_app_version_limit_case8(self, env, prepare_app_version):
        case_name = '8.不在范围内，less_than等于app_version'
        except_value = 'app_version_not_match'
        package_name, real_version = prepare_app_version
        user = 'nmp'
        vid = env['vehicles'][user]['vehicle_id']
        account_id = env['vehicles'][user]['account_id']
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/in/message/notify_hu",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "md5",
                "sign": "",
                "app_id": "80001"
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCG',
                'async': False,
                'ttl': 100000,
                'target_app_ids': '30010',
                'do_push': True,
                'device_ids': vid,
                'scenario': 'hu_poi',
                'include_app_versions': json.dumps({"more_than": math.floor(real_version / 2),
                                                    "less_than": real_version, "equal": real_version + 1}),
                'app_package_name': package_name,
                'payload': json.dumps({"user_id": account_id,
                                       "data": json.dumps(
                                           {"type": "poi", "source": "nioapp", "longitude": 116.465546, "latitude": 40.02179, "city": "北京市", "region": "朝阳区", "name": "望京诚盈中心",
                                            "address": "朝阳区望京广顺北大街与来广营西路交汇处"}, ensure_ascii=False)}),
            },
        }

        with allure.step(f"请求{inputs['path']}接口{case_name}"):
            response = hreq.request(env, inputs)
            assert_equal(except_value, response['data']['details'][0]['result'])

    def test_notify_hu_app_version_limit_case9(self, env):
        case_name = '不加版本限制'
        user = 'nmp'
        except_value = 'success'
        vid = env['vehicles'][user]['vehicle_id']
        account_id = env['vehicles'][user]['account_id']
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/in/message/notify_hu",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "region": "cn",
                "sign": "",
                "lang": "zh-cn",
                "app_id": "80001"
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCG',
                'async': False,
                'ttl': 100000,
                'target_app_ids': '30010',
                'do_push': True,
                'device_ids': vid,
                'scenario': 'hu_poi',
                # 'app_package_name': package_name,
                'payload': json.dumps({"user_id": account_id,
                                       "data": json.dumps(
                                           {"type": "poi", "source": "nioapp", "longitude": 116.465546, "latitude": 40.02179, "city": "北京市", "region": "朝阳区", "name": "望京诚盈中心",
                                            "address": "朝阳区望京广顺北大街与来广营西路交汇处"}, ensure_ascii=False)}),
            },
        }
        with allure.step(f"请求{inputs['path']}接口{case_name}"):
            response = hreq.request(env, inputs)
            assert_equal(except_value, response['data']['details'][0]['result'])


def generate_app_version(real_version=1000, package_name='com.nio.nomi'):
    # 1.在范围内, 不等于某个值
    # 2.不在范围内，等于某个值
    # 3.不在范围内
    # 4.不限制版本情况，只传app_package_name，
    # 5.不限制版本情况，只传include_app_versions，
    # 6.两个都不传（不校验版本）
    real_version = 0 if real_version < 0 else real_version

    data = [{"case_name": "1.在范围内, 不等于某个值",
             'include_app_versions': json.dumps({"more_than": random.randint(real_version - math.floor(real_version / 2), real_version - math.floor(real_version / 3)),
                                                 "less_than": random.randint(real_version + math.ceil(real_version / 3), real_version + math.ceil(real_version / 2)),
                                                 "equal": real_version + 1}),
             'app_package_name': package_name,
             "except": "success"},
            {"case_name": "2.不在范围内，等于某个值",
             'include_app_versions': json.dumps({"more_than": random.randint(real_version + math.ceil(real_version / 5), real_version + math.ceil(real_version / 4)),
                                                 "less_than": random.randint(real_version + math.ceil(real_version / 3), real_version + math.ceil(real_version / 2)),
                                                 "equal": real_version}),
             'app_package_name': package_name,
             "except": "success"},
            {"case_name": "3.不在范围内",
             'include_app_versions': json.dumps({"more_than": random.randint(real_version + math.ceil(real_version / 5), real_version + math.ceil(real_version / 4)),
                                                 "less_than": random.randint(real_version + math.ceil(real_version / 3), real_version + math.ceil(real_version / 2)),
                                                 "equal": real_version + 1}),
             'app_package_name': package_name,
             "except": "app_version_not_match1"},
            {"case_name": "4.不限制版本情况，只传app_package_name",
             'app_package_name': package_name,
             "except": "success"},
            {"case_name": "5.不限制版本情况，只传include_app_versions",
             'include_app_versions': json.dumps({"more_than": random.randint(real_version - math.ceil(real_version / 3), real_version - math.ceil(real_version / 4)),
                                                 "less_than": random.randint(real_version + math.floor(real_version / 2), real_version * 2), "equal": real_version}),
             "except": "success"},
            {"case_name": "6.两个都不传（不校验版本）",
             "except": "success"},
            {"case_name": "7.在范围内，more_than等于app_version",
             'include_app_versions': json.dumps({"more_than": real_version,
                                                 "less_than": random.randint(real_version + math.ceil(real_version / 3), real_version + math.ceil(real_version / 2)),
                                                 "equal": real_version}),
             'app_package_name': package_name,
             "except": "success"},
            {"case_name": "8.不在范围内，less_than等于app_version",
             'include_app_versions': json.dumps({"more_than": math.floor(real_version / 2),
                                                 "less_than": real_version, "equal": real_version}),
             'app_package_name': package_name,
             "except": "success"},
            ]
    return data
