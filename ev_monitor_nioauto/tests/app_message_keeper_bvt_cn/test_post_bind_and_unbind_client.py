# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_post_bind_client_to_c.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/15 5:40 下午
# @Description :
"""
    http://showdoc.nevint.com/index.php?s=/647&page_id=31094
    /api/2/in/message_keeper/bind_client
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
        * client_id
        * account_id
    """

import random
import string
import pytest
import allure
from utils.http_client import TSPRequest as hreq
from utils.logger import logger

bind_client_keys = "case_name,target_app_id,host_key,data_key"
bind_client_cases = [
    # ("正案例_TOB_Android Staff APP 10003", "10003", 'app_tob_in', 'nmp_app_tob'),
    # ("正案例_TOB_Android Fellow APP 10018", "10018", 'app_tob_in', 'nmp_app_tob'),
    # ("正案例_TOC_IOS_NIO_APP 10002", "10002", 'app_in', 'nmp_app'),
    ("正案例_TOC_ANDROID_NIO_APP 10001", "10001", 'app_in', 'nmp_app'),

]
bind_client_ids = [f"{case[0]}" for case in bind_client_cases]


@pytest.mark.parametrize(bind_client_keys, bind_client_cases, ids=bind_client_ids)
def test_bind_client(env, mysql, case_name, target_app_id, host_key, data_key):
    with allure.step(f'app_message_keeper服务绑定client接口{case_name}'):
        host = env['host'][host_key]
        account_id = env["app_message_keeper"][data_key][int(target_app_id)]["user1"]["account_id"]
        client_id = env["app_message_keeper"][data_key][int(target_app_id)]["user1"]["bind_client_id"]
        inputs = {
            "host": host,
            "path": "/api/2/in/message_keeper/bind_client",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": 10000,
                'sign': ''
            },
            "data": {
                "target_app_id": target_app_id,
                "client_id": client_id,
                "account_id": account_id,
            }
        }
        response = hreq.request(env, inputs)
        assert response["result_code"] == "success"
        clients = mysql[data_key].fetch("bindings", where_model={"client_id": client_id, "visible": 1})
        assert len(clients) == 1
    with allure.step('app_message_keeper服务解绑client接口'):
        inputs = {
            "host": host,
            "path": "/api/2/in/message_keeper/unbind_client",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": 10000,
                'sign': ''
            },
            "data": {
                "target_app_id": target_app_id,
                "client_id": client_id,
                "account_id": account_id,
            }
        }
        response = hreq.request(env, inputs)
        assert response["result_code"] == "success"
        clients = mysql[data_key].fetch("bindings", where_model={"client_id": client_id, "visible": 0})
        assert len(clients) == 1
