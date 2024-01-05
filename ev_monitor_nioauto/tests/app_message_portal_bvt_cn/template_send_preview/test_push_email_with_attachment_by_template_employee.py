# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_template_add.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/10 4:02 下午
# @Description :
import json
import os
import time
import allure
import pytest
import requests
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from tests.app_message_portal.template_management.template_server import init_email_template, get_template_detail
from tests.app_message_portal.variable_management.variable_server import extracted_private_variable_from_template, generate_private_variable_replace
from tests.app_message_center.test_data.file.file_path import zip_path, pdf_path, apk_path, pptx_path, png_path, xlsx_path, doc_path, pdf_path_1


app_id = 10000
cn_email_with_attachment_send_path = "/api/2/in/message_portal/template/cn/email_with_attach/send"
employee_email_with_attachment_send_path = "/api/2/in/message_portal/template/employee/email_with_attach/send"
# eu_email_with_attachment_send_path = "/api/2/in/message_portal/template/eu/email_with_attach/send"
allow_environment = ["test", "stg"]
eu_allow_environment = ["test_marcopolo", "stg_marcopolo"]


class TestTemplateSendEmail(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_template(self, env, mysql):
        return init_email_template(env, mysql)

    employee_email_with_attachment_send_keys = "case_name,template_name,replace_values,file_path"
    employee_email_with_attachment_send_cases = [
        ("正案例_公共变量+自定义变量模板_有多个重复变量", "L_R_repeat", "all", xlsx_path),
    ]
    employee_email_with_attachment_send_ids = [f"{case[0]}" for case in employee_email_with_attachment_send_cases]

    @pytest.mark.parametrize(employee_email_with_attachment_send_keys, employee_email_with_attachment_send_cases, ids=employee_email_with_attachment_send_ids)
    def test_template_with_attachment_email_send_cn(self, env, cmdopt, mysql, redis, case_name, template_name, replace_values, prepare_template, file_path):
        """
        http://showdoc.nevint.com/index.php?s=/647&page_id=32670
        """
        with allure.step(f"【{cmdopt}】环境,清理{10022}频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete(f"rate.limiting:employee/email_direct_push_10022")
        region = "cn"
        recipients = "550736273@qq.com"
        # cc_recipients = "842244250@qq.com"
        # bcc_recipients = "maplepurple1123@163.com"
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        files, file_name, file_type, file_size = None, None, None, 0
        if file_path:
            file_name = os.path.basename(file_path)
        with allure.step(f"【{cmdopt}】环境,清理10022频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete("rate.limiting:cn/email_direct_push_10022")
            else:
                logger.debug("非test环境，没有权限清理redis数据")
        template_id_map = prepare_template
        template_id = template_id_map.get(template_name)
        template_detail = get_template_detail(env, template_id)
        template_content = template_detail.get("data").get("template_str")
        private_variable = extracted_private_variable_from_template(template_content)
        generate_replace_values = []
        if private_variable and replace_values:
            part_user, part_variable = False, False
            if "part_value" == replace_values:
                part_variable = True
            elif "part_user" in replace_values:
                part_user = True
            generate_replace_values = generate_private_variable_replace(recipients, private_variable, part_user, part_variable)
        with allure.step('CN邮件发送内容预览接口'):
            json_dict = {
                "recipients": recipients,
                "template_id": template_id,
                "replace_values": generate_replace_values,
                # "cc_recipients": cc_recipients,
                # "bcc_recipients": bcc_recipients,
            }
            inputs = {
                "host": env['host']['app_in'],
                "path": cn_email_with_attachment_send_path,
                "method": "POST",
                "params": {
                    "region": region,
                    "lang": "zh-cn",
                    "hash_type": "sha256",
                    "app_id": app_id,
                    "sign": ""
                },
                "files": {
                    "template_push_data": (None, json.dumps(json_dict, ensure_ascii=False), 'application/json'),
                    "file": (file_name, open(file_path, "rb"), 'application/octet-stream')
                }
            }
            response = hreq.request(env, inputs)
            assert response['result_code'] == 'success'

    employee_email_with_attachment_send_keys = "case_name,template_name,replace_values,file_path"
    employee_email_with_attachment_send_cases = [
        ("正案例_公共变量+自定义变量模板_变量不重复", "L_R_no_repeat", "all", xlsx_path),
    ]
    employee_email_with_attachment_send_ids = [f"{case[0]}" for case in employee_email_with_attachment_send_cases]

    @pytest.mark.parametrize(employee_email_with_attachment_send_keys, employee_email_with_attachment_send_cases, ids=employee_email_with_attachment_send_ids)
    def test_template_with_attachment_email_send_employee(self, env, cmdopt, mysql, redis, case_name, template_name, replace_values, prepare_template, file_path):
        """
        http://showdoc.nevint.com/index.php?s=/647&page_id=32670
        """
        region = "cn"
        recipients = "chunyan.liu1@nio.com"
        cc_recipients = "colin.li@nio.com,qiangwei.zhang@nio.com"
        bcc_recipients = "qiangwei.zhang@nio.com"
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        files, file_name, file_type, file_size = None, None, None, 0
        if file_path:
            file_name = os.path.basename(file_path)
        with allure.step(f"【{cmdopt}】环境,清理10022频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete("rate.limiting:employee/email_direct_push_10022")
            else:
                logger.debug("非test环境，没有权限清理redis数据")
        template_id_map = prepare_template
        template_id = template_id_map.get(template_name)
        template_detail = get_template_detail(env, template_id)
        template_content = template_detail.get("data").get("template_str")
        private_variable = extracted_private_variable_from_template(template_content)
        generate_replace_values = []
        if private_variable and replace_values:
            part_user, part_variable = False, False
            if "part_value" == replace_values:
                part_variable = True
            elif "part_user" in replace_values:
                part_user = True
            generate_replace_values = generate_private_variable_replace(recipients, private_variable, part_user, part_variable)
        with allure.step('CN邮件发送内容预览接口'):
            json_dict = {
                "recipients": recipients,
                "template_id": template_id,
                "replace_values": generate_replace_values,
                "cc_recipients": cc_recipients,
                # "bcc_recipients": bcc_recipients,
            }
            inputs = {
                "host": env['host']['app_in'],
                "path": employee_email_with_attachment_send_path,
                "method": "POST",
                "params": {
                    "region": region,
                    "lang": "zh-cn",
                    "hash_type": "sha256",
                    "app_id": app_id,
                    "sign": ""
                },
                "files": {
                    "template_push_data": (None, json.dumps(json_dict, ensure_ascii=False), 'application/json'),
                    "file": (file_name, open(file_path, "rb"), 'application/octet-stream')
                }
            }
            response = hreq.request(env, inputs)
            assert response['result_code'] == 'success'