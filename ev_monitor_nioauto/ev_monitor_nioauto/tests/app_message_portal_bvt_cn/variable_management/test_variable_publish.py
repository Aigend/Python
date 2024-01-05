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
])
def test_variable_publish(env, mysql, case_name, app_id, id_type):
    if id_type == "published":
        variable_id = get_published_variable_id(env, mysql)
    elif id_type == "new":
        new_variable = create_new_variable(env, mysql)
        variable_id = new_variable.get("id")
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
        assert response['result_code'] == 'success'
        variable = mysql["nmp_app"].fetch("remote_variable", {"id": variable_id}, )
        status = variable[0].get("status")
        assert int(status) == 9

