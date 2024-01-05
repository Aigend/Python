#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    获取根据notify各个category的统计信息，例如有多少个分类，每个分类未读消息数以及最新的一条消息等
    http://showdoc.nevint.com/index.php?s=/13&page_id=3989
"""

import allure
import pytest
from utils.http_client import TSPRequest as hreq


class TestMeesageAPI(object):
    @pytest.fixture(scope='class', autouse=False)
    def prepare(self, env, mysql):
        data = {}
        data['host_app'] = env['host']['app']
        data['host_app_in'] = env['host']['app_in']
        user = 'nmp'
        data['app_id_phone'] = '10002' if user == 'li' else '10001'  # 10001 andriod， 10002 ios
        data['account_id'] = env['vehicles'][user]['account_id']
        data['client_id'] = env['vehicles'][user]['client_id']
        data['client_id_app'] = env['vehicles'][user][f'client_id_app_{data["app_id_phone"]}']
        data['authorization'] = env['vehicles'][user][f'token_{data["app_id_phone"]}']
        return data

    def test_history_info(self, env, prepare):
        """
        获取根据notify各个category的统计信息，例如有多少个分类，每个分类未读消息数以及最新的一条消息等
        http://showdoc.nevint.com/index.php?s=/13&page_id=3989

        为了减少突然的流量高峰，增加了一层缓存， 在redis中存储history_info接口从mysql里获取的数据 ttl为10秒。
        这样第二次调用接口如果在10秒内的话直接取redis数据，否则仍然取mysql数据


        test环境 redis： t-bj-cs-message-01.dsh08y.0001.cnn1.cache.amazonaws.com.cn
        key:"message_api_prefix:{env}:{appIdStr}:{cidx}:{userId}
        例如：
        get 'message_api_prefix:test:["10001","10002"]:128505:466260582'

        clientid: ChBcDkPqNEQPZKKg0w6RDmbxEAEY-esHIJFOKAE=
        其中cidx是clients表里的主键id,user_id根据bindings表查询

        """
        inputs = {
            "host": env["host"]["app_in"],
            "path": "/api/1/message/history_info",
            "method": "GET",
            "headers": {
                "authorization": prepare['authorization'],
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
            },
            "params": {
                "hash_type": "md5",
                "region": "cn",
                "lang": "zh-cn",
                "app_id": prepare['app_id_phone'],
                'client_id': prepare['client_id_app'],
                'sign': ''
            }
        }

        response = hreq.request(env, inputs)
        with allure.step("校验 result_code"):
            assert response.get('result_code') == "success"
