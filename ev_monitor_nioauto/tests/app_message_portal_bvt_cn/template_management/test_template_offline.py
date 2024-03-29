# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_template_add.py
# @Author : qiangwei.zhang
# @time: 2021/07/29
# @api: POST_/api/2/in/message_portal/template/offline 【必填】
# @showdoc:http://showdoc.nevint.com/index.php?s=/647&page_id=32580
# @Description :脚本描述

import allure
import pytest
from utils.http_client import TSPRequest as hreq
from tests.app_message_portal.template_management.template_server import create_new_template, get_published_template_id
from utils.assertions import assert_equal

path = "/api/2/in/message_portal/template/offline"


@pytest.mark.parametrize("case_name,app_id,id_type", [
    ("正案例_未发布的模板也可以被下线", "10000", "new"),
    ("正案例_已发布的模板，下线后改为草稿状态", "10000", "published"),
])
def test_template_offline(env, mysql, case_name, app_id, id_type):
    if id_type == "new":
        template_id = create_new_template(env, mysql).get("template_id")
    elif id_type == "published":
        template_id = get_published_template_id(env, mysql)
    with allure.step('下线已发布消息模版接口'):
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
            assert int(status) == 1
            # mysql["nmp_app"].delete("message_template", {"id": template_id, "status": 9})
        else:
            if not template_id:
                response.pop("request_id")
                response.pop("server_time")
                expected_res = {
                    "result_code": "invalid_param",
                    "debug_msg": "necessary parameters are null."
                }
                assert_equal(expected_res, response)
            else:
                response.pop("request_id")
                response.pop("server_time")
                expected_res = {
                    "result_code": "invalid_param",
                    "debug_msg": "invalid template id"
                }
                assert_equal(expected_res, response)
