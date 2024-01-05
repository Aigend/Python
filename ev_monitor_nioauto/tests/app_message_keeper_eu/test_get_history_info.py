# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_gistory_info.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/4 11:08 上午
# @Description :
"""
    http://showdoc.nevint.com/index.php?s=/647&page_id=30998
    获取历史信息
    /api/2/in/message_keeper/history_info
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
            *规则 {"C":101,"CC":102,"CW":103,"EU":104,"NC":105,"NI":106,"U":107,"W":108}
                ✅* 字母开头ID 字母对应的数字如上 101*10的6次方+位数 EU90313==104*1000000+90313=104090313
                ✅* 数字开头 9*10的8次方+原user_id的int值
        * target_app_id 开始位置 limit
            ✅* 必填
        show_sub_app
    """

import allure
import time
import pytest

from utils.assertions import assert_equal
from utils.httptool import request as rq
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from utils.employee_id_converter import employee_id_converter

# 100417 titan_web_tob
# 1000014 titan_app_tob
# 1000003 nio_app_ios_eu_toc
# 1000014 nio_app_android_eu_toc
# 100404 official_website_eu_toc

history_info_keys = "case_name,target_app_id,host_key,data_key"
history_info_cases = [
    ("正案例_TOB_泰坦WEB获取history_info_100417", "100417", 'app_tob_in', 'nmp_app_tob'),
    ("正案例_TOB_泰坦APP获取history_info_1000014", "1000014", 'app_tob_in', 'nmp_app_tob'),
    ("正案例_TOC_IOS_NIOAPP获取history_info_1000003", "1000003", 'app_in', 'nmp_app'),
    ("正案例_TOC_ANDROID_NIOAPP获取history_info_1000004", "1000004", 'app_in', 'nmp_app'),
    ("正案例_TOC_official_website官网WEB获取history_info_100404", "100404", 'app_in', 'nmp_app'),

]
history_info_ids = [f"{case[0]}" for case in history_info_cases]


@pytest.mark.parametrize(history_info_keys, history_info_cases, ids=history_info_ids)
def test_history_info(env, mysql, case_name, target_app_id, host_key, data_key):
    tob_titan_group, toc_app_web_group = ["100417", "1000014"], ["1000003", "1000004", "100404"]
    group_dict = {"100417": tob_titan_group, "1000014": tob_titan_group, "1000003": toc_app_web_group, "1000004": toc_app_web_group, "100404": toc_app_web_group}
    app_id_group = group_dict.get(target_app_id, [target_app_id])
    with allure.step(f'{host_key}公司员工获取消息内容接口{case_name}'):
        app_id = 10000
        host = env['host'][host_key]
        user_id = env["app_message_keeper"][data_key][int(target_app_id)]["user1"]["account_id"]
        if "tob" in data_key:
            account_id = employee_id_converter(user_id)
        else:
            account_id = user_id
        inputs = {
            "host": host,
            "path": "/api/2/in/message_keeper/history_info",
            "method": "GET",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                'account_id': user_id,
                'target_app_id': target_app_id,
                'sign': ''
            }
        }
        response = hreq.request(env, inputs)
        assert response["result_code"] == "success"
        datas = response['data']

        table = 'history_' + str(account_id)[-3:]
        for data in datas:
            category = data.get("category")
            unread_num = data.get("unread_num")
            message_id = data['msg'][0]['message_id']

            category_message_count_mysql = mysql[data_key].fetch(table, fields=['count(1) as message_count', "category"],
                                                                 where_model={'user_id': account_id, 'app_id in': app_id_group, 'category': category, "read": 0})
            assert int(category_message_count_mysql[0]["message_count"]) == int(unread_num)
            last_message_mysql = mysql[data_key].fetch(table, where_model={'user_id': account_id, 'app_id in': app_id_group, 'category': category},
                                                       suffix='order by  create_time desc')
            assert last_message_mysql[0]["message_id"] == message_id
