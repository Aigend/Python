#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:li.liu2 
@time: 2020/08/07 19:13
@contact: li.liu2@nio.com
@description:
    获取notify列表
    http://showdoc.nevint.com/index.php?s=/13&page_id=923
"""

import allure
import pytest
from utils.http_client import TSPRequest as hreq

enable_cold_history = False

class TestMeesageAPI(object):

    history_list_keys = "case_name,target_app_id,host_key,data_key"
    history_list_cases = [
        ("正案例_TOC_IOS_NIO_APP 10002", "10002", 'app_in', 'nmp_app'),
        ("正案例_TOC_ANDROID_NIO_APP 10001", "10001", 'app_in', 'nmp_app'),
    ]
    history_list_ids = [f"{case[0]}" for case in history_list_cases]

    @pytest.mark.parametrize(history_list_keys, history_list_cases, ids=history_list_ids)
    def test_history_list(self, env, mysql, case_name, target_app_id, host_key, data_key):
        """
        获取notify列表
        http://showdoc.nevint.com/index.php?s=/13&page_id=923

        """
        offset = 0
        count = 50
        ""
        toc_nio_app_group, tob_staff_app_group, tob_fellow_app_group = ["10001", "10002"], ["10003"], ["10018"]
        group_dict = {"10001": toc_nio_app_group, "10002": toc_nio_app_group, "10003": tob_staff_app_group, "10018": tob_fellow_app_group}
        app_id_group = group_dict.get(target_app_id, [target_app_id])
        account_id = env["app_message_keeper"][data_key][int(target_app_id)]["user1"]["account_id"]
        token = env["app_message_keeper"][data_key][int(target_app_id)]["user1"][f"token_{target_app_id}"]
        inputs = {
            "host": env['host']['app_ex'],
            "path": "/api/1/message/history_list",
            "method": "GET",
            "headers": {
                "authorization": token,
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; BLN-AL20 Build/HONORBLN-AL20)/2.9.5-Lifestyle-Android'
            },
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": target_app_id,
                "offset": offset,
                'count': count,
                'sign': ''

            }
        }
        response = hreq.request(env, inputs)
        data = response.get("data")
        with allure.step("校验 result_code"):
            assert response.get('result_code') == "success"
        history = 'history_' + str(account_id)[-3:]
        cold_history = 'cold_history_' + str(account_id)[-3:]
        with allure.step("校验mysql"):
            message_in_mysql_history = mysql[data_key].fetch(history, where_model={'user_id': account_id, 'app_id in': app_id_group}, suffix=f"limit {offset},{count}",
                                                             retry_num=5)
            history_len = len(message_in_mysql_history)
            message_in_mysql_cold_history = []
            if history_len < count and enable_cold_history:
                message_in_mysql_cold_history = mysql[data_key].fetch(cold_history, where_model={'user_id': account_id, 'app_id in': app_id_group},
                                                                      suffix=f"limit {count - history_len}", retry_num=5)
            len_of_message_in_mysql = history_len + len(message_in_mysql_cold_history)
            assert len_of_message_in_mysql == len(data)
