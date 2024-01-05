# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_get_grsql.py
# @Author : qiangwei.zhang
# @time: 2021/07/23
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import json
import random
import string
import time
import allure
import pytest
from utils.logger import logger
from utils.http_client import TSPRequest as hreq
from utils.random_tool import random_code
"""
https://tsp-test.nioint.com/api/1/in/battery/graphql?sign=c77ca3df4b7413842f2692d935a0dfc6&timestamp=1627009082&app_id=100078
"""


def test_post_battery_graphql(env, cmdopt, mysql):
    """
        接口文档：http://showdoc.nevint.com/index.php?s=/252&page_id=30638
        https://tsp-stg-eu.nioint.com/api/1/in/battery/get_bid
        "03UPSI2PKM7EZ1G5LXNQDOU3": "9af2ce4ba4be428a945df36a65325cb0"
        "03UPLR2HTON6KDVJQW1F7SME": "cb818cb2eeea4e17befede33a17340ac"
    """
    app_id = 100078
    http = {
        "host": env['host']['tsp_in'],
        "path": "/api/1/in/battery/graphql",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "params": {
            "app_id": app_id,
            "sign": ""
        },
        "json": {
            "query": "{pack (nio_encoding:\"P0000084AH130YY0012340001YFTY01\", export:false) {code bid nio_encoding nio_code model_id order_no status source create_time cell_code_size} }"}
    }
    response = hreq.request(env, http)
    assert response['result_code'] == 'success'
