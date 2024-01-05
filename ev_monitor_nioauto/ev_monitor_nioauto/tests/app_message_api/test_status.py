#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    查看message api 服务状态
    http://showdoc.nevint.com/index.php?s=/13&page_id=133
"""

import allure
import pytest

from utils.http_client import TSPRequest as hreq


@pytest.mark.skip("deprecated")
def test_status(env):
    """
    检查message api所依赖的别的服务的服务状态
    http://showdoc.nevint.com/index.php?s=/13&page_id=12888
    """
    inputs = {
        "host": env["host"]["app_in"],
        "path": "/api/1/message/status",
        "method": "GET",
        "headers": {
            "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
        }
    }
    response = hreq.request(env, inputs)
    with allure.step('校验response'):
        assert response.get("result_code") == 'success'
