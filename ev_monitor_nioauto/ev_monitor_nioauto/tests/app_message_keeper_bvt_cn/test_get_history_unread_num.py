# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_get_history_unread_num.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/5/26 3:14 下午
# @Description :
"""
        http://showdoc.nevint.com/index.php?s=/647&page_id=31037
        获取未读消息数量
        /api/2/in/message_keeper/history_unread_num
        接口参数：
            * app_id 服务ID
                ✅* 必填
            * region 区域码
                ✅* 非必填
            * lang 语言
                ✅* 非必填
            * timestamp 时间戳
                ✅* 必填
            * sign 签名
                ✅* 必填
            * account_id 用户ID
                ✅* 必填
            * categories 类别
                ✅* 非必填，默认所有
                ✅* 最多30个
                ✅* 单个
                ✅* 多个
            * show_sub_app
                ⏸️* 默认 false
                ⏸* true
                ⏸* false
            * target_app_id 展示原始数据
                ✅* 非必填，默认所有
        """

import allure
import time
import pytest

from utils.assertions import assert_equal
from utils.httptool import request as rq
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from utils.employee_id_converter import employee_id_converter
from utils.assertions import assert_equal


class TestMeesageAPI(object):
    history_unread_num_keys = "case_name,target_app_id,host_key,data_key"
    history_unread_num_cases = [
        ("正案例_TOB_Android Staff APP 10003", "10003", 'app_tob_in', 'nmp_app_tob'),
        ("正案例_TOB_Android Fellow APP 10018", "10018", 'app_tob_in', 'nmp_app_tob'),
        ("正案例_TOC_IOS_NIO_APP 10002", "10002", 'app_in', 'nmp_app'),
        ("正案例_TOC_ANDROID_NIO_APP 10001", "10001", 'app_in', 'nmp_app'),

    ]
    history_unread_num_ids = [f"{case[0]}" for case in history_unread_num_cases]

    @pytest.mark.parametrize(history_unread_num_keys, history_unread_num_cases, ids=history_unread_num_ids)
    def test_history_unread_num_total(self, env, mysql, cmdopt, case_name, target_app_id, host_key, data_key):
        with allure.step(f'{host_key}公司员工获取未读消息数量接口{case_name}'):
            host = env['host'][host_key]
            app_id = 10000
            toc_nio_app_group, tob_staff_app_group, tob_fellow_app_group = ["10001", "10002"], ["10003"], ["10018"]
            group_dict = {"10001": toc_nio_app_group, "10002": toc_nio_app_group, "10003": tob_staff_app_group, "10018": tob_fellow_app_group}
            app_id_group = group_dict.get(target_app_id, [target_app_id])
            account_id = env["app_message_keeper"][data_key][int(target_app_id)]["user1"]["account_id"]
            # if "tob" in data_key:
            #     account_id = employee_id_converter(user_id)
            # else:
            #     account_id = user_id
            inputs = {
                "host": host,
                "path": "/api/2/in/message_keeper/history_unread_num",
                "method": "GET",
                "headers": {"content-type": "application/x-www-form-urlencoded"},
                "params": {
                    "region": "cn",
                    "lang": "zh-cn",
                    'nonce': 'nondceafadfdasfadfa',
                    "hash_type": "sha256",
                    "app_id": app_id,
                    'account_id': account_id,
                    'target_app_id': target_app_id,
                    # 'categories': categories,
                    # 'show_sub_app': True,
                    'sign': ''
                }
            }
            response = hreq.request(env, inputs)
            data = response['data']
            logger.debug(data)
            table = 'history_' + str(account_id)[-3:]
            unread_num_in_mysql = mysql[data_key].fetch(table, fields=['count(1) as unread_num'], where_model={'user_id': account_id, 'read': 0, 'app_id in': app_id_group})
            assert int(unread_num_in_mysql[0]['unread_num']) == int(data)

    @pytest.mark.parametrize('host_key, data_key,target_app_id,categories',
                             [
                                 ('app_tob_in', 'nmp_app_tob', "10003", "p0,p1"),
                                 ('app_tob_in', 'nmp_app_tob', "10018", "community,car_order"),
                                 ('app_in', 'nmp_app', "10001", "activity,default"),
                                 ('app_in', 'nmp_app', "10002", "activity,default"),
                             ])
    def test_history_unread_num_by_category(self, env, mysql, cmdopt, host_key, data_key, target_app_id, categories):
        with allure.step(f'{host_key}获取未读消息数量接口'):
            host = env['host'][host_key]
            toc_nio_app_group, tob_staff_app_group, tob_fellow_app_group = ["10001", "10002"], ["10003"], ["10018"]
            group_dict = {"10001": toc_nio_app_group, "10002": toc_nio_app_group, "10003": tob_staff_app_group, "10018": tob_fellow_app_group}
            app_id_group = group_dict.get(target_app_id, [target_app_id])
            account_id = env["app_message_keeper"][data_key][int(target_app_id)]["user1"]["account_id"]
            inputs = {
                "host": host,
                "path": "/api/2/in/message_keeper/history_unread_num",
                "method": "GET",
                "params": {
                    "region": "cn",
                    "lang": "zh-cn",
                    'nonce': 'nondceafadfdasfadfa',
                    "hash_type": "sha256",
                    "app_id": 10000,
                    'account_id': account_id,
                    'target_app_id': target_app_id,
                    'categories': categories,
                    'sign': ''
                }
            }
            response = hreq.request(env, inputs)
            details = response['data']
            logger.debug(details)
            with allure.step("校验mysql"):
                # 接口中category为0的会返回，查数据库统计为0的无值所以需要特殊处理一下
                table = 'history_' + str(account_id)[-3:]
                for data in details:
                    category = data.get("category")
                    unread_num_in_data = data.get("unread_num")
                    unread_num_in_mysql = mysql[data_key].fetch(table, fields=['count(1) as unread_num, category'],
                                                                where_model={'user_id': account_id, 'read': 0, 'category': category, 'app_id in': app_id_group})
                    assert int(unread_num_in_mysql[0]['unread_num']) == int(unread_num_in_data)
