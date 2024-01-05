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

import requests

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq
from tests.app_message_portal.tag_management.tag_server import add_tag, get_published_tag, init_tag
from utils.logger import logger

get_tag_num_path = "/api/2/in/message_portal/tag/id_num"
account_type_map = {"account_id": 1, "user_id": 2, "mobile_num": 3, "email": 4, "not_exist": 5, "None": None}


class TestUpdateTag(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_tag(self, env, mysql):
        return init_tag(env, mysql)

    get_tag_num_keys = "case_name,app_id,tag_name,expect_result"
    get_tag_num_cases = (
        ["正案例_分页url", 10000, "init_fake_id", {"result_code": "success"}],
        ["正案例_单页url", 10000, "init_email", {"result_code": "success"}],
    )
    get_tag_num_ids = [f"{case[0]}" for case in get_tag_num_cases]

    @pytest.mark.parametrize(get_tag_num_keys, get_tag_num_cases, ids=get_tag_num_ids)
    def test_get_tag_num(self, env, mysql, case_name, app_id, tag_name, expect_result, prepare_tag):
        with allure.step("准备tag id"):
            tag_id = prepare_tag.get(tag_name)
            tag = mysql["nmp_app"].fetch("remote_tag", where_model={"id": tag_id})
            url = tag[0].get("url")
        with allure.step(f'接口地址{get_tag_num_path}'):
            inputs = {
                "host": env['host']['app_in'],
                "path": get_tag_num_path,
                "method": "GET",
                "params": {
                    "region": "cn",
                    "lang": "zh-cn",
                    "hash_type": "sha256",
                    "app_id": app_id,
                    "sign": "",
                    "id": tag_id
                }
            }
            response = hreq.request(env, inputs)
            if "正案例" in case_name:
                res = requests.get(url).json()
                assert response.get("data") == res.get("data").get("total")
            else:
                response.pop("request_id")
                response.pop("server_time")
                assert_equal(response, expect_result)
