# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_push_notify.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/5/13 4:36 下午
# @Description :
"""
   接口文档：http://showdoc.nevint.com/index.php?s=/647&page_id=30817
        account_ids
            ✅* 单个正常用户
            ✅* 单个异常用户 --有校验
            ✅* 不传
            ✅* 多个正常用户
            ✅* 多个正常用户,包含小米，苹果走all渠道推送
            ✅* 多个正常用户有重复 --未去重
            ✅* 多个全部异常用户  --error getting notify target
            ✅* 多个用户，部分正常部分异常  --一个异常，其他正常用户也返回发送失败
        payload
            ✅* JSON格式
                ✅* title --不传接口返回成功，无校验
                ✅* description --不传接口返回成功，无校验
            ✅* 非JSON格式 --
            ✅* 不传
        scenario 场景 透传，
            * https://nextevinc.sharepoint.cn/:x:/r/ConnectedVehicleService/_layouts/15/Doc.aspx?sourcedoc=%7B70075998-6626-4ACC-AA5C-CEA95F6674C2%7D&file=Message%20Senario.xlsx&action=default&mobileredirect=true
            * ls_event
            ✅* ls_system
            * ls_comment
            * ls_content
            * ls_livestream
            * ls_lottery
            * ls_link
            * 不传
        ttl
            * 消息在mqtt存活时间，最长7天
        target_app_ids
            ✅* 单个正常
            ✅* 多个全部正常
            ✅* 多个正常有重复
            ✅* 多个全部异常
            ✅* 部分正常部分异常
        store_history
            ✅* True 消息存入历史表
            ✅* False 消息不存入历史表
            ✅* 不传，默认为True
        pass_through 是否显示在通知栏
            ✅* 0 显示在通知栏
            ✅* 1 不显示在通知栏
            ✅* 不传，默认0
        category 信息的类别
            ✅* default 默认（app中显示在通知里）
            ✅* activity 活动
            ✅* red_packet 积分红包
            ✅* logistics 物流
            ✅* notification 通知
        do_push 是否做推送
            ✅* True 推送
            ✅* False 不推送
            ✅* 不传，默认为True
        channel 消息通道
            ✅* all
            ✅* mqtt
            ✅* mipush
            ✅* apns
            * hwpush
            * fcm
            * web
            ✅* 不传，默认all

   状态：
        receive(21) 收到请求,
        generate_msg(22) 生成消息,
        store_msg(23) 存储消息,
        generate_pushTask(24) 发送kafka到push,
        send_pushTask(25),
        send_to_thirdParty(26) 发送到第三方
"""

import json
import time
import random
import string

import allure
import pytest

from tests.app_message_center.test_push_notify import init_notify_account
from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq
from utils.logger import logger

server_app_id = 10000


class TestNotify(object):
    push_notify_one_config_cn_keys = "case_name,category,target_app_id,channel,host_key,data_key"
    push_notify_one_config_cn_cases = [
        # TOC服务 10001 允许的category测试案例
        ("正案例_TOC_category=default,target_app_id=10001", 'activity', "10001", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=notification,target_app_id=10001", 'notification', "10001", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=activity,target_app_id=10001", 'activity', "10001", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=logistics,target_app_id=10001", 'logistics', "10001", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=red_packet,target_app_id=10001", 'red_packet', "10001", 'all', "app_in", "nmp_app"),
        # TOC服务 10002 允许的category测试案例
        ("正案例_TOC_category=default,target_app_id=10002", 'activity', "10002", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=notification,target_app_id=10002", 'notification', "10002", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=activity,target_app_id=10002", 'activity', "10002", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=logistics,target_app_id=10002", 'logistics', "10002", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=red_packet,target_app_id=10002", 'red_packet', "10002", 'all', "app_in", "nmp_app"),
        ("反案例_TOC_category=inbox,target_app_id=10002", 'inbox', "10002", 'all', "app_in", "nmp_app"),
        # TOB服务 10003 允许的category测试案例
        ("正案例_TOB_category=p0,target_app_id=10003", 'p0', "10003", 'all', "app_tob_in", "nmp_app_tob"),
        ("正案例_TOB_category=p0,target_app_id=10003", 'default', "10003", 'all', "app_tob_in", "nmp_app_tob"),
        ("正案例_TOB_category=p1,target_app_id=10003", 'p1', "10003", 'all', "app_tob_in", "nmp_app_tob"),
        # TOB服务 10018 允许的category测试案例
        ("正案例_TOB_category=community,target_app_id=10018", 'community', "10018", 'all', "app_tob_in", "nmp_app_tob"),
        ("正案例_TOB_category=car_order,target_app_id=10018", 'car_order', "10018", 'all', "app_tob_in", "nmp_app_tob"),
    ]
    push_notify_one_config_cn_ids = [f"{case[0]}" for case in push_notify_one_config_cn_cases]

    @pytest.mark.parametrize(push_notify_one_config_cn_keys, push_notify_one_config_cn_cases, ids=push_notify_one_config_cn_ids)
    def test_push_notify_one_config_cn(self, env, cmdopt, mysql, case_name, category, channel, host_key, data_key, target_app_id):
        """
        "10003":["p0","p1"],
        "10018":["community","car_order","leads","pe_order","refund_order","credit_detail","community_invitation","web_link","stock_car","order_price_confirm","test_drive_order","task_leads","task","service_order","order_commodity","order_substitution","test_drive_leads","leads_distribute","leads_activity","test_driveprocess_order","test_drive_escort_order","car_pay_order","price_confirmation","car_payloans_order","stock_release_car","unbind_car_order","car_transport_order","car_delivery_order","reserved_car_order","chargeback_car_order","drawback_order","task_expire","drive_task","car_replacement_order","red_packet","car_update_order","purchase_order","distribute_order","integral_activity","numerical_selection_order","regional_sales_promotion","leads_correlation","leads_alternative","test_drive_alternative","car_order_alternative","task_alternative","other_alternative"]
        """
        if cmdopt not in ["test", "stg", "test_alps"]:
            logger.debug(f"该案例只在cn环境执行")
            return 0

        user_id = env["app_message_keeper"][data_key][int(target_app_id)]["user1"]["account_id"]
        init_notify_account(env, mysql, data_key, host_key, user_id, app_id=target_app_id)
        inputs = {
            "host": env['host'][host_key],
            "path": "/api/2/in/message/app_notify",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": server_app_id,
                "sign": ''
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCA',
                'account_ids': user_id,
                'ttl': 100000,
                'target_app_ids': target_app_id,
                'do_push': True,
                'scenario': 'ls_link',
                'channel': channel,
                "category": category,
                "pass_through": 0,
                "store_history": True,
                'payload': json.dumps({
                    "target_link": "http://www.niohome.com",
                    "description": f"时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} category:{category}",
                    "title": f"【{cmdopt}】环境;用户id:【{user_id}】channel:{channel}渠道推送测试用户id:{user_id}"
                })
            },
        }
        if not category:
            inputs["data"].pop("category")
        response = hreq.request(env, inputs)
        if case_name.startswith("正案例"):
            assert response['result_code'] == 'success'
            message_id = response['data'].pop('message_id', '')
            with allure.step("校验mysql"):
                # if 'tob' in data_key:
                #     account_id = employee_id_converter(user_id)
                #     logger.debug(f"员工ID{user_id}转化后ID为{account_id}")
                # else:
                #     account_id = user_id
                message_in_mysql = mysql[data_key].fetch(f'history_{str(user_id)[-3:]}', {'user_id': user_id, 'message_id': message_id}, retry_num=30)
                assert len(message_in_mysql) == 1
        else:
            expected_res = {
                "result_code": "invalid_param",
                "debug_msg": "category is forbidden"
            }
            response.pop("request_id")
            response.pop("server_time")

            assert_equal(expected_res, response)
