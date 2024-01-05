# -*- coding: utf-8 -*-
# @Project : cvs_basic_autotest
# @File : test_notify_email.py
# @Author : qiangwei.zhang.o
# @CreateTime : 2021/3/16 6:04 下午
# @Description :
"""
    接口文档：http://showdoc.nevint.com/index.php?s=/13&page_id=30141
    附件发送邮件功能测试结果
    测试的接口
        ✅* CN
        ✅* EU
        ✅* employee
    测试场景
        ✅* 文件类型
            * pdf
            * 图片
            * word 文档
            * x l s
            * 压缩文件
        ✅* 文件大小
            * 最大10M
        ✅* 文件数量
            * 1个
            ❌* 多个文件不支持
        ✅* 文件名称
            * 非中文
            * 带有中文
        ✅* 不传附件

    指定sender_name
    None employee+cn默认为notification@nio.com，eu默认为notification@nio.io
    tsp@nioint.com
    notification@nio.io
    notification@nio.com
    错误发件人

"""

import time
import os
import pytest
import allure
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from tests.app_message_center.test_data.file.file_path import zip_path, pdf_path, apk_path, pptx_path, png_path, xlsx_path, doc_path, pdf_path_1

cn_email_with_attachment_path = "/api/2/in/message/cn/email_direct_push"
allow_environment = ["test", "stg", "test_alps"]


# @pytest.mark.skip("manual")
@pytest.mark.run(order=1)
class TestPushEmailCN(object):
    push_cn_email_with_attachment_keys = 'case_name,sender_name,recipients,file_path,host_key,data_key'
    push_cn_email_with_attachment_cases = [  # ("正案例_TOC_单个收件人有附件", "notification@nio.com", "550736273@qq.com", pdf_path, 'app_in', 'nmp_app'),
        # ("正案例_TOC_单个收件人有附件apk", "notification@nio.com","550736273@qq.com", apk_path, 'app_in', 'nmp_app'),
        # ("正案例_TOC_单个收件人有附件pptx", "notification@nio.com","550736273@qq.com", pptx_path, 'app_in', 'nmp_app'),
        # ("正案例_TOC_单个收件人有附件png", "notification@nio.com","550736273@qq.com", png_path, 'app_in', 'nmp_app'),
        # ("正案例_TOC_单个收件人有附件xlsx", "notification@nio.com", "550736273@qq.com", xlsx_path, 'app_in', 'nmp_app'),
        # ("正案例_TOC_单个收件人有附件doc", "notification@nio.com", "550736273@qq.com", xlsx_path, 'app_in', 'nmp_app'),
        # ("正案例_TOC_单个收件人有附件pdf", "notification@nio.com","550736273@qq.com", pdf_path_1, 'app_in', 'nmp_app'),
        # ("正案例_TOC_指定发件人notification@nio.com", "notification@nio.com", "550736273@qq.com", xlsx_path, 'app_in', 'nmp_app'),
        # ("正案例_TOC_指定发件人nio_pay@nioint.com", "nio_pay@nioint.com", "550736273@qq.com", xlsx_path, 'app_in', 'nmp_app'),
        ("正案例_TOC_默认收件人notification@nio.com", None, "550736273@qq.com", xlsx_path, 'app_in', 'nmp_app'),
    ]
    push_cn_email_with_attachment_ids = [f"{case[0]}" for case in push_cn_email_with_attachment_cases]

    @pytest.mark.parametrize(push_cn_email_with_attachment_keys, push_cn_email_with_attachment_cases, ids=push_cn_email_with_attachment_ids)
    def test_push_cn_email_with_attachment(self, env, cmdopt, mysql, redis, case_name, sender_name, recipients, file_path, host_key, data_key):
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        time.sleep(1)
        file_name = os.path.basename(file_path)
        file_type = file_name.split('.')[-1]
        file_size = os.path.getsize(file_path)
        logger.debug(f"cn send email test 附件\n文件名称:{file_name}\n文件类型:{file_type}\n文件大小(byte):{file_size}\n文件大小(M):{file_size / 1024 / 1024}")
        with allure.step(f"【{cmdopt}】环境，CN支持附件发送邮件接口{case_name}"):
            category = 'ads'
            app_id = 10000
            inputs = {
                "host": env['host'][host_key],
                "path": cn_email_with_attachment_path,
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
                    "subject": f"【{cmdopt}】环境cn接口:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                    "content": f"cn send email test 附件\n文件名称:{file_name}\n文件类型:{file_type}\n文件大小(byte):{file_size}\n文件大小(M):{file_size / 1024 / 1024}",
                    "category": category,
                    "sender_name": sender_name,
                },
                "files": {"file": (file_name, open(file_path, "rb"))},
            }
            response = hreq.request(env, inputs)
            with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
                if "test" in cmdopt:
                    redis["app_message"].delete(f"rate.limiting:cn/email_direct_push_{app_id}")
            if case_name.startswith("正案例"):
                assert response['result_code'] == 'success'
                assert response['data']["details"][0]["result"] == 'success', f"{response['data']['details'][0]['recipient']}邮件发送失败request_id:{response['request_id']}"
                message_id = response['data']['message_id']
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
