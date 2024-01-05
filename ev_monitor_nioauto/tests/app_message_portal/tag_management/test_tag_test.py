# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_tag_test.py
# @Author : qiangwei.zhang
# @time: 2021/08/03
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述
import time

import allure
from utils.http_client import TSPRequest as hreq
from utils.logger import logger

account_type_map = {"account_id": 1, "mobile_num": 2, "user_id": 3, "email": 4, "not_exist": 5, "None": None}


def test_tag_test(env, mysql):
    url = "http://pangu.nioint.com:5000/pangu/get_tag_fake_id_page"
    with allure.step('根据测试远程参数url'):
        path = "/api/2/in/message_portal/tag/test"
        app_id = 10000
        # app_id = 10022
        http = {
            "host": env['host']['app_in'],
            "path": path,
            "method": "GET",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                'url': url,
                'type': 1,
                'sign': '',
            }
        }
        response = hreq.request(env, http)
        logger.debug(response)
        assert response['result_code'] == 'success'


def get_url(env):
    start_time = time.time()
    with allure.step('根据测试远程参数url'):
        app_id = 10000
        http = {
            "host": "https://message-intl-test.nioint.com",
            "path": "/api/1/internal/bind/email",
            "method": "GET",
            "params": {
                "hash_type": "sha256",
                "app_id": app_id,
                "offset": 0,
                "count": 100,
                'sign': ''
            }
        }
        response = hreq.request(env, http)
        end_time = time.time()
        s_time = end_time - start_time
        logger.debug(f"s_time:{s_time * 1000}")
        logger.debug(response)


def test_get_url_fake(env, mysql):
    start_time = time.time()
    with allure.step('根据测试远程参数url'):
        app_id = 10000
        http = {
            "host": "http://pangu.nioint.com:5000",
            "path": "/pangu/get_tag_fake_id_page_2k",
            "method": "GET",
            "params": {
                "hash_type": "sha256",
                "app_id": app_id,
                "offset": 0,
                "count": 1,
                'sign': ''
            }
        }
        response = hreq.request(env, http)
        end_time = time.time()
        s_time = end_time - start_time
        logger.debug(f"s_time:{s_time * 1000}")
        logger.debug(response)
