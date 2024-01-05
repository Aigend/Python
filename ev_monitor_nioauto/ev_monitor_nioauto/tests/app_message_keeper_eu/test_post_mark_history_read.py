# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_get_history_read.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/4 11:21 上午
# @Description :
"""
    http://showdoc.nevint.com/index.php?s=/647&page_id=31035
    将消息标记为已读
    /api/2/in/message_keeper/tob/history_read
    Query Parameters：
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
    Body Parameters
        * employee_id 用户ID
            ✅* 必填
            * 规则 {"C":101,"CC":102,"CW":103,"EU":104,"NC":105,"NI":106,"U":107,"W":108}
                ✅* 字母开头ID 字母对应的数字如上 101*10的6次方+位数 EU90313==104*1000000+90313=104090313
                ✅* 数字开头 9*10的8次方+原user_id的int值
        * target_app_id
            ✅* 必填
            ✅* 单个
        * message_ids
            * 最多50个
            ✅* 非必填
        ✅* categories
    """
import json

import allure
import time
import pytest

from tests.app_message_center.test_push_notify import init_notify_account
from utils.assertions import assert_equal
from utils.httptool import request as rq
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from utils.employee_id_converter import employee_id_converter

mark_history_read_keys = "case_name,target_app_id,host_key,data_key"
mark_history_read_cases = [
    ("正案例_TOB_泰坦WEB获取mark_history_read_100417", "100417", 'app_tob_in', 'nmp_app_tob'),
    ("正案例_TOB_泰坦APP获取mark_history_read_1000014", "1000014", 'app_tob_in', 'nmp_app_tob'),
    ("正案例_TOC_IOS_NIOAPP获取mark_history_read_1000003", "1000003", 'app_in', 'nmp_app'),
    ("正案例_TOC_ANDROID_NIOAPP获取mark_history_read_1000004", "1000004", 'app_in', 'nmp_app'),
    ("正案例_TOC_official_website官网WEB获取mark_history_read_100404", "100404", 'app_in', 'nmp_app'),

]
mark_history_read_ids = [f"{case[0]}" for case in mark_history_read_cases]


@pytest.mark.parametrize(mark_history_read_keys, mark_history_read_cases, ids=mark_history_read_ids)
def test_mark_history_read(env, cmdopt, mysql, case_name, target_app_id, host_key, data_key):
    with allure.step(f'{host_key}将消息标记未已读接口{case_name}'):
        user_id = env["app_message_keeper"][data_key][int(target_app_id)]["user1"]["account_id"]
        if "tob" in data_key:
            account_id = employee_id_converter(user_id)
        else:
            account_id = user_id
        table = f'history_{str(account_id)[-3:]}'
        message_id = push_notify(env, cmdopt, mysql, host_key, data_key, target_app_id, user_id)
        inputs = {
            "host": env['host'][host_key],
            "path": "/api/2/in/message_keeper/history_read",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": 10000,
                'sign': ''
            },
            "data": {
                "account_id": user_id,
                "target_app_id": target_app_id,
                "message_ids": message_id,
            }
        }
        response = hreq.request(env, inputs)

        assert response["result_code"] == "success"
    with allure.step('校验数据库中标记为已读'):
        message_in_mysql = mysql[data_key].fetch(table, {'user_id': account_id, 'message_id': message_id, "read": 1}, retry_num=30)
        assert len(message_in_mysql) == 1
    with allure.step('手动将数据标记改为未读'):
        if "stg" not in cmdopt:
            mysql[data_key].update(table, {"user_id": account_id, "message_id": message_id}, {"read": 0})


def push_notify(env, cmdopt, mysql, host_key, data_key, target_app_id, user_id):
    init_notify_account(env, mysql, data_key, host_key, user_id, target_app_id)
    inputs = {
        "host": env['host'][host_key],
        "path": "/api/2/in/message/app_notify",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "params": {
            "region": "cn",
            "lang": "zh-cn",
            "hash_type": "sha256",
            "app_id": "10000",
            "sign": ''
        },
        "data": {
            'nonce': 'MrVIRwkCLBKySgCA',
            'account_ids': user_id,
            'ttl': 100000,
            'target_app_ids': target_app_id,
            'do_push': True,
            'scenario': 'ls_link',
            'channel': "all",
            "category": "default",
            "pass_through": 0,
            "store_history": True,
            'payload': json.dumps({
                "target_link": "http://www.niohome.com",
                "description": f"时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "title": f"【{cmdopt}】环境;用户id:【{user_id}】渠道推送测试用户id:{user_id}"
            }, ensure_ascii=False)
        },
    }
    response = hreq.request(env, inputs)
    return response['data'].pop('message_id', '')
