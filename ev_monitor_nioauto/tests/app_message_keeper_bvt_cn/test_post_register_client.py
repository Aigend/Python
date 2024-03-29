# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_post_register_client_to_c.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/15 5:40 下午
# @Description :
"""
    http://showdoc.nevint.com/index.php?s=/647&page_id=31092
    将消息标记为已读
    /api/2/in/message_keeper/tob/register_client
    Query Parameters：
        * app_id 服务ID
            * 必填
        * region 区域码
            * 必填
        * lang 语言
            * 必填
        * timestamp 时间戳
            * 必填
        * sign 签名
            * 必填
        * hash_type
    Body Parameters
        * target_app_id 用户ID
            * 必填
        * app_version
            * 必填
            * 有效的 9.50.1
            * 无效的 9.050.1
        * brand
        * device_token
        * device_type
            * 必填
            * IPhone,Samsung,Sony,HuaWei,XiaoMi
        * device_id
            * 必填
            * android_id,vehicle_id
        * os
            * 必填
            * android,ios,linux
        * os_version
            * 必填
            * 有效的 6.0.1
        * push_type
            * 非必填
            * mipush
            * apns
            * hwpush
        * push_version
            * 非必填,默认0

            10003	Android Staff APP
10018	Android Fellow APP
    """

import random
import string
import pytest
import allure
from utils.http_client import TSPRequest as hreq
from utils.assertions import assert_equal

register_client_keys = "case_name,target_app_id,host_key,data_key"
register_client_cases = [
    ("正案例_TOB_Android Staff APP 10003", "10003", 'app_tob_in', 'nmp_app_tob'),
    ("正案例_TOB_Android Fellow APP 10018", "10018", 'app_tob_in', 'nmp_app_tob'),
    ("正案例_TOC_IOS_NIO_APP 10002", "10002", 'app_in', 'nmp_app'),
    ("正案例_TOC_ANDROID_NIO_APP 10001", "10001", 'app_in', 'nmp_app'),
    ("反案例_TOC_非白名单app_id register_client 10000", "10000", 'app_in', 'nmp_app'),
    ("反案例_TOB_非白名单app_id register_client 10000", "10000", 'app_tob_in', 'nmp_app_tob'),
]
register_client_ids = [f"{case[0]}" for case in register_client_cases]


@pytest.mark.parametrize(register_client_keys, register_client_cases, ids=register_client_ids)
def test_register_client(env, mysql, case_name, target_app_id, host_key, data_key):
    app_id_client_info = {
        "10000": {
            "target_app_id": "10000",
            "app_version": "6.5.1",
            "brand": "IPhone",
            "device_type": "IOS",
            "device_token": "IPhone",
            "device_id": "".join(random.sample(string.ascii_letters, 13)),
            "os": "ios",
            "os_version": "8.5.1",
            "push_type": "apns",
            "push_version": 1,
        },
        "10002": {
            "target_app_id": "10002",
            "app_version": "6.5.1",
            "brand": "IPhone",
            "device_type": "IOS",
            "device_token": "IPhone",
            "device_id": "".join(random.sample(string.ascii_letters, 13)),
            "os": "ios",
            "os_version": "8.5.1",
            "push_type": "apns",
            "push_version": 1,
        },
        "10001": {
            "target_app_id": "10001",
            "app_version": "8.5.1",
            "brand": "Huawei",
            "device_type": "android",
            "device_token": "HuaWei_" + "".join(random.sample(string.ascii_letters, 13)),
            "device_id": "".join(random.sample(string.ascii_letters, 13)),
            "os": "android",
            "os_version": "6.5.1",
            "push_type": "hwpush",
            "push_version": 1
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
            "push_version": 1
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
            "push_version": 1
        },
        "100417": {
            "target_app_id": "100417",
            "app_version": "87.0.4280.88",
            "brand": "chrome",
            "device_type": "BROWSER",
            "device_token": "chrome_" + "".join(random.sample(string.ascii_letters, 13)),
            "device_id": "".join(random.sample(string.ascii_letters, 13)),
            "os": "macintel",
            "os_version": "10_15_7",
            "push_type": "web",
            "push_version": 1
        }
    }

    with allure.step(f'{host_key}服务注册client接口{case_name}'):
        host = env['host'][host_key]
        inputs = {
            "host": host,
            "path": "/api/2/in/message_keeper/register_client",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": target_app_id,
                'sign': ''
            },
            "data": app_id_client_info.get(str(target_app_id))
        }
        response = hreq.request(env, inputs)
        if case_name.startswith("正案例"):
            assert response["result_code"] == "success"
            client_id = response["data"]
            clients = mysql[data_key].fetch("clients", where_model={"client_id": client_id})
            assert len(clients) == 1
        else:
            except_res = {
                "result_code": "invalid_app_id",
                "debug_msg": "app id is not in white list"
            }
            response.pop("request_id")
            response.pop("server_time")
            assert_equal(except_res, response)
