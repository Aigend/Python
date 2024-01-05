# -*- coding: utf-8 -*-
# @Project : cvs_basic_autotest
# @File : test_notify_email.py
# @Author : qiangwei.zhang.o
# @CreateTime : 2021/3/16 6:04 下午
# @Description :
# @showdoc : http://showdoc.nevint.com/index.php?s=/647&page_id=31593
"""
* 直接发送员工邮件接口 /api/2/in/message/employee/email_direct_push
    * recipients
        * 收件人
            * 多个正常 
            * 单个正常 
            * 部分正常 任何一个异常全部不发送
            * 多个正常有重复 
            * 全部异常
            * 邮件组
            * 邮件组+单个收件人
            * 邮件组+多个收件人
        * 必填 
    * subject
        * 必填 
    * content
        * 必填 
    * category
        * 必填 
    * sender_name
        * 非必填默认notification@nio.com 
        * tsp@nioint.com 
    * file
        * 非必填 
    * single_mail
        * true 
        * false 
    * cc_recipients
        * 抄送人
            * 多个正常 
            * 单个正常 
            * 部分正常 任何一个异常全部不发送
            * 多个正常有重复 去重
            * 全部异常 任何一个异常全部不发送
            * 邮件组
            * 邮件组+单个收件人
            * 邮件组+多个收件人
        * 非必填 
    * bcc_recipients
        * 密送人
            * 多个正常 
            * 单个正常 
            * 部分正常 任何一个异常全部不发送
            * 多个正常有重复 去重
            * 全部异常 任何一个异常全部不发送
            * 邮件组
            * 邮件组+单个收件人
            * 邮件组+多个收件人
        * 非必填
"""

import time
import os
import pytest
import allure
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from tests.app_message_center.test_data.file.file_path import file_path_map

email_email_direct_push_path = "/api/2/in/message/employee/email_direct_push"
app_id = 10000
sg_email = "DS_CVS_QA@nio.com"
g_email = "DS_CVS_QA@nio.com"
s_email = "qiangwei.zhang@nio.com"


@pytest.mark.run(order=1)
class TestPushEmailEmployee(object):
    notify_email_employee_with_attachment_keys = 'case_name,host_key,data_key,recipients,file_path'
    notify_email_employee_with_attachment_cases = [
        # --------------TOC服务--------------
        # ("正案例_TOC_公司员工邮箱带附件pdf_path", 'app_in', 'nmp_app', s_email, file_path_map.get("pdf_path")),
        # ("正案例_TOC_公司员工邮箱带附件apk_path", 'app_in', 'nmp_app', s_email, file_path_map.get("apk_path")),
        # ("正案例_TOC_公司员工邮箱带附件pptx_path", 'app_in', 'nmp_app', s_email, file_path_map.get("pptx_path")),
        # ("正案例_TOC_公司员工邮箱带附件png_path", 'app_in', 'nmp_app', s_email, file_path_map.get("png_path")),
        ("正案例_TOC_公司员工邮箱带附件xlsx_path", 'app_in', 'nmp_app', s_email, file_path_map.get("xlsx_path")),
        # ("正案例_TOC_公司员工邮箱带附件doc_path", 'app_in', 'nmp_app', s_email, file_path_map.get("doc_path")),
        # ("正案例_TOC_公司员工邮箱带附件zip_path", 'app_in', 'nmp_app', s_email, file_path_map.get("zip_path")),
        # ("正案例_TOC_公司员工邮箱带附件zip_path", 'app_in', 'nmp_app', s_email, file_path_map.get("zip_path")),
        # --------------TOB服务--------------
        ("正案例_TOB_公司员工邮箱带附件xlsx_path", 'app_tob_in', 'nmp_app_tob', s_email, file_path_map.get("xlsx_path")),
    ]
    notify_email_employee_with_attachment_ids = [f"{case[0]}" for case in notify_email_employee_with_attachment_cases]

    @pytest.mark.parametrize(notify_email_employee_with_attachment_keys, notify_email_employee_with_attachment_cases, ids=notify_email_employee_with_attachment_ids)
    def test_notify_email_employee_with_attachment(self, env, cmdopt, case_name, mysql, redis, host_key, data_key, recipients, file_path):
        time.sleep(1)  # 有频率限制
        file_name = os.path.basename(file_path)
        file_type = file_name.split('.')[-1]
        file_size = os.path.getsize(file_path)
        with allure.step(f"员工发送邮件接口：{case_name}"):
            category = 'ads'  # marketing_email,fellow_contact
            inputs = {
                "host": env['host'][host_key],
                "path": email_email_direct_push_path,
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
                    "subject": f"【{cmdopt}】环境{case_name}time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                    "content": f"employee send email test 附件文件名称:{file_name}文件类型:{file_type}文件大小(byte):{file_size}文件大小(M):{file_size / 1024 / 1024}",
                    # "category": "ads",
                },
                "files": {"file": (file_name, open(file_path, "rb"))},
            }
            response = hreq.request(env, inputs)
            with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
                if "test" in cmdopt:
                    redis["app_message"].delete(f"rate.limiting:{app_id}")
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

    notify_email_employee_with_cc_keys = 'case_name,sender_name,recipients,cc_recipients,bcc_recipients,file_path,host_key,data_key'
    notify_email_employee_with_cc_test_cases = [
        # --------------TOC服务--------------
        ("正案例_TOC_单个收件人无附件", None, s_email, None, None, None, 'app_in', 'nmp_app'),
        ("正案例_TOC_单个收件人有附件", None, s_email, "qiangwei.zhang@nio.com", None, file_path_map.get("xlsx_path"), 'app_in', 'nmp_app'),
        # ("正案例_TOC_单个收件人，有抄送", None, g_email, s_email, None, file_path_map.get("zip_path"), 'app_in', 'nmp_app'),
        # ("正案例_TOC_单个收件人，有抄送", None, "qiangwei.zhang@nio.com,colin.li@nio.com,chunyan.liu@nio.com", "qiangwei.zhang@nio.com", None, None, 'app_in', 'nmp_app'),
        # ("正案例_TOC_单个收件人，有抄送", None, "DS_CVS_QA@nio.com", "qiangwei.zhang@nio.com", None, None, 'app_in', 'nmp_app'),
        # ("正案例_TOC_单个收件人,无附件", None, s_email, None, None, None, 'app_in', 'nmp_app'),
        # ("正案例_TOC_收件人为邮件组", None, "DS_CVS_QA@nio.com", None, None, None, 'app_in', 'nmp_app'),
        # ("正案例_TOC_收件人为邮件组+多个收件人,带附件", None, sg_email, None, None, file_path_map.get("zip_path"), 'app_in', 'nmp_app'),
        # ("正案例_TOC_单个收件人,抄送人为邮件组+收件人,带附件", None, s_email, sg_email, None, file_path_map.get("zip_path"), 'app_in', 'nmp_app'),
        # ("正案例_TOC_单个收件人,秘送人为邮件组+收件人,带附件", None, s_email, None, sg_email, file_path_map.get("zip_path"), 'app_in', 'nmp_app'),
        # ("正案例_TOB_收件人为邮件组", None, "DS_CVS_QA@nio.com", None, None, None, 'app_tob_in', 'nmp_app_tob'),
        # ("正案例_TOB_收件人为邮件组+多个收件人,带附件", None, sg_email, None, None, file_path_map.get("zip_path"), 'app_tob_in', 'nmp_app_tob'),
        # ("正案例_TOB_单个收件人,抄送人为邮件组+收件人,带附件", None, s_email, sg_email, None, file_path_map.get("zip_path"), 'app_tob_in', 'nmp_app_tob'),
        # ("正案例_TOB_单个收件人,秘送人为邮件组+收件人,带附件", None, s_email, None, sg_email, file_path_map.get("zip_path"), 'app_tob_in', 'nmp_app_tob'),
        # ("正案例_TOB_单个收件人无附件", None, s_email, None, None, None, 'app_tob_in', 'nmp_app_tob'),
        # ("正案例_TOB_单个收件人有附件", None, s_email, "qiangwei.zhang@nio.com", None, file_path_map.get("zip_path"), 'app_tob_in', 'nmp_app_tob'),
    ]
    notify_email_employee_with_cc_ids = [f"{case[0]}" for case in notify_email_employee_with_cc_test_cases]

    # @pytest.mark.skip("manual")
    @pytest.mark.parametrize(notify_email_employee_with_cc_keys, notify_email_employee_with_cc_test_cases, ids=notify_email_employee_with_cc_ids)
    def test_notify_email_employee_with_cc(self, env, cmdopt, mysql, redis, case_name, sender_name, recipients, cc_recipients, bcc_recipients, file_path, host_key, data_key):
        time.sleep(1)  # 有频率限制
        files, file_name, file_type, file_size = None, None, None, 0
        if file_path:
            file_name = os.path.basename(file_path)
            file_type = file_name.split('.')[-1]
            file_size = os.path.getsize(file_path)
            files = {"file": (file_name, open(file_path, "rb"))}
        else:
            files = {"file": None}
        with allure.step(f"员工发送邮件接口：{case_name}"):
            category = 'ads'  # marketing_email,fellow_contact
            inputs = {
                "host": env['host'][host_key],
                "path": email_email_direct_push_path,
                "method": "POST",
                # "headers": {"Content-Type": "application/x-www-form-urlencoded"},
                "params": {
                    "region": "cn",
                    "lang": "zh-cn",
                    "hash_type": "sha2566",
                    "app_id": app_id,
                    "sign": ""
                },
                "data": {
                    "recipients": recipients,
                    "cc_recipients": cc_recipients,
                    "bcc_recipients": bcc_recipients,
                    "single_mail": "true",
                    "subject": f"【{cmdopt}】{host_key}环境消息平台测试邮件，single_mail True请忽略。time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}category:{category}",
                    "content": f"消息平台测试邮件，如有打扰请见谅。 案例名称:{case_name} API:{email_email_direct_push_path} 附件文件名称:{file_name}文件类型:{file_type}文件大小(byte):{file_size}文件大小(M):{file_size / 1024 / 1024}",
                },
                "files": files,
            }
            response = hreq.request(env, inputs)
            with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
                if "test" in cmdopt:
                    redis["app_message"].delete(f"rate.limiting:employee/email_push_{app_id}")
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
