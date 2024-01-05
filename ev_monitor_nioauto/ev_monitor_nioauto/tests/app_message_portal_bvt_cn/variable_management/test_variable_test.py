# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_variable_test.py
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


def test_variable_test(env, mysql):
    url = "https://message-intl-test.nioint.com/api/1/internal/bind/email"
    with allure.step('测试远程参数url'):
        path = "/api/2/in/message_portal/variable/test"
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
                       'ids': '123,234',
                       'url': url,
                       'sign': ""
                       }
        }
        response = hreq.request(env, http)
        logger.debug(response)
        assert response['result_code'] == 'success'
