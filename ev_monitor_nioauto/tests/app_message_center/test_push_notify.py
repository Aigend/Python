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
            ✅* 多个正常用户有重复 --
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
            ✅* ls_system
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
            ⏸* 0 显示在通知栏
            ⏸* 1 不显示在通知栏
            ⏸* 不传，默认0
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
            ⏸* mqtt
            ⏸* mipush
            ⏸️* apns
            ⏸* hwpush
            ⏸* fcm
            ✅* 不传，默认all

{
"1000003":["inbox","activity"],
"1000004":["inbox","activity"],
"100404":["inbox","activity"],
"1000014":["user","test_drive","order","delivery","service","power","care","interactive","used_car","system","silent"],
"100417":["in_box","activity"],
"10001":["comment","activity","notification","logistics","red_packet","remotecontrol","orderstatus","social_events","community_invitation","likes","reply"],
"10002":["comment","activity","notification","logistics","red_packet","remotecontrol","orderstatus","social_events","community_invitation","likes","reply"],
"10003":["p0","p1"],
"10018":["community","car_order","leads","pe_order","refund_order","credit_detail","community_invitation","web_link","stock_car","order_price_confirm","test_drive_order","task_leads","task","service_order","order_commodity","order_substitution","test_drive_leads","leads_distribute","leads_activity","test_driveprocess_order","test_drive_escort_order","car_pay_order","price_confirmation","car_payloans_order","stock_release_car","unbind_car_order","car_transport_order","car_delivery_order","reserved_car_order","chargeback_car_order","drawback_order","task_expire","drive_task","car_replacement_order","red_packet","car_update_order","purchase_order","distribute_order","integral_activity","numerical_selection_order","regional_sales_promotion","leads_correlation","leads_alternative","test_drive_alternative","car_order_alternative","task_alternative","other_alternative"]
}
"""

import json
import random
import string
import time
import allure
import pytest
from utils.logger import logger
from utils.http_client import TSPRequest as hreq
from utils.employee_id_converter import employee_id_converter
from data.email_content import html5_new1
from utils.assertions import assert_equal

server_app_id = 10000


class TestNotify(object):
    @pytest.mark.parametrize('category, channel, host_key, data_key, num',
                             [
                                 ('activity', 'all', "app_in", "nmp_app", 10),
                             ])
    def test_push_notify_batch(self, env, cmdopt, mysql, category, channel, host_key, data_key, num):
        if cmdopt in ["test", "stg", "test_alps"]:
            target_app_ids = "10001,10002"
        elif cmdopt in ["test_marcopolo", "stg_marcopolo"]:
            target_app_ids = "1000003,1000004"
        employee_ids = mysql[data_key].fetch("bindings", where_model={'visible': 1, 'user_id>': 1000, 'app_id in': target_app_ids.split(",")}, fields=["account_id", "user_id"],
                                             suffix=f"limit {num}")
        user_ids = ""
        app_id = 10000
        for uid in employee_ids:
            if "tob" in data_key:
                key = "account_id"
            else:
                key = "user_id"
            if not user_ids:
                user_ids = str(uid.get(key))
            else:
                user_ids = user_ids + "," + str(uid.get(key))
        http = {
            "host": env['host'][host_key],
            "path": "/api/2/in/message/app_notify",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                "sign": ''
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCA',
                'account_ids': user_ids,
                'ttl': 100000,
                'target_app_ids': target_app_ids,
                'do_push': True,
                'scenario': 'ls_link',
                'channel': channel,
                "category": category,
                "pass_through": 0,
                "store_history": True,
                'payload': json.dumps({
                    "target_link": "http://www.niohome.com",
                    "description": f"时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} category:{category}",
                    "title": f"【{cmdopt}】环境{channel}渠道推送测试"
                })
            },
        }
        response = hreq.request(env, http)
        assert response['result_code'] == 'success'
        message_id = response['data'].pop('message_id', '')
        with allure.step("校验mysql"):
            for uid in user_ids.split(','):
                if 'tob' in data_key:
                    account_id = employee_id_converter(uid)
                else:
                    account_id = uid
                message_in_mysql = mysql[data_key].fetch(f'history_{str(account_id)[-3:]}', {'user_id': account_id, 'message_id': message_id}, retry_num=30)
                assert len(message_in_mysql) == 1

    push_notify_one_keys = "case_name,category,channel,host_key,data_key,store_history"
    push_notify_one_cases = [
        # ("正案例_TOC_category不为None,store_history为True", 'inbox', 'apns', "app_in", "nmp_app", True),
        ("正案例_TOC_category不为None,store_history为True", 'inbox', 'all', "app_in", "nmp_app", True),
        # ("正案例_TOC_category不为None,store_history为False", 'activity', 'all', "app_in", "nmp_app", False),
        # ("反案例_TOC_category为None,store_history为True", None, 'all', "app_in", "nmp_app", True),
        # ("正案例_TOC_category为None,store_history为False", None, 'all', "app_in", "nmp_app", False),
        ("正案例_TOB_category不为None,store_history为True", 'default', 'all', "app_tob_in", "nmp_app_tob", True),
        ("正案例_TOB_category不为None,store_history为False", 'default', 'all', "app_tob_in", "nmp_app_tob", False),
        # ("反案例_TOB_category为None,store_history为True", None, 'all', "app_tob_in", "nmp_app_tob", True),
        # ("正案例_TOB_category为None,store_history为False", None, 'all', "app_tob_in", "nmp_app_tob", False),
    ]

    @pytest.mark.parametrize(push_notify_one_keys, push_notify_one_cases)
    def test_push_notify_one_eu(self, env, cmdopt, mysql, case_name, category, channel, host_key, data_key, store_history):
        if cmdopt not in ["test_marcopolo", "stg_marcopolo"]:
            logger.debug("eu环境测试案例")
            return 0
        user_id = env[data_key]['push_notify']['user2']['account_id']
        user_app_id = env[data_key]['push_notify']['user2']['app_id']
        # user_id = 1006908429
        # # user_app_id = 1000003
        target_app_ids = '10001,10002'
        if "marcopolo" in cmdopt:
            target_app_ids = '1000003,1000004'
            if "tob" in data_key:
                target_app_ids = user_app_id
        init_notify_account(env, mysql, data_key, host_key, user_id, user_app_id)
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
                'target_app_ids': target_app_ids,
                'do_push': True,
                'scenario': 'ls_link',
                'channel': channel,
                "category": category,
                # "pass_through": 0,
                "store_history": store_history,
                'payload': json.dumps({
                    "link_value": "http://www.niohome.com",
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
            time.sleep(5)
            if store_history:
                with allure.step("校验mysql"):
                    if 'tob' in data_key:
                        account_id = employee_id_converter(user_id)
                        logger.debug(f"员工ID{user_id}转化后ID为{account_id}")
                    else:
                        account_id = user_id
                    message_in_mysql = mysql[data_key].fetch(f'history_{str(account_id)[-3:]}', {'user_id': account_id, 'message_id': message_id}, retry_num=30)
                    assert len(message_in_mysql) == 1
        else:
            expected_res = {
                "result_code": "invalid_param",
                "debug_msg": "if store_history is true, then category is not allowed to be null"
            }
            response.pop("request_id")
            response.pop("server_time")

            assert_equal(expected_res, response)

    push_notify_one_config_cn_keys = "case_name,category,target_app_id,channel,host_key,data_key"
    push_notify_one_config_cn_cases = [
        # TOC服务 10001 允许的category测试案例
        ("正案例_TOC_category=default,target_app_id=10001", 'notification', "10001", 'all', "app_in", "nmp_app"),
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

    @pytest.mark.parametrize(push_notify_one_config_cn_keys, push_notify_one_config_cn_cases)
    def test_push_notify_one_config_cn(self, env, cmdopt, mysql, case_name, category, channel, host_key, data_key, target_app_id):
        """
        "10003":["p0","p1"],
        "10018":["community","car_order","leads","pe_order","refund_order","credit_detail","community_invitation","web_link","stock_car","order_price_confirm","test_drive_order","task_leads","task","service_order","order_commodity","order_substitution","test_drive_leads","leads_distribute","leads_activity","test_driveprocess_order","test_drive_escort_order","car_pay_order","price_confirmation","car_payloans_order","stock_release_car","unbind_car_order","car_transport_order","car_delivery_order","reserved_car_order","chargeback_car_order","drawback_order","task_expire","drive_task","car_replacement_order","red_packet","car_update_order","purchase_order","distribute_order","integral_activity","numerical_selection_order","regional_sales_promotion","leads_correlation","leads_alternative","test_drive_alternative","car_order_alternative","task_alternative","other_alternative"]
        """
        """
        
          "手机号": "98762775276",
          "验证码": "426308",
          "account_id": "301124399",
          ChABwhn2XZzGQvDgIDhfl16qEAEYgPwIIJFOKAE=

          "手机号": "98762775277",
          "验证码": "389698",
          "account_id": "151103551",
          ChDpbPXeKRl8cxsFq9ejgFtEEAEY__sIIJFOKAE=
          
          208575247
        """

        if cmdopt not in ["test", "stg", "test_alps"]:
            logger.debug(f"该案例只在cn环境执行")
            return 0
        user_id = env["app_message_keeper"][data_key][int(target_app_id)]["user1"]["account_id"]
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
                'ttl': 1000,
                'target_app_ids': target_app_id,
                'do_push': True,
                'scenario': 'ls_link',
                'channel': channel,
                "category": category,
                # "pass_through": 0,
                # "store_history": True,
                'payload': json.dumps({
                    "target_link": "nio://so/new_servicedetail?order_no=845158603307972101",
                    # "description": f"时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} category:{category};用户id:【{user_id}】channel:{channel}渠道推送测试用户id:{user_id}",
                    "description": "center description content",
                    "title": f"【{cmdopt}】环境center title"
                }, ensure_ascii=False)

            },
        }
        if not category:
            inputs["data"].pop("category")
        response = hreq.request(env, inputs)
        if case_name.startswith("正案例"):
            assert response['result_code'] == 'success'
            message_id = response['data'].pop('message_id', '')
            with allure.step("校验mysql"):
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

    push_notify_one_config_eu_keys = "case_name,category,target_app_id,channel,host_key,data_key"
    push_notify_one_config_eu_cases = [
        # TOC服务 1000004 允许的category测试案例
        ("正案例_TOC_category=default,target_app_id=1000004", 'default', "1000004", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=inbox,target_app_id=1000004", 'inbox', "1000004", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=activity,target_app_id=1000004", 'activity', "1000004", 'all', "app_in", "nmp_app"),
        ("反案例_TOC_category=logistics,target_app_id=1000004", 'logistics', "1000004", 'all', "app_in", "nmp_app"),
        # TOC服务 1000003 允许的category测试案例
        ("正案例_TOC_category=default,target_app_id=1000003", 'default', "1000003", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=inbox,target_app_id=1000003", 'inbox', "1000003", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=activity,target_app_id=1000003", 'activity', "1000003", 'all', "app_in", "nmp_app"),
        ("反案例_TOC_category=logistics,target_app_id=1000003", 'logistics', "1000003", 'all', "app_in", "nmp_app"),
        # TOC服务 100404 允许的category测试案例
        ("正案例_TOC_category=inbox,target_app_id=100404", 'inbox', "100404", 'all', "app_in", "nmp_app"),
        ("正案例_TOC_category=activity,target_app_id=100404", 'activity', "100404", 'all', "app_in", "nmp_app"),
        ("反案例_TOC_category=logistics,target_app_id=100404", 'logistics', "100404", 'all', "app_in", "nmp_app"),
        # TOB服务 100417 允许的category测试案例
        ("正案例_TOB_category=in_box,target_app_id=100417", 'in_box', "100417", 'all', "app_tob_in", "nmp_app_tob"),
        ("正案例_TOB_category=activity,target_app_id=100417", 'activity', "100417", 'all', "app_tob_in", "nmp_app_tob"),
        ("反案例_TOB_category=logistics,target_app_id=100417", 'logistics', "100417", 'all', "app_tob_in", "nmp_app_tob"),
        # TOB服务 1000014 允许的category测试案例
        ("正案例_TOB_category=user,target_app_id=1000014", 'user', "1000014", 'all', "app_tob_in", "nmp_app_tob"),
        ("正案例_TOB_category=test_drive,target_app_id=1000014", 'test_drive', "1000014", 'all', "app_tob_in", "nmp_app_tob"),
        ("正案例_TOB_category=order,target_app_id=1000014", 'order', "1000014", 'all', "app_tob_in", "nmp_app_tob"),
        ("正案例_TOB_category=delivery,target_app_id=1000014", 'delivery', "1000014", 'all', "app_tob_in", "nmp_app_tob"),
        ("正案例_TOB_category=service,target_app_id=1000014", 'service', "1000014", 'all', "app_tob_in", "nmp_app_tob"),
        ("正案例_TOB_category=power,target_app_id=1000014", 'power', "1000014", 'all', "app_tob_in", "nmp_app_tob"),
        ("正案例_TOB_category=care,target_app_id=1000014", 'care', "1000014", 'all', "app_tob_in", "nmp_app_tob"),
        ("正案例_TOB_category=interactive,target_app_id=1000014", 'interactive', "1000014", 'all', "app_tob_in", "nmp_app_tob"),
        ("正案例_TOB_category=used_car,target_app_id=1000014", 'used_car', "1000014", 'all', "app_tob_in", "nmp_app_tob"),
        ("正案例_TOB_category=system,target_app_id=1000014", 'system', "1000014", 'all', "app_tob_in", "nmp_app_tob"),
        ("正案例_TOB_category=silent,target_app_id=1000014", 'silent', "1000014", 'all', "app_tob_in", "nmp_app_tob"),
        ("反案例_TOB_category=logistics,target_app_id=1000014", 'logistics', "1000014", 'all', "app_tob_in", "nmp_app_tob"),
    ]
    push_notify_one_config_eu_ids = [f"{case[0]}" for case in push_notify_one_config_eu_cases]

    @pytest.mark.parametrize(push_notify_one_config_eu_keys, push_notify_one_config_eu_cases, ids=push_notify_one_config_eu_ids)
    def test_push_notify_one_config_eu(self, env, cmdopt, mysql, case_name, category, channel, host_key, data_key, target_app_id):

        if cmdopt not in ["test_marcopolo", "stg_marcopolo"]:
            logger.debug(f"该案例只在marco polo环境执行")
            return 0
        user_id = env["app_message_keeper"][data_key][int(target_app_id)]["user1"]["account_id"]
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
                    "description": f"时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} category:{category}{case_name}",
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
                if 'tob' in data_key:
                    account_id = employee_id_converter(user_id)
                    logger.debug(f"员工ID{user_id}转化后ID为{account_id}")
                else:
                    account_id = user_id
                message_in_mysql = mysql[data_key].fetch(f'history_{str(account_id)[-3:]}', {'user_id': account_id, 'message_id': message_id}, retry_num=30)
                assert len(message_in_mysql) == 1
        else:
            expected_res = {
                "result_code": "invalid_param",
                "debug_msg": "category is forbidden"
            }
            response.pop("request_id")
            response.pop("server_time")

            assert_equal(expected_res, response)

    def login_email_password(self, env, app_id=10001):
        email = "12345678@qq.com"
        password = "pan_gu@123456"
        inputs = {
            "host": env['host']['app_in'],
            "path": "/acc/2/in/login/email",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "app_id": app_id,
                'nonce': f"test{str(int(time.time() * 1000))}",
                "sign": ''
            },
            "data": {
                "email": email,
                "password_e": password,
                "device_id": '10001',
                "terminal": json.dumps({"app_id": "10001", "desc": "测试专属id"}),
                "origin_app_id": app_id,
                "remote_ip": "10.111.154.118",
            }
        }
        response_dict = hreq.request(env, inputs)
        return response_dict


def init_notify_account(env, mysql, data_key, host_key, account_id, app_id):
    cmdopt = env.get("cmdopt")
    if 'tob' in data_key and 'marcopolo' in cmdopt:
        account_id_c = employee_id_converter(account_id)
        clients = mysql[data_key].fetch("bindings", where_model={"user_id": account_id_c, "app_id": app_id}, fields=["message_id"], retry_num=5)
        logger.debug(f"员工ID{account_id}转化后ID为{account_id_c}")
    else:
        clients = mysql[data_key].fetch("bindings", where_model={"user_id": account_id, "app_id": app_id}, fields=["client_id", "visible"], retry_num=5)
    host = env['host'][host_key]
    if not clients:
        with allure.step('app_message_keeper服务注册client接口'):
            data_hw = {
                "target_app_id": app_id,
                "app_version": "8.5.1",
                "brand": "Huawei",
                "device_type": "android",
                "device_token": "HuaWei_" + "".join(random.sample(string.ascii_letters, 13)),
                "device_id": "".join(random.sample(string.ascii_letters, 13)),
                "os": "android",
                "os_version": "6.0.1",
                "push_type": "hwpush",
                "push_version": 1,
                "client_id": 1,
            }
            inputs = {
                "host": host,
                "path": "/api/2/in/message_keeper/register_client",
                "method": "POST",
                "headers": {"Content-Type": "application/x-www-form-urlencoded"},
                "params": {
                    "region": "cn",
                    "lang": "zh-cn",
                    "hash_type": "sha256",
                    "app_id": 10000,
                    'sign': ''
                },
                "data": data_hw
            }
            response = hreq.request(env, inputs)
            assert response["result_code"] == "success"
            client_id = response["data"]
            clients = mysql[data_key].fetch("clients", where_model={"client_id": client_id}, fields=["client_id", "visible"])
            assert len(clients) == 1
        with allure.step('app_message_keeper服务绑定client接口'):
            inputs = {
                "host": host,
                "path": "/api/2/in/message_keeper/bind_client",
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
                    "target_app_id": app_id,
                    "client_id": client_id,
                    "account_id": account_id,
                }
            }
            response = hreq.request(env, inputs)
            assert response["result_code"] == "success"
    else:
        client_bind_status_list = [int(client.get("visible")) for client in clients]
        if not any(client_bind_status_list):
            client_id = clients[0].get("client_id")
            with allure.step('app_message_keeper服务绑定client接口'):
                inputs = {
                    "host": host,
                    "path": "/api/2/in/message_keeper/bind_client",
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
                        "target_app_id": app_id,
                        "client_id": client_id,
                        "account_id": account_id,
                    }
                }
                response = hreq.request(env, inputs)
                assert response["result_code"] == "success"

    # with allure.step('app_message_keeper服务解绑client接口'):
    #     inputs = {
    #         "host": host,
    #         "path": "/api/2/in/message_keeper/unbind_client",
    #         "method": "POST",
    #         "headers": {"Content-Type": "application/x-www-form-urlencoded"},
    #         "params": {
    #             "region": "cn",
    #             "lang": "zh-cn",
    #             "hash_type": "sha256",
    #             "app_id": 10000,
    #             'sign': ''
    #         },
    #         "data": {
    #             "target_app_id": app_id,
    #             "client_id": client_id,
    #             "account_id": account_id,
    #         }
    #     }
    #     response = hreq.request(env, inputs)
    #     assert response["result_code"] == "success"
    #     clients = mysql[data_key].fetch("bindings", where_model={"client_id": client_id, "visible": 0})
    #     assert len(clients) == 1
