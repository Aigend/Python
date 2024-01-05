# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_bind_unbind.py
# @Author : qiangwei.zhang
# @time: 2021/10/20
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import pytest
import allure
import random
import string
from utils.http_client import TSPRequest as hreq
from utils.assertions import assert_equal

app_id = 10001
register_path = '/api/1/message/register_client'
bind_path = '/api/1/message/bind_client'
unbind_path = '/api/1/message/unbind_client'
update_path = '/api/1/message/update_client'

app_id_client_info = {
    "hwpush": {
        "target_app_id": "10001",
        "app_version": "8.5.1",
        "brand": "Huawei",
        "device_type": "android",
        "device_token": "HuaWei_" + "".join(random.sample(string.ascii_letters, 13)),
        "device_id": "".join(random.sample(string.ascii_letters, 13)),
        "os": "android",
        "os_version": "6.5.1",
        "push_type": "hwpush",
        "nonce": ''.join(random.choices(string.digits + string.ascii_lowercase, k=16)),
        "push_version": 1
    },
    "oppo": {
        "target_app_id": "10001",
        "app_version": "8.5.1",
        "brand": "oppo",
        "device_type": "android",
        "device_token": "HuaWei_" + "".join(random.sample(string.ascii_letters, 13)),
        "device_id": "".join(random.sample(string.ascii_letters, 13)),
        "os": "android",
        "os_version": "6.5.1",
        "push_type": "oppo",
        "nonce": ''.join(random.choices(string.digits + string.ascii_lowercase, k=16)),
        "push_version": 1
    },
    "vivo": {
        "target_app_id": "10001",
        "app_version": "8.5.1",
        "brand": "vivo",
        "device_type": "android",
        "device_token": "HuaWei_" + "".join(random.sample(string.ascii_letters, 13)),
        "device_id": "".join(random.sample(string.ascii_letters, 13)),
        "os": "android",
        "os_version": "6.5.1",
        "nonce": ''.join(random.choices(string.digits + string.ascii_lowercase, k=16)),
        "push_type": "vivo",
        "push_version": 1
    },
    "mipush": {
        "target_app_id": "10001",
        "app_version": "8.5.1",
        "brand": "MI",
        "device_type": "android",
        "device_token": "HuaWei_" + "".join(random.sample(string.ascii_letters, 13)),
        "device_id": "".join(random.sample(string.ascii_letters, 13)),
        "os": "android",
        "os_version": "6.5.1",
        "nonce": ''.join(random.choices(string.digits + string.ascii_lowercase, k=16)),
        "push_type": "mipush",
        "push_version": 1
    },
    "not_exist": {
        "target_app_id": "10001",
        "app_version": "8.5.1",
        "brand": "MI",
        "device_type": "android",
        "device_token": "HuaWei_" + "".join(random.sample(string.ascii_letters, 13)),
        "device_id": "".join(random.sample(string.ascii_letters, 13)),
        "os": "android",
        "os_version": "6.5.1",
        "nonce": ''.join(random.choices(string.digits + string.ascii_lowercase, k=16)),
        "push_type": "not_exist",
        "push_version": 1
    },
    "default": {
        "target_app_id": "10001",
        "app_version": "8.5.1",
        "brand": "not_exist",
        "device_type": "android",
        "device_token": "HuaWei_" + "".join(random.sample(string.ascii_letters, 13)),
        "device_id": "".join(random.sample(string.ascii_letters, 13)),
        "os": "android",
        "nonce": ''.join(random.choices(string.digits + string.ascii_lowercase, k=16)),
        "os_version": "6.5.1",
        "push_version": 1
    },
    "apns": {
        "app_version": "4.14.5",
        "brand": "iPhone 7",
        "device_type": "IOS",
        "device_token": 'Iphone_' + ''.join(random.choices(string.digits, k=13)),
        "device_id": ''.join(random.choices(string.digits, k=13)),
        "os": "IOS",
        "os_version": "15.1",
        "nonce": ''.join(random.choices(string.digits + string.ascii_lowercase, k=16)),
        "push_type": "apns",
        "push_ver": 1
    }
}

bind_client_keys = "case_name,app_id,brand"
bind_client_cases = [
    ("android绑定client", "10001", "hwpush"),
    ("android绑定client", "10001", "oppo"),
    ("android绑定client", "10001", "vivo"),
    ("android绑定client", "10001", "mipush"),
    ("ios绑定client", "10002", "apns"),
]
bind_client_ids = [f"{case[0]}_{case[1]}_{case[2]}" for case in bind_client_cases]


@pytest.mark.parametrize(bind_client_keys, bind_client_cases, ids=bind_client_ids)
def test_register_bind_unbind_client(env, mysql, case_name, app_id, brand):
    client_id = env["notify"][brand]["client_id"]
    account_id = env["notify"][brand]["account_id"]
    mobile = env["notify"][brand]["phone_number"]
    vc_code = env["notify"][brand]["vc_code"]
    host = env['host']['app_ex']
    # with allure.step(f'api服务注册client接口{case_name}'):
    #     inputs = {
    #         "host": host,
    #         "path": register_path,
    #         "method": "POST",
    #         "headers": {"Content-Type": "application/x-www-form-urlencoded"},
    #         "params": {
    #             "region": "cn",
    #             "lang": "zh-cn",
    #             "hash_type": "sha256",
    #             "app_id": "10001",
    #             'sign': ''
    #         },
    #         "data": app_id_client_info.get(str(brand))
    #     }
    #     response = hreq.request(env, inputs)
    #     assert response["result_code"] == "success"
    #     client_id = response.get("data").get("client_id")
    with allure.step('取得access_token'):
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
                'nonce': ''.join(random.choices(string.digits + string.ascii_lowercase, k=16)),
                'sign': ''
            },
            "data": {
                'mobile': mobile,
                'verification_code': vc_code,
                'country_code': '86',
                'authentication_type': 'mobile_verification_code',
                'device_id': app_id,
                "terminal": '{"name":"我的华为手机","model":"HUAWEI P10"}',
            },
        }
        response = hreq.request(env, inputs)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
        access_token = response['data']['access_token']
        print(access_token)
    with allure.step(f'{case_name}Bind {client_id} to {account_id}'):
        inputs = {
            "host": host,
            "path": bind_path,
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded", "Authorization": access_token},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                'sign': ''
            },
            "data": {"client_id": client_id,
                     "account_id": account_id,
                     "nonce": ''.join(random.choices(string.digits + string.ascii_lowercase, k=16))}
        }
        response = hreq.request(env, inputs)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
    with allure.step(f'Unbind {client_id} from {account_id}'):
        inputs = {
            "host": env['host']['app_in'],
            "path": unbind_path,
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded", "Authorization": access_token},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                'sign': ''
            },
            "data": {"client_id": client_id}
        }
        response = hreq.request(env, inputs)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
    if env['cmdopt'] == 'test':
        with allure.step('校验bindings库中visible为0'):
            record = mysql['nmp_app'].fetch_one('bindings', {'client_id': client_id})
            assert_equal(record['visible'], 0)
