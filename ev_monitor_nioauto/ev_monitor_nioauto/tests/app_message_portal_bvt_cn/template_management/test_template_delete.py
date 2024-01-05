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


from utils.http_client import TSPRequest as hreq
from utils.assertions import assert_equal
from tests.app_message_portal.template_management.template_server import create_new_template, create_template_and_published, offline_template


@pytest.mark.parametrize("case_name,id_type,expected_result", [
    ("正案例_删除模板", "new", {"result_code": "success"}),
    ("正案例_删除下线模板", "new_publish_offline", {"result_code": "success"}),
])
def test_template_delete(env, mysql, case_name, id_type, expected_result):
    if id_type == "new":
        template_id = create_new_template(env, mysql).get("template_id")
    elif id_type == "new_publish_offline":
        template_id = create_template_and_published(env, mysql)
        offline_template(env, mysql, template_id)

    with allure.step('删除消息模版接口'):
        path = "/api/2/in/message_portal/template/delete"
        app_id = 10000
        http = {
            "host": env['host']['app_in'],
            "path": path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": {"id": template_id}
        }
        response = hreq.request(env, http)
        assert response['result_code'] == 'success'
        response.pop('request_id')
        response.pop('server_time')
        assert_equal(response, expected_result)
        if response['result_code'] == "success":
            with allure.step('校验mysql模板被删除'):
                template = mysql["nmp_app"].fetch("message_template", {"valid": 1, "template_id": template_id}, retry_num=1)
                assert len(template) == 0
            with allure.step('校验mysql message_template_snapshot模板未被删除'):
                template_snapshot = mysql["nmp_app"].fetch("message_template_snapshot", {"template_id": template_id}, {"count(1) template_count"})
                template_snapshot_count_after_update = template_snapshot[0].get("template_count")
                assert template_snapshot_count_after_update > 0
