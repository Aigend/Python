# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_get_history_list.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/5/26 3:14 下午
# @Description :
"""
        http://showdoc.nevint.com/index.php?s=/647&page_id=30948
        获取历史消息列表
        /api/2/in/message_keeper/history_list
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
            * employee_id 用户ID
                ✅* 必填
                *规则 {"C":101,"CC":102,"CW":103,"EU":104,"NC":105,"NI":106,"U":107,"W":108}
                     ✅* 字母开头ID 字母对应的数字如上 101*10的6次方+位数 EU90313==104*1000000+90313=104090313
                     ✅* 数字开头 9*10的8次方+原user_id的int值
            * offset 开始位置 limit
                ✅* 必填
            * count 数量
                ✅* 必填
            * scenario 场景
                ✅* 非必填
                ✅* 默认所有
                ✅* 指定场景
            * categories 类别
                ✅* 非必填，默认所有
                ✅* 最多30个
                ✅* 指定场景
            * show_sub_app
                ⏸️* 默认 false
                ⏸* true
                ⏸* false
            * show_raw 展示原始数据
                ✅* 默认 false
                ✅* true
                ✅* false
            * show_unread
                ✅* 非必填，默认 false 读取所有的
                ✅* true 只读取未读消息
                ✅* false 读取所有的消息
            * show_unsent
                ✅* 默认 false
                ✅* true 查询到未发送的会将状态改为10000
                ✅* false
            * last_ts 截止时间
                ✅* 13位时间戳
                ✅* 小于截止时间的数据
        """

import allure
import time
import pytest

from utils.assertions import assert_equal
from utils.httptool import request as rq
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from utils.employee_id_converter import employee_id_converter


class TestMeesageAPI(object):
    history_list_keys = "case_name,target_app_id,host_key,data_key"
    history_list_cases = [
        ("正案例_TOB_Android Staff APP 10003", "10003", 'app_tob_in', 'nmp_app_tob'),
        ("正案例_TOB_Android Fellow APP 10018", "10018", 'app_tob_in', 'nmp_app_tob'),
        ("正案例_TOC_IOS_NIO_APP 10002", "10002", 'app_in', 'nmp_app'),
        ("正案例_TOC_ANDROID_NIO_APP 10001", "10001", 'app_in', 'nmp_app'),

    ]
    history_list_ids = [f"{case[0]}" for case in history_list_cases]

    @pytest.mark.parametrize(history_list_keys, history_list_cases, ids=history_list_ids)
    def test_history_list(self, env, cmdopt, case_name, target_app_id, host_key, data_key, mysql):
        with allure.step(f'公司员工获取消息列表接口{case_name}'):
            max_count = 10
            app_id = 10000
            toc_nio_app_group, tob_staff_app_group, tob_fellow_app_group = ["10001", "10002"], ["10003"], ["10018"]
            group_dict = {"10001": toc_nio_app_group, "10002": toc_nio_app_group, "10003": tob_staff_app_group, "10018": tob_fellow_app_group}
            app_id_group = group_dict.get(target_app_id, [target_app_id])
            account_id = env["app_message_keeper"][data_key][int(target_app_id)]["user1"]["account_id"]
            inputs = {
                "host": env['host'][host_key],
                "path": "/api/2/in/message_keeper/history_list",
                "method": "GET",
                "headers": {"Content-Type": "application/x-www-form-urlencoded"},
                "params": {
                    "region": "cn",
                    "lang": "zh-cn",
                    "hash_type": "sha256",
                    "app_id": app_id,
                    'account_id': account_id,
                    'target_app_id': target_app_id,
                    "offset": 0,
                    'count': max_count,
                    'sign': ''
                }
            }
            response = hreq.request(env, inputs)
            data = response['data']
            logger.debug(f"接口返回长度{len(data)}")
            history = 'history_' + str(account_id)[-3:]
            cold_history = 'cold_history_' + str(account_id)[-3:]
            with allure.step("校验mysql"):
                message_in_mysql_history = mysql[data_key].fetch(history, fields=['count(1) as message_count'], where_model={'user_id': account_id, 'app_id in': app_id_group})
                if cmdopt in ["test"]:
                    message_in_mysql_cold_history = mysql[data_key].fetch(cold_history, fields=['count(1) as message_count'],
                                                                          where_model={'user_id': account_id, 'app_id in': app_id_group})
                    len_of_message_in_mysql = int(message_in_mysql_history[0]['message_count']) + int(message_in_mysql_cold_history[0]['message_count'])
                else:
                    len_of_message_in_mysql = int(message_in_mysql_history[0]['message_count'])
                len_of_message_in_mysql = len_of_message_in_mysql if len_of_message_in_mysql < max_count else max_count
                assert len_of_message_in_mysql == len(data)
                logger.debug(f"接口返回长度{len(data)}")
