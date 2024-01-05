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

bind_client_keys = "case_name,app_id"
bind_client_cases = [
    ("android绑定client", "10001"),
    ("ios绑定client", "10002"),
]
bind_client_ids = [f"{case[0]}" for case in bind_client_cases]


@pytest.mark.parametrize(bind_client_keys, bind_client_cases, ids=bind_client_ids)
def test_bind_unbind(env, mysql, case_name, app_id):
    account_id = env["app_message_keeper"]["nmp_app"][int(app_id)]["user1"]["account_id"]
    client_id = env["app_message_keeper"]["nmp_app"][int(app_id)]["user1"]["bind_client_id"]
    mobile = env["app_message_keeper"]["nmp_app"][int(app_id)]["user1"]["mobile"]
    vc_code = env["app_message_keeper"]["nmp_app"][int(app_id)]["user1"]["vc_code"]
    host = env['host']['app_in']
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
        with allure.step('校验bindings库中visible为1'):
            record = mysql['nmp_app'].fetch_one('bindings', {'client_id': client_id})
            assert_equal(record['visible'], 0)
