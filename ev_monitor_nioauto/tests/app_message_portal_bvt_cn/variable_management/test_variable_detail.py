# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_variable_detail.py
# @Author : qiangwei.zhang
# @time: 2021/08/03
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述
# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_variable_detail1.py
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
from tests.app_message_portal.variable_management.variable_server import create_new_variable, delete_variable
from utils.assertions import assert_equal
from utils.message_formator import format_to_variable_detail


def test_variable_detail(env, mysql, cmdopt):
    variable = create_new_variable(env, mysql)
    variable_id = variable.get("id")
    with allure.step('根据id获取消息远程参数url详情接口'):
        path = "/api/2/in/message_portal/variable/detail"
        app_id = 10000
        http = {
            "host": env['host']['app_in'],
            "path": path,
            "method": "GET",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn",
                       "lang": "zh-cn",
                       "hash_type": "sha256",
                       "app_id": app_id,
                       'id': variable_id,
                       'sign': ""
                       }
        }
        response = hreq.request(env, http)
        logger.debug(response)
        assert response['result_code'] == 'success'
        expect_data = format_to_variable_detail(variable, cmdopt)
        assert_equal(expect_data, response['data'])
        delete_variable(env, mysql, variable_id)
