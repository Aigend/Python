# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_template_add.py
# @Author : qiangwei.zhang
# @time: 2021/07/29
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import allure
import pytest
from utils.random_tool import random_string
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from tests.app_message_portal.template_management.template_server import create_new_template, get_published_template_id, get_deleted_template_id
from utils.assertions import assert_equal


@pytest.mark.parametrize("case_name,app_id,id_type", [
    ("正案例_未发布的模板", "10000", "new"),
    ("正案例_已发布的模板", "10000", "published"),
    ("反案例_不存在的模板", "10000", "not_exist"),
    ("反案例_不传模板ID", "10000", "None"),
    ("反案例_已删除", "10000", "deleted"),

])
def test_template_publish(env, mysql, case_name, app_id, id_type):
    if id_type == "new":
        template_id = create_new_template(env, mysql).get("template_id")
    elif id_type == "published":
        template_id = get_published_template_id(env, mysql)
    elif id_type == "deleted":
        template_id = get_deleted_template_id(env, mysql)
    else:
        template_id_map = {"None": None, "not_exist": -1}
        template_id = template_id_map.get(id_type)
    with allure.step('发布消息模版接口'):
        path = "/api/2/in/message_portal/template/publish"
        app_id = 10000
        http = {
            "host": env['host']['app_in'],
            "path": path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": {
                "id": template_id,
            }
        }
        response = hreq.request(env, http)
        if case_name.startswith("正案例"):
            assert response['result_code'] == 'success'
            template = mysql["nmp_app"].fetch("message_template", {"template_id": template_id}, )
            status = template[0].get("status")
            assert int(status) == 9
            # mysql["nmp_app"].delete("message_template", {"template_id": template_id, "status": 9})
        else:
            if template_id:
                response.pop("request_id")
                response.pop("server_time")
                expected_res = {
                    "result_code": "invalid_param",
                    "debug_msg": "invalid template id"
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
