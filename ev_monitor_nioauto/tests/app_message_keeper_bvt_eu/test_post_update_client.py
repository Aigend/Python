# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_post_update_client_to_c.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/15 5:40 下午
# @Description :
"""
    http://showdoc.nevint.com/index.php?s=/647&page_id=31092
    /api/2/in/message_keeper/tob/update_client
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
        * device_token
        * push_type
            * 非必填
            * mipush
            * apns
            * hwpush
        * push_version
            * 非必填,默认0
            *
        * client_id
    """

import random
import string
import pytest
import allure
from utils.http_client import TSPRequest as hreq

update_client_keys = "case_name,target_app_id,host_key,data_key"
update_client_cases = [
    ("正案例_TOB_泰坦WEB获取update_client_100417", "100417", 'app_tob_in', 'nmp_app_tob'),
    ("正案例_TOB_泰坦APP获取update_client_1000014", "1000014", 'app_tob_in', 'nmp_app_tob'),
    ("正案例_TOC_IOS_NIOAPP获取update_client_1000003", "1000003", 'app_in', 'nmp_app'),
    ("正案例_TOC_ANDROID_NIOAPP获取update_client_1000004", "1000004", 'app_in', 'nmp_app'),
    ("正案例_TOC_official_website官网WEB获取update_client_100404", "100404", 'app_in', 'nmp_app'),

]
update_client_ids = [f"{case[0]}" for case in update_client_cases]


@pytest.mark.parametrize(update_client_keys, update_client_cases, ids=update_client_ids)
def test_update_client(env, mysql, case_name, target_app_id, host_key, data_key):
    with allure.step(f'{host_key}服务更新client接口{case_name}'):
        app_id_client_info = {
            "1000003": {
                "target_app_id": "1000003",
                "app_version": "6.5.1",
                "device_token": "IPhone"+"".join(random.sample(string.ascii_letters, 13)),
                "push_type": "apns",
                "push_version": 1,
            },
            "1000004": {
                "target_app_id": "1000004",
                "app_version": "8.5.1",
                "device_token": "HuaWei_" + "".join(random.sample(string.ascii_letters, 13)),
                "push_type": "hwpush",
                "push_version": 1
            },
            "100404": {
                "target_app_id": "100404",
                "app_version": "8.5.1",
                "device_token": "chrome_" + "".join(random.sample(string.ascii_letters, 13)),
                "push_type": "web",
                "push_version": 1
            },
            "1000014": {
                "target_app_id": "1000014",
                "app_version": "0.0.40",
                "device_token": "oppo_" + "".join(random.sample(string.ascii_letters, 13)),
                "push_type": "mipush",
                "push_version": 1
            },
            "100417": {
                "target_app_id": "100417",
                "app_version": "87.0.4280.88",
                "device_token": "chrome_" + "".join(random.sample(string.ascii_letters, 13)),
                "push_type": "web",
                "push_version": 1
            }
        }
        client_id = env["app_message_keeper"][data_key][int(target_app_id)]["user1"]["update_client_id"]
        host = env['host'][host_key]
        update_data = app_id_client_info.get(str(target_app_id))
        update_data["client_id"] = client_id
        device_token = app_id_client_info.get(str(target_app_id)).get("device_token")
        inputs = {
            "host": host,
            "path": "/api/2/in/message_keeper/update_client",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": 10000,
                'sign': ''
            },
            "data": app_id_client_info.get(str(target_app_id))
        }
        response = hreq.request(env, inputs)
        assert response["result_code"] == "success"
    with allure.step(f'{data_key}校验数据库中数据已更新'):
        clients = mysql[data_key].fetch("clients", where_model={"client_id": client_id}, fields=["device_token"])
        assert device_token == clients[0]['device_token']
