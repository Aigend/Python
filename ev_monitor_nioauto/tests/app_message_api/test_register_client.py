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
        }
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


register_client_10001_keys = "case_name,brand,host_key,data_key"
register_client_10001_cases = [
    ("正案例_TOC_ANDROID_NIO_APP 10001", "hwpush", 'app_in', 'nmp_app'),
    ("正案例_TOC_ANDROID_NIO_APP 10001", "oppo", 'app_in', 'nmp_app'),
    ("正案例_TOC_ANDROID_NIO_APP 10001", "vivo", 'app_in', 'nmp_app'),
    ("正案例_TOC_ANDROID_NIO_APP 10001", "mipush", 'app_in', 'nmp_app'),
    ("正案例_TOC_ANDROID_NIO_APP 10001", "default", 'app_in', 'nmp_app'),
    ("反案例_TOC_ANDROID_NIO_APP 10001", "not_exist", 'app_in', 'nmp_app'),
]
register_client_10001_ids = [f"{case[0]} {case[1]}" for case in register_client_10001_cases]


@pytest.mark.parametrize(register_client_10001_keys, register_client_10001_cases, ids=register_client_10001_ids)
def test_register_client_10001(env, mysql, case_name, brand, host_key, data_key):
    """
    ALL(0),
    MIPUSH(1),
    JPUSH(2),
    APNS(3),
    MQTT(4),
    HWPUSH(5),
    EMAIL(6),
    FCMPUSH(7),
    WEBPUSH(8),
    OPPO(9),
    VIVO(10);
    """
    push_type_dict = {
        "mipush": 1,
        "default": 1,
        "vivo": 10,
        "oppo": 9,
        "not_exist": -1,
        "hwpush": 5,
    }

    app_id_client_info = {
        "hwpush": {
            # "target_app_id": "10001",
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
            # "target_app_id": "10001",
            "app_version": "8.5.1",
            "brand": "not_exist",
            "device_type": "android",
            "device_token": "HuaWei_" + "".join(random.sample(string.ascii_letters, 13)),
            "device_id": "".join(random.sample(string.ascii_letters, 13)),
            "os": "android",
            "nonce": ''.join(random.choices(string.digits + string.ascii_lowercase, k=16)),
            "os_version": "6.5.1",
            "push_version": 1
        }
    }

    with allure.step(f'{host_key}服务注册client接口{case_name}'):
        host = env['host'][host_key]
        inputs = {
            "host": host,
            "path": register_path,
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": "10001",
                'sign': ''
            },
            "data": app_id_client_info.get(str(brand))
        }
        response = hreq.request(env, inputs)
        if case_name.startswith("正案例"):
            assert response["result_code"] == "success"
            client_id = response.get("data").get("client_id")
            clients = mysql[data_key].fetch("clients", where_model={"client_id": client_id})
            assert len(clients) == 1
            assert int(clients[0].get("push_type")) == int(push_type_dict.get(brand))
        else:
            except_res = {
                "result_code": "invalid_param",
                "debug_msg": "invalid push type"
            }
            response.pop("request_id")
            response.pop("server_time")
            assert_equal(except_res, response)
