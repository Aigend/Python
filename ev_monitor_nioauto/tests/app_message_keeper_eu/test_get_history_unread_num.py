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
        ("正案例_TOB_泰坦WEB获取history_unread_num_100417", "100417", 'app_tob_in', 'nmp_app_tob'),
        ("正案例_TOB_泰坦APP获取history_unread_num_1000014", "1000014", 'app_tob_in', 'nmp_app_tob'),
        ("正案例_TOC_IOS_NIOAPP获取history_unread_num_1000003", "1000003", 'app_in', 'nmp_app'),
        ("正案例_TOC_ANDROID_NIOAPP获取history_unread_num_1000004", "1000004", 'app_in', 'nmp_app'),
        ("正案例_TOC_official_website官网WEB获取history_unread_num_100404", "100404", 'app_in', 'nmp_app'),

    ]
    history_unread_num_ids = [f"{case[0]}" for case in history_unread_num_cases]

    @pytest.mark.parametrize(history_unread_num_keys, history_unread_num_cases, ids=history_unread_num_ids)
    def test_history_unread_num_total(self, env, mysql, cmdopt, case_name, target_app_id, host_key, data_key):

        with allure.step(f'{host_key}公司员工获取未读消息数量接口{case_name}'):
            host = env['host'][host_key]
            app_id = 10000
            tob_titan_group, toc_app_web_group = ["100417", "1000014"], ["1000003", "1000004", "100404"]
            group_dict = {"100417": tob_titan_group, "1000014": tob_titan_group, "1000003": toc_app_web_group, "1000004": toc_app_web_group, "100404": toc_app_web_group}
            app_id_group = group_dict.get(target_app_id, [target_app_id])
            user_id = env["app_message_keeper"][data_key][int(target_app_id)]["user1"]["account_id"]
            if "tob" in data_key:
                account_id = employee_id_converter(user_id)
            else:
                account_id = user_id
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
                    'account_id': user_id,
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

    @pytest.mark.parametrize('host_key, data_key',
                             [
                                 ('app_tob_in', 'nmp_app_tob'),
                                 ('app_in', 'nmp_app'),
                             ])
    def test_history_unread_num_by_category(self, env, mysql, cmdopt, host_key, data_key):
        with allure.step(f'{host_key}公司员工获取未读消息数量接口'):
            host = env['host'][host_key]
            user_id = env[data_key]['account_id']
            categories = "activity,default"
            if "tob" in data_key:
                account_id = employee_id_converter(user_id)
                target_app_id = 1000004
            else:
                account_id = user_id
                target_app_id = 1000003
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
                    'account_id': user_id,
                    'target_app_id': target_app_id,
                    'categories': categories,
                    'sign': ''
                }
            }
            response = hreq.request(env, inputs)
            datas = response['data']
            logger.debug(datas)
            with allure.step("校验mysql"):
                # 接口中category为0的会返回，查数据库统计为0的无值所以需要特殊处理一下
                table = 'history_' + str(account_id)[-3:]
                for data in datas:
                    category = data.get("category")
                    unread_num_in_data = data.get("unread_num")
                    unread_num_in_mysql = mysql[data_key].fetch(table, fields=['count(1) as unread_num, category'],
                                                                where_model={'user_id': account_id, 'read': 0, 'category': category})
                    assert int(unread_num_in_mysql[0]['unread_num']) == int(unread_num_in_data)
