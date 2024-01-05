# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto 
# @File : test_push_email_employee.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/3/16 6:04 下午
# @Description :
import time
import allure
import pytest
from utils.http_client import TSPRequest as hreq


class TestPushEmailEmployee(object):
    def test_notify_email_employee(self, env, cmdopt, mysql, redis):
        with allure.step(f"员工发送邮件接口"):
            category = 'fellowMessage'  # marketing_email,fellow_contact
            app_id = 10000
            data_key = 'nmp_app'
            recipients = 'qiangwei.zhang@nio.com'
            inputs = {
                "host": env['host']['app_in'],
                "path": "/api/2/in/message/employee/email_push",
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {
                    "region": "cn",
                    "lang": "zh-cn",
                    "hash_type": "sha256",
                    "app_id": app_id,
                    "sign": ""
                },
                "json": {
                    "recipients": recipients,
                    "subject": f"【{cmdopt}】环境time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                    "content": f"员工发送邮件接口",
                }
            }
            with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
                if "test" in cmdopt:
                    redis["app_message"].delete(f"rate.limiting:employee/email_push_{app_id}")
            response = hreq.request(env, inputs)
            assert response['result_code'] == 'success'
            with allure.step("校验mysql"):
                message_id = response['data']['message_id']
                email_history = mysql[data_key].fetch('email_history', {'message_id': message_id}, ['recipient'])
                recipient_list = recipients.split(',')
                for email_history_info in email_history:
                    assert email_history_info['recipient'] in recipient_list
                email_content = mysql[data_key].fetch('email_history_meta_info', {'message_id': message_id})
                assert len(email_content) == 1

    def test_notify_email_employee_batch(self, env, cmdopt, mysql, redis):
        with allure.step(f"员工发送邮件接口"):
            app_id = 10000
            recipients = 'qiangwei.zhang@nio.com,colin.li@nio.com'
            data_key = 'nmp_app'
            inputs = {
                "host": env['host']['app_in'],
                "path": "/api/2/in/message/employee/email_push",
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {
                    "region": "cn",
                    "lang": "zh-cn",
                    "hash_type": "sha256",
                    "app_id": app_id,
                    "sign": ""
                },
                "json": {
                    "recipients": recipients,
                    "subject": f"【BVT】【{cmdopt}】环境time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                    "content": f"【BVT】员工发送邮件接口",
                }
            }
            with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
                if "test" in cmdopt:
                    redis["app_message"].delete(f"rate.limiting:employee/email_push_{app_id}")
            response = hreq.request(env, inputs)
            assert response['result_code'] == 'success'
            with allure.step("校验mysql"):
                message_id = response['data']['message_id']
                email_history = mysql[data_key].fetch('email_history', {'message_id': message_id}, ['recipient'])
                recipient_list = recipients.split(',')
                for email_history_info in email_history:
                    assert email_history_info['recipient'] in recipient_list
                email_content = mysql[data_key].fetch('email_history_meta_info', {'message_id': message_id})
                assert len(email_content) == 1

    def test_notify_email_employee_recipients(self, env, cmdopt, redis):
        with allure.step(f"员工发送邮件接口"):
            recipients = "qiangwei.zhang@nio.com"
            category = 'fellowMessage'  # ads, verify, fellowMessage
            app_id = 10000
            http = {
                "host": env['host']['app_in'],
                "path": "/api/2/in/message/employee/email_push",
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {
                    "region": "cn",
                    "lang": "zh-cn",
                    "hash_type": "sha256",
                    "app_id": app_id,
                    "sign": ""
                },
                "json": {
                    "sender_name": None,
                    "recipients": recipients,
                    "subject": f"【BVT】【{cmdopt}】环境time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                    "content": f"【BVT】员工发送邮件接口",
                }
            }
            with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
                if "test" in cmdopt:
                    redis["app_message"].delete(f"rate.limiting:employee/email_push_{app_id}")
            response = hreq.request(env, http)
            with allure.step(f"校验员工发送邮件返回状态码"):
                assert response['result_code'] == 'success'
