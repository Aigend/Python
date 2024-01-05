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

enable_cold_history = True

class TestMeesageAPI(object):
    history_list_keys = "case_name,target_app_id,host_key,data_key"
    history_list_cases = [
        ("正案例_TOB_泰坦WEB获取history_list_100417", "100417", 'app_tob_in', 'nmp_app_tob'),
        ("正案例_TOB_泰坦APP获取history_list_1000014", "1000014", 'app_tob_in', 'nmp_app_tob'),
        ("正案例_TOC_IOS_NIOAPP获取history_list_1000003", "1000003", 'app_in', 'nmp_app'),
        ("正案例_TOC_ANDROID_NIOAPP获取history_list_1000004", "1000004", 'app_in', 'nmp_app'),
        ("正案例_TOC_official_website官网WEB获取history_list_100404", "100404", 'app_in', 'nmp_app'),

    ]
    history_list_ids = [f"{case[0]}" for case in history_list_cases]

    @pytest.mark.parametrize(history_list_keys, history_list_cases, ids=history_list_ids)
    def test_history_list(self, env, case_name, target_app_id, host_key, data_key, mysql):
        with allure.step(f'公司员工获取消息列表接口{case_name}'):
            count = 50
            offset = 0

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
                "host": env['host'][host_key],
                "path": "/api/2/in/message_keeper/history_list",
                "method": "GET",
                "headers": {"Content-Type": "application/x-www-form-urlencoded"},
                "params": {
                    "region": "cn",
                    "lang": "zh-cn",
                    "hash_type": "sha256",
                    "app_id": app_id,
                    'account_id': user_id,
                    'target_app_id': target_app_id,
                    "offset": offset,
                    'count': count,
                    # 'nonce': 'nondceafadfdasfadfa',
                    # 'scenario': 'ls_system',
                    # 'categories': 'red_packet',
                    # 'show_sub_app': True,
                    # 'show_raw': True,
                    # 'show_unread': True,
                    # 'show_unsent': True,
                    # 'last_ts': int(time.time()*1000),
                    'sign': ''
                }
            }
            response = hreq.request(env, inputs)
            data = response['data']
            logger.debug(f"接口返回长度{len(data)}")
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
                logger.debug(f"接口返回长度{len(data)}")
