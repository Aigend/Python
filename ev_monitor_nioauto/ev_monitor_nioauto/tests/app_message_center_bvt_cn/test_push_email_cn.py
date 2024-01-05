# -*- coding: utf-8 -*-
# @Project : cvs_basic_autotest
# @File : test_push_email_cn.py
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
import allure
import pytest

from utils.http_client import TSPRequest as hreq


# @pytest.mark.skip("manual")
class TestPushEmailCN(object):
    def test_push_cn_email(self, env, cmdopt, mysql):
        recipients = '550736273@qq.com'
        host_key = 'app_in'
        data_key = 'nmp_app'
        with allure.step(f"【{cmdopt}】环境，CN发送邮件接口"):
            category = 'fellowMessage'  # ads, verify, fellowMessage
            app_id = 10000
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
                    "subject": f"【BVT】【{cmdopt}】环境cn接口:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                    "content": "【BVT】cn send email test",
                    "category": category,
                }
            }
            response = hreq.request(env, inputs)
            assert response['result_code'] == 'success'
            message_id = response['data']['message_id']
            with allure.step("校验mysql"):
                email_history = mysql[data_key].fetch('email_history', {'message_id': message_id}, ['recipient'])
                recipient_list = recipients.split(',')
                for email_history_info in email_history:
                    assert email_history_info['recipient'] in recipient_list
                email_content = mysql[data_key].fetch('email_history_meta_info', {'message_id': message_id})
                assert len(email_content) == 1


