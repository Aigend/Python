# -*- coding: utf-8 -*-
# @Project : cvs_basic_autotest
# @File : test_notify_email.py
# @Author : qiangwei.zhang.o
# @CreateTime : 2021/3/16 6:04 下午
# @Description :
"""
            接口文档：http://showdoc.nevint.com/index.php?s=/13&page_id=30141
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
                * category
                    1.必填
                    2.字典校验，无校验
                        ads, verify, fellowMessage

        """

import time
import pytest
import allure
import string
import random
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from data.email_content import long_text, html5
from utils.collection_message_states import collection_message_states
from utils.assertions import assert_equal
from utils.validation_data_format import validation_email_format
from utils.random_tool import random_string

allow_environment = ["test", "stg", "test_alps"]


@pytest.mark.run(order=1)
class TestPushEmailCN(object):
    push_cn_email_keys = 'case_name,recipients,host_key,data_key'
    push_cn_email_cases = [
        ("正案例_TOC_单个收件人", "550736273@qq.com", 'app_in', 'nmp_app'),
        ("反案例_TOC_收件人为None", None, 'app_in', 'nmp_app'),
        ("反案例_TOC_105个收件人大于100个", ','.join([f"{random_string(12)}@qq.com" for i in range(105)]), 'app_in', 'nmp_app'),
    ]
    ids = [f"{case[0]}" for case in push_cn_email_cases]

    @pytest.mark.parametrize(push_cn_email_keys, push_cn_email_cases, ids=ids)
    def test_push_cn_email(self, env, cmdopt, mysql, redis, case_name, recipients, host_key, data_key):
        category = 'fellowMessage'  # ads, verify, fellowMessage
        app_id = 10000
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete(f"rate.limiting:cn/email_push_{app_id}")
                # redis["app_message"].delete(f"rate.limiting:{app_id}")
        time.sleep(1)  # 有频率限制
        with allure.step(f"【{cmdopt}】环境，CN发送邮件接口{case_name}"):

            inputs = {
                "host": env['host'][host_key],
                "path": "/api/2/in/message/cn/email_push",
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
                    "subject": f"【{cmdopt}】环境cn接口:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                    "content": "cn send email test",
                    "category": category,
                }
            }
            response = hreq.request(env, inputs)
            if case_name.startswith("正案例"):
                assert response['result_code'] == 'success'
                assert response['data']["details"][0]["result"] == 'success', f"{response['data']['details'][0]['recipient']}邮件发送失败request_id:{response['request_id']}"
                message_id = response['data']['message_id']
                expected_states = [21, 22, 23, 24, 26]
                ms_st = f"{message_id}|{expected_states}|/api/2/in/message/cn/email_push"
                collection_message_states(cmdopt, ms_st)
                with allure.step("校验mysql"):
                    email_history = mysql[data_key].fetch('email_history', {'message_id': message_id}, ['recipient'])
                    recipient_list = recipients.split(',')
                    for email_history_info in email_history:
                        assert (email_history_info['recipient'] in recipient_list) == True
                    email_content = mysql[data_key].fetch('email_history_meta_info', {'message_id': message_id})
                    assert len(email_content) == 1
            else:
                if recipients:
                    if len(recipients.split(",")) >= 100:
                        assert response['result_code'] == 'invalid_param'
                        assert response['debug_msg'] == 'exceed limit, max receiver is 100'
                    else:
                        assert response['result_code'] == 'success'
                        assert response['data']["details"][0]["result"] == 'success', f"{response['data']['details'][0]['recipient']}邮件发送失败request_id:{response['request_id']}"

                else:
                    #
                    assert response['result_code'] == 'invalid_param'
                    assert response['debug_msg'] == 'necessary parameters are null.'

    push_cn_email_batch_keys = 'case_name,recipients,host_key,data_key'
    push_cn_email_batch_cases = [
        ('正案例_正常格式邮箱',
         "qiangwei.zhang@nio.com,maplepurple1123@163.com,550736273@qq.com,842244250@qq.com,maplepurple4@gmail.com,sherryyyyue@outlook.com,nioyue@icloud.com,sherry_shen@protonmail.com",
         'app_in', 'nmp_app'),
        # ('反案例_部分正常格式邮箱', "qiangwei.zhang@nio.com,1234567,2324434,550736273@qq.com", 'app_in', 'nmp_app'),
        # ('反案例_多个全部异常', "1234567,2324434,qq12121qq.com.cn", 'app_in', 'nmp_app'),
        # ('反案例_单个异常', "qq12121qq.com.cn", 'app_in', 'nmp_app'),
    ]
    ids = [f"{case[0]}" for case in push_cn_email_batch_cases]

    @pytest.mark.parametrize(push_cn_email_batch_keys, push_cn_email_batch_cases, ids=ids)
    def test_push_cn_email_batch(self, env, cmdopt, mysql, redis, case_name, recipients, host_key, data_key):
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        recipient_list = recipients.split(',')
        user_number = len(recipient_list)
        expected_details, expected_success, expected_failure, recipients_status = [], 0, 0, {}
        for i in range(user_number):
            recipient = recipient_list[i]

            if validation_email_format(recipient):
                recipients_status[recipient] = True
                expected_details.append({f"recipient": recipient, "result": "success"})
                expected_success = expected_success + 1
            else:
                recipients_status[recipient] = False
                expected_details.append({f"recipient": recipient, "result": "invalid_recipient"})
                expected_failure = expected_failure + 1
        expected_response = {
            "data": {
                # 多个值根据用户值进行排序
                "details": sorted(expected_details, key=lambda x: x['recipient'], reverse=True),
                "success": expected_success,
                "failure": expected_failure,
            },
            "result_code": "success",
        }
        app_id = 10007
        inputs = {
            "host": env['host'][host_key],
            "path": "/api/2/in/message/cn/email_push",
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
                "subject": f"【{cmdopt}】环境cn接口:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "content": "cn send email test",
                "category": "fellowMessage",
            }
        }
        with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete(f"rate.limiting:cn/email_push_{app_id}")
        response = hreq.request(env, inputs)
        assert response['result_code'] == 'success'
        assert response['data']["details"][0]["result"] == 'success', f"{response['data']['details'][0]['recipient']}邮件发送失败request_id:{response['request_id']}"
        response.pop("request_id")
        response.pop("server_time")
        message_id = response["data"].pop("message_id")
        details = response["data"]['details']
        response["data"]['details'] = sorted(details, key=lambda x: x['recipient'], reverse=True)
        assert_equal(response, expected_response)
        recipient_list = recipients.split(',')
        with allure.step("校验mysql"):
            for recipient in recipient_list:
                if recipients_status.get(recipient):
                    email_content = mysql['nmp_app'].fetch('email_history_meta_info', {'message_id': message_id})
                    assert len(email_content) == 1
                    email_history = mysql['nmp_app'].fetch('email_history', {'message_id': message_id, 'recipient': recipient})
                    assert len(email_history) == 1
                else:
                    email_history = mysql['nmp_app'].fetch('email_history', {'message_id': message_id, 'recipient': recipient}, retry_num=1)
                    assert len(email_history) == 0
