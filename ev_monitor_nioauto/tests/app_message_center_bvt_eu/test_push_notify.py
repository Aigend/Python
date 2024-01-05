# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_push_notify.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/5/13 4:36 下午
# @Description :
"""
   接口文档：http://showdoc.nevint.com/index.php?s=/647&page_id=30817
"""

import json
import time
from utils.http_client import TSPRequest as hreq


class TestNotify(object):
    def test_push_notify(self, env, cmdopt):
        params_app_id = 10000
        path = "/api/2/in/message/app_notify"
        host = env['host']['app_in']
        category = 'default'
        channel = 'all'
        user_id = env['account']['nomarl']['account_id']
        app_id = '1000004,1000003'
        inputs = {
            "host": host,
            "path": path,
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": params_app_id,
                "sign": ''
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCA',
                'account_ids': user_id,
                'ttl': 100000,
                'target_app_ids': app_id,
                'do_push': True,
                'scenario': 'ls_system',
                'channel': channel,
                "category": category,
                "pass_through": 0,
                "store_history": True,
                'payload': json.dumps({
                        "target_link": "http://www.niohome.com",
                        "description": f"【BVT】时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} category:{category}user_id:{user_id}app_id:{app_id}",
                        "title": f"【BVT】【{cmdopt}】环境{channel}渠道推送测试"
                }),

            },
        }
        response = hreq.request(env, inputs)
        assert response['result_code'] == 'success'

