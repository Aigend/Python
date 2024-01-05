#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    获取一年前的notify列表
    http://showdoc.nevint.com/index.php?s=/13&page_id=21616

"""

import allure
import pytest

from utils.assertions import assert_equal
from utils.httptool import request as rq
from utils.http_client import TSPRequest as hreq
from utils.time_parse import timestamp_to_utc_strtime


class TestMeesageAPI(object):
    @pytest.fixture(scope='class', autouse=False)
    def prepare(self, env, mysql):
        data = {}
        data['host_app'] = env['host']['app']
        data['host_app_in'] = env['host']['app_in']
        data['app_id_phone'] = '10001'
        data['client_id_app'] = env['vehicles']['nmp'][f'client_id_app_{data["app_id_phone"]}']
        data['authorization'] = env['vehicles']['nmp'][f'token_{data["app_id_phone"]}']
        data['account_id'] = env['vehicles']['nmp']['account_id']
        return data

    def test_archive_history_list(self, env, prepare, mysql):
        """
        获取一年前的notify列表
        http://showdoc.nevint.com/index.php?s=/13&page_id=21616
        """
        max_count = 50
        inputs = {
            "host": env["host"]["app_in"],
            "path": "/api/1/message/archive_history_list",
            "method": "GET",
            "headers": {
                "authorization": prepare['authorization'],
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
            },
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "md5",
                "app_id": prepare['app_id_phone'],
                'client_id': prepare['client_id_app'],
                "offset": 0,
                'count': max_count,
                # 'nonce': 'nondceafadfdasfadfa',
                "sign": ""
            }
        }
        response = hreq.request(env, inputs)
        data = response.get('data', '')
        assert response.get("result_code") == "success"
        table = 'archive_history_' + str(prepare['account_id'])[-3:]
        with allure.step("校验mysql"):
            message_in_mysql = mysql['nmp_app'].fetch(table, {'user_id': prepare['account_id'], 'visible': 1}, fields=['count(1) as msg_count'])
            len_of_message_in_mysql = message_in_mysql[0]['msg_count']
            len_of_message_in_mysql = len_of_message_in_mysql if len_of_message_in_mysql < max_count else max_count
            assert_equal(len_of_message_in_mysql, len(data))
