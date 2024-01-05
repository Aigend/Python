# -*- coding: utf-8 -*-
# @Project : cvs_basic_autotest
# @File : test_push_email.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/3/16 6:04 下午
# @Description :

import time
import os
import pytest
import allure
import string
import random

from utils.assertions import assert_equal
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from tests.app_message_center.test_data.file.file_path import file_path_map

eu_email_with_attachment_path = "/api/2/in/message/eu/email_direct_push"
allow_environment = ["test_marcopolo", "stg_marcopolo", "prod"]


@pytest.mark.run(order=1)
class TestPushEmailEU(object):
    eu_email_not_subscribe_with_attachment_keys = 'case_name,sender_name,category,white_app_id,recipients,file_path'
    eu_email_not_subscribe_with_attachment_cases = [
        ('正案例_默认发件人', None, 'order_email', '10000', "maplepurple1123@163.com", file_path_map.get("xlsx_path")),
        ('正案例_白名单发件人', "notification-test@nio.io", 'test_drive', '10000', "550736273@qq.com", file_path_map.get("xlsx_path")),
        ('正案例_白名单发件人', "notification-test@nio.io", 'verify', '10007', "550736273@qq.com", file_path_map.get("xlsx_path")),
        ('反案例_错误发件人', "qiangwei.zhang@nio.com", 'test_drive', '10000', "550736273@qq.com", file_path_map.get("xlsx_path")),
    ]
    eu_email_not_subscribe_with_attachment_ids = [f"{case[0]}" for case in eu_email_not_subscribe_with_attachment_cases]

    @pytest.mark.parametrize(eu_email_not_subscribe_with_attachment_keys, eu_email_not_subscribe_with_attachment_cases, ids=eu_email_not_subscribe_with_attachment_ids)
    def test_eu_email_not_subscribe_with_attachment(self, env, cmdopt, mysql, redis, case_name, sender_name, category, white_app_id, recipients, file_path):
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        time.sleep(1)
        file_name = os.path.basename(file_path)
        file_type = file_name.split('.')[-1]
        file_size = os.path.getsize(file_path)
        with allure.step(f"【{cmdopt}】环境,无需订阅{category}频道发送邮件:{case_name}"):
            http = {
                "host": env['host']['app_in'],
                "path": eu_email_with_attachment_path,
                "method": "POST",
                "params": {
                    "region": "eu",
                    "lang": "zh-cn",
                    "hash_type": "sha256",
                    "app_id": white_app_id,
                    "sign": ""
                },
                "data": {
                    "recipients": recipients,
                    "subject": f"【{cmdopt}】环境time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                    "content": f"employee send email test 附件文件名称:{file_name}文件类型:{file_type}文件大小(byte):{file_size}文件大小(M):{file_size / 1024 / 1024}",
                    "category": category,
                    "sender_name": sender_name,
                },
                "files": {"file": (file_name, open(file_path, "rb"))},
            }
            response = hreq.request(env, http)
            with allure.step(f"【{cmdopt}】环境,清理{white_app_id}频率限制"):
                if "test" in cmdopt:
                    redis["app_message"].delete(f"rate.limiting:{white_app_id}")
            if case_name.startswith("正案例"):
                assert response['result_code'] == 'success', f"result_code Except success Actual {response['result_code']}"
                assert response['data']["details"][0]["result"] == 'success', f"{response['data']['details'][0]['recipient']}邮件发送失败request_id:{response['request_id']}"
                message_id = response['data']['message_id']
                with allure.step("校验mysql"):
                    email_history = mysql['nmp_app'].fetch('email_history', {'message_id': message_id}, ['recipient'])
                    recipient_list = recipients.split(',')
                    for email_history_info in email_history:
                        assert email_history_info['recipient'] in recipient_list
                    email_content = mysql['nmp_app'].fetch('email_history_meta_info', {'message_id': message_id})
                    assert len(email_content) == 1
            else:
                expected_res = {
                    "result_code": "invalid_param",
                    "debug_msg": "invalid sender name"
                }
                response.pop('request_id')
                response.pop('server_time')
                assert_equal(expected_res, response)

    eu_email_not_subscribe_no_attachment_keys = 'case_name,sender_name,category,white_app_id,recipients'
    eu_email_not_subscribe_no_attachment_cases = [
        ('正案例_无附件', "notification-test@nio.io", 'test_drive', '10000', "550736273@qq.com"),
    ]
    eu_email_not_subscribe_no_attachment_ids = [f"{case[0]}" for case in eu_email_not_subscribe_no_attachment_cases]

    @pytest.mark.parametrize(eu_email_not_subscribe_no_attachment_keys, eu_email_not_subscribe_no_attachment_cases, ids=eu_email_not_subscribe_no_attachment_ids)
    def test_eu_email_not_subscribe_no_attachment(self, env, cmdopt, mysql, redis, case_name, sender_name, category, white_app_id, recipients):
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        with allure.step(f"【{cmdopt}】环境,无需订阅{category}频道发送邮件:{case_name}"):
            http = {
                "host": env['host']['app_in'],
                "path": eu_email_with_attachment_path,
                "method": "POST",
                "headers": {"Content-Type": "application/x-www-form-urlencoded"},
                "params": {
                    "region": "eu",
                    "lang": "zh-cn",
                    "hash_type": "sha256",
                    "app_id": white_app_id,
                    "sign": ""
                },
                "data": {
                    "recipients": recipients,
                    "subject": f"【{cmdopt}】环境time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                    "content": f"employee send email test 无附件",
                    "category": category,
                    "sender_name": sender_name,
                }
            }
            response = hreq.request(env, http)
            with allure.step(f"【{cmdopt}】环境,清理{white_app_id}频率限制"):
                if "test" in cmdopt:
                    redis["app_message"].delete(f"rate.limiting:{white_app_id}")
            assert response['result_code'] == 'success'
            assert response['data']["details"][0]["result"] == 'success', f"{response['data']['details'][0]['recipient']}邮件发送失败request_id:{response['request_id']}"
            message_id = response['data']['message_id']
            with allure.step("校验mysql"):
                email_history = mysql['nmp_app'].fetch('email_history', {'message_id': message_id}, ['recipient'])
                recipient_list = recipients.split(',')
                for email_history_info in email_history:
                    assert (email_history_info['recipient'] in recipient_list) == True
                email_content = mysql['nmp_app'].fetch('email_history_meta_info', {'message_id': message_id})
                assert len(email_content) == 1
