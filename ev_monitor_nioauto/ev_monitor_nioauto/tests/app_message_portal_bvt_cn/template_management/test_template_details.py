# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_template_detail1.py
# @Author : qiangwei.zhang
# @time: 2021/08/03
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述


import allure
import pytest
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from tests.app_message_portal.template_management.template_server import create_new_template, get_published_template_id
from utils.assertions import assert_equal
from utils.message_formator import format_to_template_detail


# app_id = 1000075
# app_id = 10000


@pytest.mark.parametrize("case_name,app_id,id_type,channel", [
    ("正案例_未发布的模板", "10000", "new", "email"),
    ("正案例_已发布的模板", "10000", "published", "email"),
])
def test_template_detail(env, mysql, cmdopt, case_name, app_id, id_type, channel):
    if id_type == "new":
        template_id = create_new_template(env, mysql).get("template_id")
    elif id_type == "published":
        template_id = get_published_template_id(env, mysql)
    with allure.step('根据id获取消息模板详情接口'):
        path = "/api/2/in/message_portal/template/detail"
        http = {
            "host": env['host']['app_in'],
            "path": path,
            "method": "GET",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn",
                       "lang": "zh-cn",
                       "hash_type": "sha256",
                       "app_id": app_id,
                       'id': template_id,
                       "sign": ""
                       }
        }
        response = hreq.request(env, http)
        logger.debug(response)
        if "正案例" in case_name:
            assert response['result_code'] == 'success'
            template = mysql["nmp_app"].fetch("message_template", {"template_id": template_id}, )[0]
            except_data = format_to_template_detail(template, cmdopt)
            assert_equal(except_data, response['data'])
