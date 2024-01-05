# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_sms_preview_cn.py
# @Author : qiangwei.zhang
# @time: 2021/08/25
# @api: POST_/api/2/in/message_portal/template/cn/marketing_sms/send 【必填】
# @showdoc: http://showdoc.nevint.com/index.php?s=/647&page_id=32354
# @Description :脚本描述
import time
import allure
import pytest

from utils.logger import logger
from utils.http_client import TSPRequest as hreq
from utils.random_tool import random_int
from utils.message_formator import format_to_message_state

from tests.app_message_portal.template_management.template_server import init_sms_template, get_template_detail
from tests.app_message_portal.variable_management.variable_server import extracted_private_variable_from_template, generate_private_variable_replace

cn_emay_sms_send_path = "/api/2/in/message_portal/template/cn/marketing_sms/send"
app_id = 10000
recipient_one_real = "+8617610551933"


class TestTemplateSend(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_template(self, env, mysql):
        return init_sms_template(env, mysql)

    sms_template_send_cn_emay_keys = "case_name,template_name,replace_values,recipients"
    sms_template_send_cn_emay_cases = [
        ("正案例_单个正常", "SMS_L_R_repeat", "all", recipient_one_real),
    ]
    sms_template_send_cn_emay_ids = [f"{case[0]}" for case in sms_template_send_cn_emay_cases]

    @pytest.mark.parametrize(sms_template_send_cn_emay_keys, sms_template_send_cn_emay_cases, ids=sms_template_send_cn_emay_ids)
    def test_sms_template_send_cn_emay(self, env, cmdopt, mysql,redis, case_name, template_name, replace_values, prepare_template, recipients):
        template_id_map = prepare_template
        template_id = template_id_map.get(template_name)
        template_detail = get_template_detail(env, template_id)
        template_content = template_detail.get("data").get("template_str")
        private_variable = extracted_private_variable_from_template(template_content)
        generate_replace_values, json_dict = [], {}
        if private_variable and replace_values:
            part_user, part_variable = False, False
            if "part_value" == replace_values:
                part_variable = True
            elif "part_user" in replace_values:
                part_user = True
            generate_replace_values = generate_private_variable_replace(recipients, private_variable, part_user, part_variable)
        with allure.step('CN短信发送内容预览接口'):
            json_dict = {
                "channel": "sms",
                "recipients": recipients,
                "template_id": template_id,
                "category": "ads",
                "replace_values": generate_replace_values
            }
            json_dict = {k: v for k, v in json_dict.items() if v}
            inputs = {
                "host": env['host']['app_in'],
                "path": cn_emay_sms_send_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": json_dict
            }
            response = hreq.request(env, inputs)
            if "test" in cmdopt:
                redis["app_message"].delete("rate.limiting:cn/sms_push_10022")
            else:
                logger.debug("非test环境，没有权限清理redis数据")
            assert response['result_code'] == 'success'
