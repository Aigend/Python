# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_tag_detail.py
# @Author : qiangwei.zhang
# @time: 2021/08/03
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述
# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_tag_detail1.py
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
from tests.app_message_portal.tag_management.tag_server import add_tag, get_published_tag
from utils.assertions import assert_equal
from utils.message_formator import format_to_tag_detail


class TestGetTagDetail(object):
    @pytest.fixture(scope="class")
    def prepare_tag(self, env):
        tag_id = add_tag(env)
        return tag_id

    detail_tag_keys = "case_name,app_id,id_type,expect_result"
    detail_tag_cases = (
        ["正案例_未发布tag", 10000, "new", {"result_code": "success"}],
        ["正案例_已发布tag", 10000, "published", {"result_code": "success"}],
        ["反案例_ID 为 None", 10000, "None", {"result_code": "internal_error", "debug_msg": "Required Long parameter 'id' is not present"}],
        ["反案例_ID not exist", 10000, "not_exist", {"result_code": "invalid_param", "debug_msg": "invalid tag id"}],
    )
    detail_tag_ids = [f"{case[0]}" for case in detail_tag_cases]

    @pytest.mark.parametrize(detail_tag_keys, detail_tag_cases, ids=detail_tag_ids)
    def test_tag_detail(self, env, mysql, cmdopt, case_name, app_id, id_type, expect_result, prepare_tag):
        with allure.step("准备tag id"):
            if id_type == "new":
                tag_id = prepare_tag
            elif id_type == "published":
                tag_id = get_published_tag(env, mysql)
            elif id_type == "not_exist":
                tag_id = -1
            else:
                tag_id = None
        with allure.step('根据id获取消息远程参数url详情接口'):
            path = "/api/2/in/message_portal/tag/detail"
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
                           'id': tag_id,
                           'sign': "",
                           }
            }
            if not tag_id:
                http["params"].pop('id')
            response = hreq.request(env, http)
            logger.debug(response)
            if "正案例" in case_name:
                assert response['result_code'] == 'success'
                tag = mysql["nmp_app"].fetch("remote_tag", {"id": tag_id})[0]
                expect_data = format_to_tag_detail(tag, cmdopt)
                assert_equal(response['data'], expect_data)
            else:
                response.pop("request_id")
                response.pop("server_time")
                assert_equal(response, expect_result)
