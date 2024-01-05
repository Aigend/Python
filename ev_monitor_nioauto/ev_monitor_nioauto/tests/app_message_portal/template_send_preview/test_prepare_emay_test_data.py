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
from utils.http_client import TSPRequest as hreq
from utils.random_tool import random_int
from utils.message_formator import format_to_message_state

from tests.app_message_portal.template_management.template_server import init_sms_template, get_template_detail
from tests.app_message_portal.variable_management.variable_server import extracted_private_variable_from_template, generate_private_variable_replace
from config.settings import BASE_DIR

cn_emay_sms_send_path = "/api/2/in/message_portal/template/cn/marketing_sms/send"
app_id = 10000


@pytest.mark.skip('manual')
class TestTemplateSend(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_template(self, env, mysql):
        return init_sms_template(env, mysql)

    def test_sms_template_send_cn_emay(self, env):
        for i in range(1):
            recipient_list = [f"+86{str(random_int(12))}" for i in range(10)]
            # recipient_list = ["+8617610551933", "+8613691178976"]
            recipients = ",".join(recipient_list)
            # template_id_map = prepare_template
            # template_id = template_id_map.get("SMS_L_R_repeat")
            template_id = 238  # 这个在test环境stg环境都有
            # template_id = 271  # stg环境,只有本地变量
            template_detail = get_template_detail(env, template_id)
            template_content = template_detail.get("data").get("template_str")
            private_variable = extracted_private_variable_from_template(template_content)
            generate_replace_values = generate_private_variable_replace(recipients, private_variable)
            with allure.step('CN短信发送内容预览接口'):
                json_dict = {
                    "channel": "sms",
                    "recipients": recipients,
                    "template_id": template_id,
                    "category": "marketing_sms",
                    "replace_values": generate_replace_values
                }
                inputs = {
                    "host": env['host']['app_in'],
                    "path": cn_emay_sms_send_path,
                    "method": "POST",
                    "headers": {"content-type": "application/json"},
                    "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                    "json": json_dict
                }
            with open(f'{BASE_DIR}/data/emay/emay_sms_inputs_tel_local_10.txt', 'a')as f1:
                f1.write(f'{inputs}\n')


def pare_data():
    with open(f'{BASE_DIR}/data/emay/emay_sms_inputs.txt', 'r')as f1:
        lines = f1.readlines()
        for line in lines:
            # line.replace("\n", '')
            input = eval(line)
            print(input.get("host"))
            print(input.get("path"))
            print(input.get("method"))
            print(input.get("headers"))
            print(input.get("params"))
            print(input.get("json"))
