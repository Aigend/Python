# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_tag_delete.py
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

tag_delete_path = "/api/2/in/message_portal/tag/delete"
account_type_map = {"account_id": 1, "user_id": 2, "mobile_num": 3, "email": 4, "not_exist": 5, "None": None}


class TestDeleteTag(object):
    @pytest.fixture(scope="class")
    def prepare_tag(self, env):
        tag_id = add_tag(env)
        return tag_id

    delete_tag_keys = "case_name,app_id,id_type,expect_result"
    delete_tag_cases = (
        ["正案例_删除未发布tag", 10000, "new", {"result_code": "success"}],
    )
    delete_tag_ids = [f"{case[0]}" for case in delete_tag_cases]

    @pytest.mark.parametrize(delete_tag_keys, delete_tag_cases, ids=delete_tag_ids)
    def test_delete_tag(self, env, mysql, case_name, app_id, id_type, expect_result, prepare_tag):
        with allure.step("发布tag"):
            inputs = {
                "host": env['host']['app_in'],
                "path": tag_delete_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": {
                    "id": prepare_tag
                }
            }
            response = hreq.request(env, inputs)
            response.pop("request_id")
            response.pop("server_time")
            if "正案例" in case_name:
                mysql_results = mysql['nmp_app'].fetch("remote_tag", {"id": prepare_tag}, retry_num=1)
                assert len(mysql_results) == 0
            else:
                assert_equal(response, expect_result)
