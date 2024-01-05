#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    获取配置信息
    http://showdoc.nevint.com/index.php?s=/13&page_id=7245

"""

import allure
from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq


def test_get_config(env, cmdopt):
    """
    获取配置信息
    http://showdoc.nevint.com/index.php?s=/13&page_id=7245
    """
    inputs = {
        "host": env['host']['app_in'],
        "path": "/api/1/in/message/get_config",
        "method": "GET",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "params": {
            "app_id": "10000",
            "region": "cn",
            "lang": "zh-cn",
            'project': 'nmp-api',
            'conf_name': 'notification.app_white_list',
            'sign': "",
        }
    }

    response = hreq.request(env, inputs)
    with allure.step('校验response'):
        response.pop('request_id', '')
        response.pop('server_time', '')
        expect = {'data': {"1000003": f"swc-cvs-nmp-{cmdopt}-1000003-notification",
                           "10018": f"swc-cvs-nmp-{cmdopt}-10018-notification",
                           "1000004": f"swc-cvs-nmp-{cmdopt}-1000004-notification",
                           "10001": f"swc-cvs-nmp-{cmdopt}-10001-notification",
                           "10003": f"swc-cvs-nmp-{cmdopt}-10003-notification",
                           "30007": f"swc-cvs-nmp-{cmdopt}-30007-notification"},
                  'result_code': 'success'
                  }
        assert_equal(response, expect)
