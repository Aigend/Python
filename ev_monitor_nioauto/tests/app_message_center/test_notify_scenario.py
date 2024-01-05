# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_notify_case.py
# @Author : qiangwei.zhang
# @time: 2022/02/24
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import allure
import pytest
import json
from utils.http_client import TSPRequest as hreq
from utils.logger import logger

push_notify_one_config_cn_keys = "case_name,category,target_app_id,channel,host_key,data_key,scenario,user_id"
push_notify_one_config_cn_cases = [
    # TOC服务 10001 允许的category测试案例
    ("蔚来APP事件推广通知", 'notification', "10001", 'all', "app_in", "nmp_app", "ls_event", "user_id"),
    ("蔚来APP系统消息", 'notification', "10001", 'all', "app_in", "nmp_app", "ls_system", "user_id"),
    ("蔚来APP评论回复通知", 'notification', "10001", 'all', "app_in", "nmp_app", "ls_comment", "user_id"),
    ("蔚来APP内容推广通知", 'notification', "10001", 'all', "app_in", "nmp_app", "ls_content", "user_id"),
    ("蔚来APP直播推广通知", 'notification', "10001", 'all', "app_in", "nmp_app", "ls_livestream", "user_id"),
    ("蔚来APP直播抽奖中奖消息", 'notification', "10001", 'all', "app_in", "nmp_app", "ls_lottery", "user_id"),
    ("带有跳转的通知", 'notification', "10001", 'all', "app_in", "nmp_app", "ls_link", "user_id"),
]
push_notify_one_config_cn_ids = [f"{case[0]}" for case in push_notify_one_config_cn_cases]


@pytest.mark.parametrize(push_notify_one_config_cn_keys, push_notify_one_config_cn_cases, ids=push_notify_one_config_cn_ids)
def test_push_notify_scenario_cn(env, cmdopt, mysql, case_name, category, channel, host_key, data_key, target_app_id, scenario, user_id):
    if cmdopt not in ["test", "stg", "test_alps"]:
        logger.debug(f"该案例只在cn环境执行")
        return 0
    scenario_dict = {
        # 蔚来APP事件推广通知
        "ls_event": {
            "title": "事件推广标题",
            "description": "事件推广简述",
            "event_id": "事件ID，用于获取事件详情",
        },
        # 蔚来APP系统消息
        "ls_system": {
            "title": "通知标题",
            "description": "通知简述",
            "target_link": "https://www.baidu.com/",
            "url": "http://pangu.nioint.com/login_user",
        },
        # 蔚来APP评论回复通知
        "ls_comment": {
            "title": "通知标题",
            "description": "通知简述",
            "from_user_name": "评论者的用户名",
            "comment_id": "评论ID",
            "comment": "评论内容",
            "resource_id": "content_id",
            "resource_type": "content",
            "content_type": "只有评论类型是content的时候才有这个字段",
        },
        # 蔚来APP内容推广通知
        "ls_content": {
            "title": "通知标题",
            "description": "通知简述",
            "content_id": "内容ID，用于获取内容详情",
            "content_type": "内容类型"
        },
        # 蔚来APP直播推广通知
        "ls_livestream": {
            "title": "直播标题",
            "description": "直播简介",
            "content_id": "内容ID，用于获取内容详情",
            "content_type": "内容类型"
        },
        # 蔚来APP直播抽奖中奖消息
        "ls_lottery": {
            "title": "通知标题",
            "description": "通知简述",
            "is_lead_to_address": "no",
        },
        # 带有跳转的通知
        "ls_link": {
            "title": "通知标题",
            "description": "通知简述",
            "link_value": "https://www.baidu.com/",
            "show_navigator": "true",
            "load_js_bridge": "true",
            "load_action": "true",
            "pass_through": "true",
        }
    }
    user_id = env["app_message_keeper"]["nmp_app"][10001]["user1"]["account_id"]
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
            'scenario': scenario,
            'channel': channel,
            "category": category,
            'payload': json.dumps(scenario_dict.get(scenario), ensure_ascii=False)

        },
    }
    if not category:
        inputs["data"].pop("category")
    response = hreq.request(env, inputs)
    with allure.step("校验result_code"):
        assert response['result_code'] == 'success'
        message_id = response['data'].pop('message_id', '')
    with allure.step("校验mysql"):
        message_in_mysql = mysql[data_key].fetch(f'history_{str(user_id)[-3:]}', {'user_id': user_id, 'message_id': message_id}, retry_num=30)
        assert len(message_in_mysql) == 1
