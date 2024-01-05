# -*- coding: utf-8 -*-
# @Project : cvs_basic_autotest
# @File : test_notify_email.py
# @Author : qiangwei.zhang.o
# @CreateTime : 2021/3/16 6:04 下午
# @Description :
"""
/api/2/in/message/employee/email_push
    接口文档：http://showdoc.nevint.com/index.php?s=/13&page_id=30487
    检查点
        mysql：
            * email_history 历史消息
            * email_history_meta_info 消息内容
        redis:
            *无
    字段：
        * recipients  #接口文档需修改
            1.一次最多100
            2.账户重复，无去重复逻辑
            3.以英文逗号做分割的字符串，前后不能有空格
        * subject
            1.必填校验
            2.长度，接口未加限制
            3.支持字符串类型
        * content
            1.必填校验
            2.长度，接口未加限制
            3.支持 text+html5
        * sender_name
            1.非必填，默认
                * notification@nio.io 默认项
                * notification@nio.com
                * tsp@nioint.com
            2.二选一
            3.只能一个发件人
1.选择发件人tsp@nioint.com
2.选择发件人notification@nio.com
3.不填写发件人字段
4.填写发件人字段,发件人字段为空
5.填写发件人字段,发件人为其他邮箱
"""

import time
import pytest
import allure
from utils.http_client import TSPRequest as hreq
from data.email_content import long_text, html5
from utils.collection_message_states import collection_message_states
from utils.logger import logger

notify_email_employee_path = "/api/2/in/message/employee/email_push"
email_direct_push_employee_path = "/api/2/in/message/employee/email_direct_push"
app_id = 10000

cn_sender_name_list = ['tsp@nioint.com', 'notification@nio.com', 'nio_pay@nioint.com']
eu_sender_name_list = ['tsp@nioint.com', 'notification@nio.com', 'nio_pay@nioint.com']


@pytest.mark.run(order=1)
class TestPushEmailEmployee(object):
    notify_email_employee_keys = 'case_name,host_key,data_key,recipients'
    notify_email_employee_cases = [
        # --------------TOC服务--------------
        ("正案例_TOC_公司员工邮箱xxx.xx@nio.com", 'app_in', 'nmp_app', "qiangwei.zhang@nio.com"),
        ("反案例_TOC_qq邮箱非nio邮箱", 'app_in', 'nmp_app', "550736273@qq.com"),
        ("反案例_TOC_非邮箱格式", 'app_in', 'nmp_app', "qiangwei.zhang.nio.com"),
        ("反案例_TOC_非邮箱格式", 'app_in', 'nmp_app', None),
        # # --------------TOB服务--------------
        ("正案例_TOB_公司员工邮箱xxx.xx@nio.com", 'app_tob_in', 'nmp_app_tob', "qiangwei.zhang@nio.com"),
        ("反案例_TOB_qq邮箱非nio邮箱", 'app_tob_in', 'nmp_app_tob', "550736273@qq.com"),
        ("反案例_TOB_非邮箱格式", 'app_tob_in', 'nmp_app_tob', "qiangwei.zhang.nio.com"),
        ("反案例_TOB_非邮箱格式", 'app_tob_in', 'nmp_app_tob', None),
    ]
    notify_email_employee_ids = [f"{case[0]}" for case in notify_email_employee_cases]

    @pytest.mark.parametrize(notify_email_employee_keys, notify_email_employee_cases, ids=notify_email_employee_ids)
    def test_notify_email_employee(self, env, cmdopt, case_name, mysql, redis, host_key, data_key, recipients):
        time.sleep(1)  # 有频率限制
        with allure.step(f"员工发送邮件接口：{case_name}"):
            # if host_key == "app_tob_in" and cmdopt not in ['test_marcopolo', 'stg_marcopolo']:
            #     logger.debug(f"【{cmdopt}】环境暂不支持{host_key}服务邮件推送")
            #     return 0
            category = 'fellowMessage'  # marketing_email,fellow_contact
            inputs = {
                "host": env['host'][host_key],
                "path": notify_email_employee_path,
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
                    "content": f"员工发送邮件接口：{case_name}",
                }
            }
            response = hreq.request(env, inputs)
            with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
                if "test" in cmdopt:
                    redis["app_message"].delete(f"rate.limiting:{app_id}")
            if case_name.startswith("反案例"):
                assert response['result_code'] == 'invalid_param'
                if recipients:
                    assert response['debug_msg'] == 'not a nio employee recipient.'
                else:
                    assert response['debug_msg'] == 'necessary parameters are null.'
            else:
                assert response['result_code'] == 'success'
                assert response['data']["details"][0]["result"] == 'success', f"{response['data']['details'][0]['recipient']}邮件发送失败request_id:{response['request_id']}"
                with allure.step("校验mysql"):
                    message_id = response['data']['message_id']
                    email_history = mysql[data_key].fetch('email_history', {'message_id': message_id}, ['recipient'])
                    recipient_list = recipients.split(',')
                    for email_history_info in email_history:
                        assert (email_history_info['recipient'] in recipient_list) == True
                    email_content = mysql[data_key].fetch('email_history_meta_info', {'message_id': message_id})
                    assert len(email_content) == 1

    notify_email_employee_batch_keys = 'case_name,host_key,data_key,recipients'
    notify_email_employee_batch_cases = [
        # --------------TOC服务--------------
        ("正案例_TOC_公司员工邮箱", 'app_in', 'nmp_app', "qiangwei.zhang@nio.com,qiangwei.zhang.o@nio.com"),
        ("反案例_TOC_部分是公司员工邮箱", 'app_in', 'nmp_app', "qiangwei.zhang@nio.com,550736273@qq.com,qiangwei.zhang@nio.io,qiangwei.zhang.o@nio.io"),
        ("反案例_TOC_全不是员工邮箱", 'app_in', 'nmp_app', "qwewcdesksusj,550736273@qq.com,124566@163.com,qiangwei.zhang.o@nio.io"),
        # --------------TOB服务--------------
        ("正案例_TOB_公司员工邮箱xxx.xx@nio.com", 'app_tob_in', 'nmp_app_tob', "qiangwei.zhang@nio.com"),
    ]
    notify_email_employee_batch_ids = [f"{case[0]}" for case in notify_email_employee_batch_cases]

    @pytest.mark.parametrize(notify_email_employee_batch_keys, notify_email_employee_batch_cases, ids=notify_email_employee_batch_ids)
    def test_notify_email_employee_batch(self, env, cmdopt, case_name, mysql, redis, host_key, data_key, recipients):
        with allure.step(f"员工发送邮件接口：{case_name}"):
            category = 'fellowMessage'  # marketing_email,fellow_contact
            inputs = {
                "host": env['host'][host_key],
                "path": notify_email_employee_path,
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
                    "content": f"员工发送邮件接口：{case_name}",
                }
            }
            response = hreq.request(env, inputs)
            with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
                if "test" in cmdopt:
                    redis["app_message"].delete(f"rate.limiting:employee/email_push_{app_id}")
            if case_name.startswith("反案例"):
                assert response['result_code'] == 'invalid_param'
                if recipients:
                    assert response['debug_msg'] == 'not a nio employee recipient.'
                else:
                    assert response['debug_msg'] == 'necessary parameters are null.'

            else:
                assert response['result_code'] == 'success'
                assert response['data']["details"][0]["result"] == 'success', f"{response['data']['details'][0]['recipient']}邮件发送失败request_id:{response['request_id']}"
                with allure.step("校验mysql"):
                    message_id = response['data']['message_id']
                    email_history = mysql[data_key].fetch('email_history', {'message_id': message_id}, ['recipient'])
                    recipient_list = recipients.split(',')
                    for email_history_info in email_history:
                        assert (email_history_info['recipient'] in recipient_list) == True
                    email_content = mysql[data_key].fetch('email_history_meta_info', {'message_id': message_id})
                    assert len(email_content) == 1

    notify_email_employee_send_name_cn_keys = 'case_name,sender_name,host_key,data_key'
    notify_email_employee_send_name_cn_cases = [
        # --------------TOC服务--------------
        ('正案例_TOC_默认发件人notification@nio.com', None, 'app_in', 'nmp_app'),
        ('正案例_TOC_白名单发件人notification@nio.com', "notification@nio.com", 'app_in', 'nmp_app'),
        ('正案例_TOC_白名单发件人nio_pay@nioint.com', "nio_pay@nioint.com", 'app_in', 'nmp_app'),
        ('反案例_TOC_非白名单发件人tsp@nioint.com', "tsp@nioint.com", 'app_in', 'nmp_app'),
        ('反案例_TOC_非白名单发件人notification@nio.io', "notification@nio.io", 'app_in', 'nmp_app'),
        ('反案例_TOC_非白名单发件人550736273@qq.com', '550736273@qq.com', 'app_in', 'nmp_app'),
    ]
    notify_email_employee_send_name_cn_ids = [f"{case[0]}_{case[1]}" for case in notify_email_employee_send_name_cn_cases]

    @pytest.mark.parametrize(notify_email_employee_send_name_cn_keys, notify_email_employee_send_name_cn_cases, ids=notify_email_employee_send_name_cn_ids)
    def test_notify_email_employee_send_name_cn(self, env, cmdopt, mysql, redis, case_name, sender_name, host_key, data_key):
        with allure.step(f"员工发送邮件接口：{case_name}"):
            if cmdopt not in ['test', 'stg']:
                logger.debug(f"【{cmdopt}】环境暂不支持该案例")
                return 0
            category = 'fellowMessage'  # ads, verify, fellowMessage
            recipients = "qiangwei.zhang@nio.com"

            http = {
                "host": env['host'][host_key],
                "path": notify_email_employee_path,
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
                    "sender_name": sender_name,
                    "recipients": recipients,
                    "subject": f"【{cmdopt}】环境time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                    "content": f"员工发送邮件接口：{case_name}",
                }
            }
            response = hreq.request(env, http)
            with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
                if "test" in cmdopt:
                    redis["app_message"].delete(f"rate.limiting:employee/email_push_{app_id}")
            with allure.step(f"校验员工发送邮件返回状态码"):
                if case_name.startswith("正案例"):
                    assert response['result_code'] == 'success'
                    assert response['data']["details"][0]["result"] == 'success', f"{response['data']['details'][0]['recipient']}邮件发送失败request_id:{response['request_id']}"
                else:
                    assert response['result_code'] == 'invalid_param'
                    assert response['debug_msg'] == 'invalid sender name'

    notify_email_employee_send_name_eu_keys = 'case_name,sender_name,host_key,data_key'
    notify_email_employee_send_name_eu_cases = [
        # --------------TOC服务--------------
        ('正案例_TOC_默认发件人notification@nio.io', None, 'app_in', 'nmp_app'),
        ('正案例_TOC_白名单发件人notification@nio.io', "notification@nio.io", 'app_in', 'nmp_app'),
        ('反案例_TOC_非白名单发件人notification@nio.com', "notification@nio.com", 'app_in', 'nmp_app'),
        ('反案例_TOC_非白名单发件人550736273@qq.com', '550736273@qq.com', 'app_in', 'nmp_app'),
        # --------------TOB服务--------------
        ('正案例_TOB_默认发件人notification@nio.io', None, 'app_tob_in', 'nmp_app_tob'),
        ('正案例_TOB_白名单发件人notification@nio.io', "notification@nio.io", 'app_tob_in', 'nmp_app_tob'),
        ('正案例_TOB_白名单发件人notification@nio.com', "notification@nio.com", 'app_tob_in', 'nmp_app_tob'),
        ('反案例_TOB_非白名单发件人550736273@qq.com', '550736273@qq.com', 'app_tob_in', 'nmp_app_tob'),
    ]
    notify_email_employee_send_name_eu_ids = [f"{case[0]}" for case in notify_email_employee_send_name_eu_cases]

    @pytest.mark.parametrize(notify_email_employee_send_name_eu_keys, notify_email_employee_send_name_eu_cases, ids=notify_email_employee_send_name_eu_ids)
    def test_notify_email_employee_send_name_eu(self, env, cmdopt, mysql, redis, case_name, sender_name, host_key, data_key):
        with allure.step(f"员工发送邮件接口：{case_name}"):
            if cmdopt not in ['test_marcopolo', 'stg_marcopolo']:
                logger.debug(f"【{cmdopt}】环境暂不支持该案例")
                return 0
            category = 'fellowMessage'  # ads, verify, fellowMessage
            recipients = "qiangwei.zhang@nio.com"

            http = {
                "host": env['host'][host_key],
                "path": notify_email_employee_path,
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
                    "sender_name": sender_name,
                    "recipients": recipients,
                    "subject": f"【{cmdopt}】环境time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                    "content": f"员工发送邮件接口：{case_name}",
                }
            }
            with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
                if "test" in cmdopt:
                    redis["app_message"].delete(f"rate.limiting:employee/email_push_{app_id}")
            response = hreq.request(env, http)
            with allure.step(f"校验员工发送邮件返回状态码"):
                if case_name.startswith("正案例"):
                    assert response['result_code'] == 'success'
                    assert response['data']["details"][0]["result"] == 'success', f"{response['data']['details'][0]['recipient']}邮件发送失败request_id:{response['request_id']}"
                else:
                    assert response['result_code'] == 'invalid_param'
                    assert response['debug_msg'] == 'invalid sender name'
    email_employee_direct_push_keys = 'case_name,host_key,data_key,recipients'
    email_employee_direct_push_cases = [
        # --------------TOC服务--------------
        ("正案例_TOC_公司员工邮箱xxx.xx@nio.com", 'app_in', 'nmp_app', "qiangwei.zhang@nio.com"),
        ("反案例_TOC_qq邮箱非nio邮箱", 'app_in', 'nmp_app', "550736273@qq.com"),
        ("反案例_TOC_非邮箱格式", 'app_in', 'nmp_app', "qiangwei.zhang.nio.com"),
        # --------------TOB服务--------------
        ("正案例_TOB_公司员工邮箱xxx.xx@nio.com", 'app_tob_in', 'nmp_app_tob', "qiangwei.zhang@nio.com"),
        ("反案例_TOB_qq邮箱非nio邮箱", 'app_tob_in', 'nmp_app_tob', "550736273@qq.com"),
        ("反案例_TOB_非邮箱格式", 'app_tob_in', 'nmp_app_tob', "qiangwei.zhang.nio.com"),
    ]
    email_employee_direct_push_ids = [f"{case[0]}" for case in email_employee_direct_push_cases]

    @pytest.mark.parametrize(email_employee_direct_push_keys, email_employee_direct_push_cases, ids=email_employee_direct_push_ids)
    def test_notify_email_employee_direct_push(self, env, cmdopt, case_name, mysql, redis, host_key, data_key, recipients):
        time.sleep(1)  # 有频率限制
        with allure.step(f"员工发送邮件接口：{case_name}"):
            if host_key == "app_tob_in" and cmdopt not in ['test_marcopolo', 'stg_marcopolo']:
                logger.debug(f"【{cmdopt}】环境暂不支持{host_key}服务邮件推送")
                return 0
            category = 'fellowMessage'  # marketing_email,fellow_contact
            app_id = 10000

            inputs = {
                "host": env['host'][host_key],
                "path": email_direct_push_employee_path,
                "method": "POST",
                "params": {
                    "region": "cn",
                    "lang": "zh-cn",
                    "hash_type": "sha256",
                    "app_id": app_id,
                    "sign": ""
                },
                "data": {
                    "recipients": recipients,
                    "subject": f"【{cmdopt}】环境time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                    "content": f"员工发送邮件接口：{case_name}",
                    "category": 'ads',
                }
            }
            response = hreq.request(env, inputs)
            # rate.limiting: marketing_sms_
            with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
                if "test" in cmdopt:
                    redis["app_message"].delete(f"rate.limiting:employee/email_direct_push_{app_id}")
            if case_name.startswith("反案例"):
                assert response['result_code'] == 'invalid_param'
                if recipients:
                    assert response['debug_msg'] == 'not a nio employee recipient.'
                else:
                    assert response['debug_msg'] == 'necessary parameters are null.'
            else:
                assert response['result_code'] == 'success'
                assert response['data']["details"][0]["result"] == 'success', f"{response['data']['details'][0]['recipient']}邮件发送失败request_id:{response['request_id']}"
                with allure.step("校验mysql"):
                    message_id = response['data']['message_id']
                    email_history = mysql[data_key].fetch('email_history', {'message_id': message_id}, ['recipient'])
                    recipient_list = recipients.split(',')
                    for email_history_info in email_history:
                        assert (email_history_info['recipient'] in recipient_list) == True
                    email_content = mysql[data_key].fetch('email_history_meta_info', {'message_id': message_id})
                    assert len(email_content) == 1
