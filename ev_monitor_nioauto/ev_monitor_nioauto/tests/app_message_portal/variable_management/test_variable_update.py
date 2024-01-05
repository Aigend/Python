# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_variable_update.py
# @Author : qiangwei.zhang
# @time: 2021/08/03
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import allure
import pytest
from utils.random_tool import random_string, format_time
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from tests.app_message_portal.variable_management.variable_server import create_new_variable, delete_variable, get_published_variable_id
from utils.assertions import assert_equal


@pytest.mark.parametrize("case_name,id_type,expected_result", [
    ("正案例_未发布的远程参数url", "new", {"result_code": "success"}),
    ("反案例_已发布的远程参数url", "published", {"result_code": "internal_error", "debug_msg": "update variable error"}),
    ("反案例_不存在的远程参数url", "not_exist", {"result_code": "invalid_param", "debug_msg": "invalid variable id"}),
    ("反案例_为None", "None", {"result_code": "invalid_param", "debug_msg": "necessary parameters are null."}),
])
def test_update_variable(env, mysql, case_name, id_type, expected_result):
    app_id = 10000
    if id_type == "published":
        variable_id = get_published_variable_id(env, mysql)
    elif id_type == "new":
        new_variable = create_new_variable(env, mysql)
        variable_id = new_variable.get("id")
    else:
        variable_id_map = {"None": None, "not_exist": -1}
        variable_id = variable_id_map.get(id_type)
    with allure.step('更新远程参数url接口'):
        """
        http://showdoc.nevint.com/index.php?s=/647&page_id=31041
        """
        path = "/api/2/in/message_portal/variable/update"
        rs5 = random_string(5)
        ft = format_time()
        url = f"http://www.{random_string(5)}.com"
        name = f"【更新远程参数url名称】{rs5}_{ft}"
        http = {
            "host": env['host']['app_in'],
            "path": path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                "sign": ""
            },
            "json": {
                "id": variable_id,
                "url": url,
                "name": name,
            }
        }
        response = hreq.request(env, http)
        response.pop('request_id')
        response.pop('server_time')
        assert_equal(response, expected_result)
        if case_name.startswith("正案例"):
            variable = mysql["nmp_app"].fetch("remote_variable", {"id": variable_id}, )
            mysql_value = {
                "id": variable[0].get("id"),
                "url": variable[0].get("url"),
                "name": variable[0].get("name"),
            }
            assert_equal(mysql_value, http.get("json"))
            # delete_variable(env, mysql, variable_id)
