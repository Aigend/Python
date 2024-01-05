# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_push_sms.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/3/23 11:02 上午
# @Description :
import time

import allure

from utils.http_client import TSPRequest as hreq
from utils.logger import logger


class TestPushSMS(object):
    """
    接口文档 http://showdoc.nevint.com/index.php?s=/13&page_id=30142
    检查点
        mysql：
            * sms_history 历史消息
            * sms_history_meta_info 消息内容
        redis:
            *无
    user_ids,account_ids,recipients
        * 三选一
        * 批量个数 100（批量发送）
        * 重复用户
        * 异常数据
    content
        * 必填
        * 字符串
        * 长度限制
        * 支持变量，不支持
    category
        * 必填
        * (无限制，目前无业务逻辑处理)
    Q&A:
        Q1.短信频率限制，下游调用的是哪个服务
        dd
        Q2.category 类型，不同有代码逻辑上处理么，
            目前随便传都能发送成功，邮件也是
        Q3.content 支持长度限制，是否支持变量
            目前长度1000字可以收到。2000字未收到
        Q4.重复用户处理
            目前状况是接口会返回两条成功，但是手机一条也未收到
            DD频率限制
            """

    def test_push_sms_by_account_id(self, env, cmdopt, mysql, redis):

        app_id = 10001
        account_ids = env['push_sms']['account_id']
        recipients = env['push_sms']['recipient']
        category = 'ads'
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/2/in/message/cn/sms_push",
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
                "account_ids": account_ids,
                "content": f"【BVT】【{cmdopt}】环境接口推送短信{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "category": category,
            }
        }
        if "test" in cmdopt:
            with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
                redis["app_message"].delete(f"rate.limiting:cn/sms_push_{app_id}")
        with allure.step("push_sms_by_account_id接口"):
            response = hreq.request(env, inputs)
        with allure.step("校验结果"):
            assert response['result_code'] == 'success'
            message_id = response['data']['message_id']
            sms_history = mysql["nmp_app"].fetch("sms_history", {"message_id": message_id}, ["recipient"])
            assert str(sms_history[0]['recipient']) == str(recipients)
            sms_history_info = mysql["nmp_app"].fetch("sms_history_meta_info", {"message_id": message_id}, )
            assert len(sms_history_info) == 1

    def test_push_sms_by_recipient(self, env, cmdopt, mysql, redis):
        app_id = 10001
        recipients = env['push_sms']['recipient']
        category = 'ads'
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/2/in/message/cn/sms_push",
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
                "content": f"【BVT】【{cmdopt}】环境接口推送短信测试{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "category": category,
            }
        }
        if "test" in cmdopt:
            with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
                redis["app_message"].delete(f"rate.limiting:cn/sms_push_{app_id}")
        with allure.step("push_sms_by_recipient接口"):
            response = hreq.request(env, inputs)
        with allure.step("校验结果"):
            assert response['result_code'] == 'success'
            message_id = response['data']['message_id']
            sms_history = mysql["nmp_app"].fetch("sms_history", {"message_id": message_id}, ["recipient"])
            assert str(sms_history[0]['recipient']) == str(recipients)
            sms_history_info = mysql["nmp_app"].fetch("sms_history_meta_info", {"message_id": message_id}, )
            assert len(sms_history_info) == 1

    def test_push_sms_by_user_id(self, env, cmdopt, mysql, redis):
        app_id = 10001
        user_ids = env['push_sms']['user_id']
        recipients = env['push_sms']['recipient']
        category = 'ads'
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/2/in/message/cn/sms_push",
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
                "user_ids": user_ids,
                "content": f"【BVT】【{cmdopt}】环境接口推送短信{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "category": category,
            }
        }
        if "test" in cmdopt:
            with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
                redis["app_message"].delete(f"rate.limiting:cn/sms_push_{app_id}")
        with allure.step("push_sms_by_user_id接口"):
            response = hreq.request(env, inputs)
        with allure.step("校验结果"):
            assert response['result_code'] == 'success'
            message_id = response['data']['message_id']
            sms_history = mysql["nmp_app"].fetch("sms_history", {"message_id": message_id}, ["recipient"])
            assert str(sms_history[0]['recipient']) == str(recipients)
            sms_history_info = mysql["nmp_app"].fetch("sms_history_meta_info", {"message_id": message_id}, )
            assert len(sms_history_info) == 1

