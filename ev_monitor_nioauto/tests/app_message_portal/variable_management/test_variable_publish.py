# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_variable_publish.py
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
from tests.app_message_portal.variable_management.variable_server import create_new_variable, get_published_variable_id
from utils.assertions import assert_equal


@pytest.mark.parametrize("case_name,app_id,id_type", [
    ("正案例_未发布的远程参数url", "10000", "new"),
    ("正案例_已发布的远程参数url", "10000", "published"),
    ("反案例_不存在的远程参数url", "10000", "not_exit"),
    ("反案例_已发布的远程参数url", "10000", "None"),
])
def test_variable_publish(env, mysql, case_name, app_id, id_type):
    if id_type == "published":
        variable_id = get_published_variable_id(env, mysql)
    elif id_type == "new":
        new_variable = create_new_variable(env, mysql)
        variable_id = new_variable.get("id")
    else:
        variable_id_map = {"None": None, "not_exist": -1}
        variable_id = variable_id_map.get(id_type)
    with allure.step('发布远程参数接口'):
        path = "/api/2/in/message_portal/variable/publish"
        app_id = 10000
        http = {
            "host": env['host']['app_in'],
            "path": path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": {
                "id": variable_id,
            }
        }
        response = hreq.request(env, http)
        if case_name.startswith("正案例"):
            assert response['result_code'] == 'success'
            variable = mysql["nmp_app"].fetch("remote_variable", {"id": variable_id}, )
            status = variable[0].get("status")
            assert int(status) == 9
            mysql["nmp_app"].delete("remote_variable", {"id": variable_id, "status": 9})
        else:
            if variable_id:
                response.pop("request_id")
                response.pop("server_time")
                expected_res = {
                    "result_code": "invalid_param",
                    "debug_msg": "invalid variable id"
                }
                assert_equal(expected_res, response)
            else:
                response.pop("request_id")
                response.pop("server_time")
                expected_res = {
                    "result_code": "invalid_param",
                    "debug_msg": "necessary parameters are null."
                }
                assert_equal(expected_res, response)
