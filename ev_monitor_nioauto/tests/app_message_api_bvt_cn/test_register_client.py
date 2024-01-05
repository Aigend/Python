# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_register_client.py
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

register_path = '/api/1/message/register_client'
bind_path = '/api/1/message/bind_client'
unbind_path = '/api/1/message/unbind_client'
update_path = '/api/1/message/update_client'

register_client_keys = "case_name,app_id"
register_client_cases = [
    ("android_10001注册client", "10001"),
    ("ios_10002注册client", "10002"),
    ("vid_30007注册client", "30007"),
]
register_client_ids = [f"{case[0]}" for case in register_client_cases]


@pytest.mark.parametrize(register_client_keys, register_client_cases, ids=register_client_ids)
def test_register_client(env, cmdopt, mysql, case_name, app_id):
    client_data = {
        "10001": {
            "app_version": "8.5.1",
            "brand": "Huawei",
            "device_type": "android",
            "device_token": 'HuaWei_' + ''.join(random.choices(string.digits, k=13)),
            "device_id": ''.join(random.choices(string.digits, k=13)),
            "os": "android",
            "os_version": "6.0.1",
            "nonce": ''.join(random.choices(string.digits + string.ascii_lowercase, k=16)),
            "push_type": "hwpush",
            "push_ver": 1
        },
        "30007": {
            "app_version": "8.5.1",
            "brand": "Huawei",
            "device_type": "android",
            # "device_token": 'HuaWei_' + ''.join(random.choices(string.digits, k=13)),
            "device_id": 'ghdfhjsherwewewekvhvhs',
            "os": "android",
            "os_version": "6.0.1",
            "nonce": ''.join(random.choices(string.digits + string.ascii_lowercase, k=16)),
            "push_type": "hwpush",
            "push_ver": 1
        },
        "10002": {
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
        },
        "10003": {
            "target_app_id": "10003",
            "app_version": "8.5.1",
            "brand": "Huawei",
            "device_type": "android",
            "device_token": "HuaWei_" + "".join(random.sample(string.ascii_letters, 13)),
            "device_id": "".join(random.sample(string.ascii_letters, 13)),
            "os": "android",
            "os_version": "6.5.1",
            "push_type": "hwpush",
            "push_version": 1,
            "nonce": ''.join(random.choices(string.digits + string.ascii_lowercase, k=16)),
            "push_ver": 1
        },
        "10018": {
            "target_app_id": "10018",
            "app_version": "0.0.40",
            "brand": "oppo",
            "device_type": "ANDROID",
            "device_token": "oppo_" + "".join(random.sample(string.ascii_letters, 13)),
            "device_id": "".join(random.sample(string.ascii_letters, 13)),
            "os": "android",
            "os_version": "9",
            "push_type": "mipush",
            "push_version": 1,
            "nonce": ''.join(random.choices(string.digits + string.ascii_lowercase, k=16)),
            "push_ver": 1
        },
    }
    with allure.step(f'{case_name}'):
        inputs = {
            "host": env['host']['app_in'],
            "path": register_path,
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                'sign': ''
            },
            "data": client_data.get(app_id)
        }
        response = hreq.request(env, inputs)
    with allure.step('校验response'):
        assert_equal(response['result_code'], 'success')
        client_id = response['data']['client_id']
    # if cmdopt == 'test':
    #     with allure.step('删除device记录'):
    #         mysql['nmp_app'].delete('clients', {'client_id': client_id})
    #         mysql['nmp_app'].delete('bindings', {'client_id': client_id})
