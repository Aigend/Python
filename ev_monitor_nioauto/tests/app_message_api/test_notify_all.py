#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    用于给APP群发消息
    http://showdoc.nevint.com/index.php?s=/13&page_id=151
    * only allow 10 notify all at the same time.
"""
import json
import time
import pytest
from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq


@pytest.mark.skip('manual')
class TestMeesageAPI(object):
    @pytest.mark.skip('manual')
    def test_notify_all(self, env, cmdopt):
        """
        用于给APP群发消息
        http://showdoc.nevint.com/index.php?s=/13&page_id=151
        * only allow 10 notify all at the same time.
        """
        target_app_ids = "10001,10002"
        if 'marcopolo' in cmdopt:
            target_app_ids = '1000003,1000004'
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/in/message/notify_all",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "sign": "",
                "app_id": "10000"
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCG',
                'async': False,
                'ttl': 100000,
                'target_app_ids': target_app_ids,
                'do_push': True,
                'channel': 'hwpush',
                'scenario': 'fs_system',
                "category": "activity",  # 可以default， activity，red_packet等字段，分别推到手机的通知条目，活动条目，积分红包条目
                'payload': json.dumps({
                    "target_link": "http://www.niohome.com",
                    "title": f"【{cmdopt}】环境测试notify_all推送,如有误收请忽略，打扰见谅！！！",
                    "description": f"时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} /api/1/in/message/notify_all",
                }),
            }
        }

        response = hreq.request(env, inputs)

        message_id = response['data'].pop('message_id', '')
        assert_equal('success', response['result_code'])
        assert_equal('notify_all' in message_id, True)
