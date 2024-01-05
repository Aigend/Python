# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_sms_preview_cn_emay.py
# @Author : qiangwei.zhang
# @time: 2021/11/05
# @api: POST_/api/2/in/message_portal/template/cn/marketing_sms/preview 【必填】
# @showdoc: http://showdoc.nevint.com/index.php?s=/647&page_id=32354
# @Description :脚本描述
import time
import allure
import pytest
from utils.http_client import TSPRequest as hreq
from utils.random_tool import random_int

from tests.app_message_portal.template_management.template_server import init_sms_template, get_template_detail
from tests.app_message_portal.variable_management.variable_server import extracted_private_variable_from_template, generate_private_variable_replace, verify_variable

cn_emay_sms_preview_path = "/api/2/in/message_portal/template/cn/marketing_sms/preview"

recipients = "+8617610551933,+8617610551934,+8618612709129"
test_data_map = {"recipients": "+8617610551933,+8617610551934,+8618612709129", "user_ids": "1234,2345", "account_ids": "1234,2345"}
app_id = 10000


class TestTemplateReview(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_template(self, env, mysql):
        return init_sms_template(env, mysql)

    sms_review_cn_emay_keys = "case_name,template_name,replace_values,user_key"
    sms_review_cn_emay_cases = [
        ("正案例_无变量模板", "SMS_no_variable", None, "recipients"),
        ("正案例_只有公共变量模板_变量无重复", "SMS_R_no_repeat", None, "account_ids"),
        ("正案例_只有公共变量模板_变量有重复", "SMS_R_repeat", None, "user_ids"),
        ("正案例_只有自定义变量模板_变量无重复", "SMS_L_no_repeat", "all", "recipients"),
        ("正案例_只有自定义变量模板_变量有重复", "SMS_L_repeat", "all", "recipients"),
        ("正案例_公共变量+自定义变量模板_有多个重复变量", "SMS_L_R_repeat", "all", "recipients"),
        ("正案例_公共变量+自定义变量模板_变量不重复", "SMS_L_R_no_repeat", "all", "recipients"),
    ]
    sms_review_cn_emay_ids = [f"{case[0]}" for case in sms_review_cn_emay_cases]

    @pytest.mark.parametrize(sms_review_cn_emay_keys, sms_review_cn_emay_cases, ids=sms_review_cn_emay_ids)
    def test_sms_review_cn_emay(self, env, cmdopt, mysql, case_name, template_name, replace_values, prepare_template, user_key):
        template_id_map = prepare_template
        template_id = template_id_map.get(template_name)
        template_detail = get_template_detail(env, template_id)
        template_content = template_detail.get("data").get("template_str")
        private_variable = extracted_private_variable_from_template(template_content)
        generate_replace_values, json_dict = [], {}
        user_info = test_data_map.get(user_key)
        # random_list = [str(random_int(12)) for i in range(150)]
        # user_info = ",".join(random_list)
        if private_variable and replace_values:
            part_user, part_variable = False, False
            if "part_value" == replace_values:
                part_variable = True
            elif "part_user" in replace_values:
                part_user = True
            generate_replace_values = generate_private_variable_replace(recipients, private_variable, part_user, part_variable)

        with allure.step('CN短信发送内容预览接口'):
            json_dict = {
                "channel": "email",
                user_key: user_info,
                "template_id": template_id,
                "category": "ads",
                "replace_values": generate_replace_values
            }
            json_dict = {k: v for k, v in json_dict.items() if v}
            inputs = {
                "host": env['host']['app_in'],
                "path": cn_emay_sms_preview_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": json_dict
            }
            response = hreq.request(env, inputs)
            assert response['result_code'] == 'success'
            assert len(response.get("data")) == len(user_info.split(",")) + 1
        with allure.step('验证替换参数正常替换'):
            verify_variable(response, user_info, generate_replace_values)