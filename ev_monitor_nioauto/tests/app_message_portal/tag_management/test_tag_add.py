# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_tag_add.py
# @Author : qiangwei.zhang
# @time: 2021/12/23
# @api: GET_/api/XXX 【必填】
# @showdoc: http://showdoc.nevint.com/index.php?s=/647&page_id=32812
# @Description :脚本描述

import allure
import pytest
import time
import json

from tests.app_message_portal.tag_management.tag_server import init_tag
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from utils.assertions import assert_equal

tag_add_path = "/api/2/in/message_portal/tag/add"
account_type_map = {"account_id": 1, "mobile_num": 2, "user_id": 3, "email": 4, "not_exist": 5, "None": None}

add_tag_keys = "case_name,account_type,name,url,expect_result"
add_tag_cases = (
    ["正案例_email", "email", "init_email", "http://pangu.nioint.com:5000/pangu/get_tag_email", {"result_code": "success"}],
    ["正案例_account_id", "account_id", "获取account_id", "http://www.accountidadd.com", {"result_code": "success"}],
    ["正案例_user_id", "user_id", "获取user_id", "http://www.useridadd.com", {"result_code": "success"}],
    ["正案例_mobile_num", "mobile_num", "获取mobile_num", "http://www.mobilenumadd.com", {"result_code": "success"}],
    ["正案例_email", "email", "获取email", "http://www.emailadd.com", {"result_code": "success"}],
    ["反案例_not_exist", "not_exist", "获取not_exist", "http://www.notexistadd.com", {"result_code": "invalid_param", "debug_msg": "necessary parameters are null or invalid."}],
    ["正案例_url不加校验", "account_id", "不符合规范的url", "ssdfdfdedvc", {"result_code": "success"}],
    ["反案例_type为None", "None", "不符合规范的url", "http://www.notexistadd.com", {"result_code": "invalid_param", "debug_msg": "necessary parameters are null or invalid."}],
    ["反案例_name为None", "None", None, "http://www.notexistadd.com", {"result_code": "invalid_param", "debug_msg": "necessary parameters are null or invalid."}],
    ["反案例_url为None", "account_id", "url为None", None, {"result_code": "invalid_param", "debug_msg": "necessary parameters are null or invalid."}],
)
add_tag_ids = [f"{case[0]}" for case in add_tag_cases]


@pytest.mark.parametrize(add_tag_keys, add_tag_cases, ids=add_tag_ids)
def test_add_tag(env, mysql, case_name, account_type, name, url, expect_result):
    with allure.step(f'接口地址{tag_add_path}'):
        app_id = 10000
        inputs = {
            "host": env['host']['app_in'],
            "path": tag_add_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": {
                "type": account_type_map.get(account_type),
                "name": name,
                "url": url,
            }
        }
        response = hreq.request(env, inputs)
    with allure.step("校验返回结果"):
        response.pop("request_id")
        response.pop("server_time")
        if "正案例" in case_name:
            tag_id = response.pop("data")
            expect_mysql_value = inputs.get("json")
            expect_mysql_value["id"] = tag_id
            expect_mysql_value["app_id"] = str(app_id)
            expect_mysql_value["status"] = 1  # 草稿
            assert_equal(response, expect_result)
            mysql_results = mysql['nmp_app'].fetch("remote_tag", {"id": tag_id}, exclude_fields=["create_time", "update_time"])
            assert len(mysql_results) == 1
            mysql_result = mysql_results[0]
            assert_equal(mysql_result, expect_mysql_value)
        else:
            assert_equal(response, expect_result)


def test_init_tag(env, mysql):
    tag_map = init_tag(env, mysql)
    # {'init_email': 58, 'init_mobile_num': 59, 'init_test_user_id': 60}
    logger.debug(tag_map)
