#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    获取未读的notify数量
    http://showdoc.nevint.com/index.php?s=/13&page_id=924
"""

import allure
import pytest

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq


class TestMeesageAPI(object):
    @pytest.fixture(scope='class', autouse=False)
    def prepare(self, env):
        data = {}
        user = 'nmp'
        data['app_id_phone'] = '10002' if user == 'li' else '10001'  # 10001 andriod， 10002 ios
        data['account_id'] = env['vehicles'][user]['account_id']
        data['client_id'] = env['vehicles'][user]['client_id']
        data['client_id_app'] = env['vehicles'][user][f'client_id_app_{data["app_id_phone"]}']
        data['authorization'] = env['vehicles'][user][f'token_{data["app_id_phone"]}']
        return data

    def test_history_unread_num(self, env, mysql, prepare):
        """
        获取未读的notify数量
        http://showdoc.nevint.com/index.php?s=/13&page_id=924
        """

        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/1/message/history_unread_num",
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
        data = response.get("data")
        with allure.step("校验 result_code"):
            assert response.get('result_code') == "success"

        table = 'history_' + str(prepare['account_id'])[-3:]
        with allure.step("校验mysql"):
            message_in_mysql = mysql['nmp_app'].fetch(table, fields=['count(1) as message_count'],
                                                      where_model={'user_id': prepare['account_id'], 'read': 0, 'app_id': prepare['app_id_phone']})
            len_of_message_in_mysql = message_in_mysql[0]['message_count']
            assert len_of_message_in_mysql == int(data)
