#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2021/06/01 14:10
@contact: hongzhen.bi@nio.com
@description: FOD成功失败app消息推送
"""
import pprint
import time

import pytest

from config.cert import web_cert
from utils.http_client import TSPRequest


class TestFodPushLog(object):
    @pytest.mark.skip("Manual")
    def test_fod_push_log(self, env, cmdopt, mysql, publish_msg_by_kafka):
        """
        np完整版(sku-M1000007/M1000010),激活成功可以给车主/授权人推送激活成功消息
        """
        account_id = env['vehicles']['vehicle_for_repair']['account_id']
        vehicle_id = env['vehicles']['vehicle_for_repair']['vehicle_id']
        http = {
            "host": f"{env['host']['tsp_in']}:4430",
            "path": "/api/1/in/vehicle/command/pub_fod",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "app_id": 100058,
                "nonce": int(time.time())
            },
            "data": {
                "account_id": account_id,
                "vehicle_id": vehicle_id,
                "fod_order_id": "sdsdwwwwww",
                "is_safety_critical": "false",
                "skucode": "M1000007",
                "is_deactivate": "false",
                "ttl": "86400",
                "callback_url": "http://10.110.3.103:9999/api/v1/callback"
            },
            "verify": False,
            "cert": web_cert
        }

        response = TSPRequest.request(env, http)
        pprint.pprint(response)
