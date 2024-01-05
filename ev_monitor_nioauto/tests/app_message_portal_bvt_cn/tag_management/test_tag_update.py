# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_tag_update.py
# @Author : qiangwei.zhang
# @time: 2021/12/23
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import allure
import pytest
import time
import json

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq
from tests.app_message_portal.tag_management.tag_server import add_tag, get_published_tag
from utils.logger import logger

tag_update_path = "/api/2/in/message_portal/tag/update"
account_type_map = {"account_id": 1, "user_id": 2, "mobile_num": 3, "email": 4, "not_exist": 5, "None": None}


class TestUpdateTag(object):
    @pytest.fixture(scope="class")
    def prepare_tag(self, env):
        tag_id = add_tag(env)
        return tag_id

    update_tag_keys = "case_name,app_id,account_type,name,url,id_type,expect_result"
    update_tag_cases = (
        ["正案例_更新", 10000, "user_id", "update_name", "http://www.updateurl.com", "new", {"result_code": "success"}],
        ["反案例_更新已发布tag", 10000, "user_id", "update_name", "http://www.updateurl.com", "published", {"result_code": "internal_error", "debug_msg": "update tag error"}],
    )
    update_tag_ids = [f"{case[0]}" for case in update_tag_cases]

    @pytest.mark.parametrize(update_tag_keys, update_tag_cases, ids=update_tag_ids)
    def test_update_tag(self, env, mysql, case_name, app_id, account_type, name, url, id_type, expect_result, prepare_tag):
        with allure.step("准备tag id"):
            if id_type == "new":
                tag_id = prepare_tag
                status = 1
            elif id_type == "published":
                tag_id = get_published_tag(env, mysql)
                status = 9
            else:
                tag_id = -1
        with allure.step(f'接口地址{tag_update_path}'):
            inputs = {
                "host": env['host']['app_in'],
                "path": tag_update_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": {
                    "id": tag_id,
                    "type": account_type_map.get(account_type),
                    "name": name,
                    "url": url,
                }
            }

            response = hreq.request(env, inputs)
            response.pop("request_id")
            response.pop("server_time")
            if "正案例" in case_name:
                expect_mysql_value = inputs.get("json")
                expect_mysql_value["app_id"] = str(app_id)
                expect_mysql_value["status"] = status  # 草稿
                assert_equal(response, expect_result)
                mysql_results = mysql['nmp_app'].fetch("remote_tag", {"id": tag_id}, exclude_fields=["create_time", "update_time"])
                assert len(mysql_results) == 1
                mysql_result = mysql_results[0]
                assert_equal(mysql_result, expect_mysql_value)
            else:
                assert_equal(response, expect_result)


