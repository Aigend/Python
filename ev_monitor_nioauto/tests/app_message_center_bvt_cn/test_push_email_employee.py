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
import allure
from utils.http_client import TSPRequest as hreq


# @pytest.mark.skip("manual")
class TestPushEmailEmployee(object):
    def test_notify_email_employee(self, env, cmdopt, mysql):
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
                    "subject": f"【BVT】【{cmdopt}】环境time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                    "content": f"【BVT】员工发送邮件接口",
                }
            }
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

