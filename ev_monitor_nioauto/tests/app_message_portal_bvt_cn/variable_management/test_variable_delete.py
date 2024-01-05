# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_variable_delete.py
# @Author : qiangwei.zhang
# @time: 2021/08/03
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import allure
import pytest
from utils.random_tool import random_string
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from utils.assertions import assert_equal
from tests.app_message_portal.variable_management.variable_server import create_new_variable,get_published_variable_id


@pytest.mark.parametrize("case_name,expected_result", [
    ("正案例_删除远程参数url", {"result_code": "success"}),
])
def test_variable_delete(env, mysql, case_name, expected_result):
    new_variable = create_new_variable(env, mysql)
    variable_id = new_variable.get("id")
    with allure.step('删除消息远程参数url接口'):
        path = "/api/2/in/message_portal/variable/delete"
        app_id = 10000
        http = {
            "host": env['host']['app_in'],
            "path": path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": {"id": variable_id}
        }
        response = hreq.request(env, http)
        response.pop('request_id')
        response.pop('server_time')
        assert_equal(response, expected_result)
        if response['result_code'] == "success":
            with allure.step('校验mysql远程参数url被删除'):
                variable = mysql["nmp_app"].fetch("remote_variable", {"id": variable_id}, retry_num=1)
                assert len(variable) == 0