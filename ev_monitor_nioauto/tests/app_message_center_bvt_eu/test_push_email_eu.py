# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto 
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
from data.email_content import long_text, html5
from utils.random_tool import random_string, random_int
from config.settings import BASE_DIR
from utils.collection_message_states import collection_message_states


def get_user_retry(func):
    def inner(*args, **kwargs):
        ret = func(*args, **kwargs)
        max_retry = 20
        number = 0
        if not ret:
            while number < max_retry:
                number += 1
                time.sleep(5)
                logger.debug(f"尝试第:{number}次")
                result = func(*args, **kwargs)
                if result:
                    return result
        else:
            return ret

    return inner


class TestPushEmailEU(object):
    @pytest.fixture(scope="class")
    def prepare_eu_email_account(self, env, cmdopt):
        cmdopt = "test_marcopolo" if cmdopt == 'test' else cmdopt
        # 消息平台test环境和test_marcopolo环境对应留资test_marcopolo环境
        file_path = f'{BASE_DIR}/config/{cmdopt}/email_account_info_{cmdopt}.txt'
        account_list = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    account_msg = {}
                    account_msg_list = line.split(',')
                    account_msg['account_id'] = account_msg_list[0]
                    account_msg['user_id'] = account_msg_list[1]
                    account_msg['recipient'] = account_msg_list[2]
                    account_msg['password'] = account_msg_list[3]
                    account_list.append(account_msg)
            user_id = get_user_is_by_account_id(env, account_list[0]['account_id'])
            if user_id:
                # 如果历史数据在留资系统存在，返回历史数据,否则重新生成数据
                return account_list
            else:
                return register_email_zeus(env, cmdopt, 5)
        else:
            return register_email_zeus(env, cmdopt, 5)

    def set_switch(self, env, channel, category, user_id=None, status=True):
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/2/in/message/set_switch",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "params": {
                "region": "eu",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": "10007",
                "sign": ""
            },
            "data": {
                "user_id": user_id,
                "channel": channel,
                "category": category,
                "switch": status,
            }
        }
        response = hreq.request(env, inputs)
        assert response["result_code"] == "success"

    @pytest.mark.parametrize('case_name,category,white_app_id,recipients',
                             [
                                 ('正案例_无需订阅_验证码渠道_白名单app_id_10007', 'verify', '10007', "550736273@qq.com"),
                                 ('正案例_无需订阅_试驾渠道_白名单app_id_1000075', 'test_drive', '1000075', "550736273@qq.com"),
                             ])
    def test_push_email_not_need_to_subscribe(self, env, cmdopt, mysql, redis, case_name, category, white_app_id, recipients):
        allow_environment = ["test_marcopolo", "stg_marcopolo"]
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        with allure.step(f"【{cmdopt}】环境,无需订阅{category}频道发送邮件:{case_name}"):
            http = {
                "host": env['host']['app_in'],
                "path": "/api/2/in/message/email_push",
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {
                    "region": "eu",
                    "lang": "zh-cn",
                    "hash_type": "sha256",
                    "app_id": white_app_id,
                    "sign": ""
                },
                "json": {
                    "recipients": recipients,
                    "subject": f"【BVT】【{cmdopt}】环境eu_verify接口邮件:time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                    "content": f"【BVT】【{cmdopt}】环境，message/email_push\n{case_name}",
                    "category": category,
                }
            }
            with allure.step(f"【{cmdopt}】环境,清理{white_app_id}频率限制"):
                if "test" in cmdopt:
                    redis["app_message"].delete(f"rate.limiting:eu/email_push_{white_app_id}")
            response = hreq.request(env, http)
            if case_name.startswith("反案例"):
                assert response == "Not found\n"
            else:
                assert response['result_code'] == 'success'
                message_id = response['data']['message_id']
                with allure.step("校验mysql"):
                    email_history = mysql['nmp_app'].fetch('email_history', {'message_id': message_id}, ['recipient'])
                    recipient_list = recipients.split(',')
                    for email_history_info in email_history:
                        assert (email_history_info['recipient'] in recipient_list) == True
                    email_content = mysql['nmp_app'].fetch('email_history_meta_info', {'message_id': message_id})
                    assert len(email_content) == 1

    @pytest.mark.parametrize('case_name,category,status,user_data_type',
                             [
                                 ('正案例_根据user_id订阅后发送邮件', 'fellow_contact', True, 'user_id'),
                                 ('正案例_根据account_id取消订阅后发送邮件', 'marketing_email', False, 'account_id'),
                                 ('正案例_根据recipients订阅后发送邮件', 'fellow_contact', True, 'recipient'),
                             ])
    def test_push_eu_email(self, env, cmdopt, mysql, redis, prepare_eu_email_account, case_name, category, status, user_data_type):
        allow_environment = ["test_marcopolo", "stg_marcopolo"]
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        account_msg_list = prepare_eu_email_account
        account_msg = account_msg_list[0]
        user_data = account_msg.get(user_data_type)
        recipient = account_msg.get("recipient")
        user_id = account_msg.get("user_id")
        self.set_switch(env, 'email', category, user_id, status)
        app_id = 10007
        path = "/api/2/in/message/email_push"
        inputs = {
            "host": env['host']['app_in'],
            "path": path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "eu",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                "sign": ""
            },
            "json": {
                f"{user_data_type}s": user_data,
                "subject": f"{cmdopt}time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                "content": f"{html5}",
                "category": category,
            }
        }
        with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete(f"rate.limiting:eu/email_push_{app_id}")
        response = hreq.request(env, inputs)
        assert response['result_code'] == 'success'
        response.pop("request_id")
        response.pop("server_time")
        message_id = response["data"].pop("message_id")
        if status:
            # 订阅返回结果
            expected_response = {
                "data": {
                    "details": [{f"{user_data_type}": user_data, "result": "success"}],
                    "success": 1,
                    "failure": 0,
                },
                "result_code": "success",
            }
            assert_equal(response, expected_response)
            with allure.step("校验mysql"):
                email_history = mysql['nmp_app'].fetch('email_history', {'message_id': message_id}, ['recipient'])
                recipient_list = recipient.split(',')
                for email_history_info in email_history:
                    assert (email_history_info['recipient'] in recipient_list) == True
                email_content = mysql['nmp_app'].fetch('email_history_meta_info', {'message_id': message_id})
                assert len(email_content) == 1
        else:
            # 未订阅返回结果
            expected_response = {
                "data": {
                    "details": [{f"{user_data_type}": user_data, "result": "not_subscribe", "reason": f"user do not subscribe the category:{category}"}],
                    "success": 0,
                    "failure": 1,
                },
                "result_code": "success",
            }
            assert_equal(response, expected_response)


@get_user_retry
def get_user_is_by_account_id(env, account_id):
    """
        接口文档：http://showdoc.nevint.com/index.php?s=/636&page_id=29860
        留资user那边可以根据app_id来配置返回字段，
        message_center的app_id=10022
        可以根据account_ids,user_ids,emails来查询用户列表
    """
    host = env['host']['zeus_in']
    inputs = {
        "host": host,
        "path": "/zeus/in/user/v1/users",
        "method": "GET",
        "params": {
            "hash_type": "sha256",
            "account_ids": account_id,
            "app_id": "10007",
            "offset": 0,
            "count": 50,
            "sign": ""
        }
    }
    response = hreq.request(env, inputs)
    logger.debug(response)
    assert response['result_code'] == 'success'
    user_data_list = response['data']['list']
    if user_data_list:
        return user_data_list[0]['user_id']
    else:
        return False


def register_email_zeus(env, cmdopt, count=2):
    """
    该方法用于创建留资账号，账号数据写入文件并返回list
    """
    if count > 20:
        return '请勿一次创建过多测试账号'
    file_path = f'{BASE_DIR}/config/{cmdopt}/email_account_info_{cmdopt}.txt'
    if os.path.exists(file_path):
        os.remove(file_path)
    list_account = []
    for i in range(int(count)):
        host = 'http://10.110.3.103:5000'
        api = '/pangu/email_register_zeus'
        inputs = {
            "host": host,
            "method": 'POST',
            "path": api,
            "headers": {'Content-Type': 'application/json'},
            "json": {
                "nick_name": f"evm_{cmdopt}_{random_string(6)}",
                "env": cmdopt
            }
        }
        res_dict = hreq.request(env, inputs)
        if res_dict.get('result_code') == "success":
            logger.debug(res_dict)
            data = res_dict.get('data')
            res_account_msg = data.get("account_register_info")
            account_id = res_account_msg.get('account_id')
            user_id = data.get("user").get("user_id")
            email = data.get("email")
            password = data.get("password")
            pseudo_email = data.get("pseudo_email")
            email_account_info = f"{account_id},{user_id},{email},{password},{pseudo_email},{res_account_msg.get('create_time')}"
            res_msg = {"account_id": account_id, "user_id": user_id, "recipient": email, "password": password, "pseudo_email": pseudo_email}
            list_account.append(res_msg)
            with open(file_path, 'a+')as f:
                logger.debug(email_account_info)
                f.write(f'{email_account_info}\n')
    return list_account
