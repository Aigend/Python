# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_sms_preview_cn.py
# @Author : qiangwei.zhang
# @time: 2021/08/25
# @api: POST_/api/2/in/message_portal/template/cn/sms/preview 【必填】
# @showdoc: http://showdoc.nevint.com/index.php?s=/647&page_id=31438
# @Description :脚本描述
import time
import allure
import pytest
from utils.http_client import TSPRequest as hreq
from utils.message_formator import format_to_message_state
from tests.app_message_portal.template_management.template_server import init_sms_voice_template, get_template_detail
from tests.app_message_portal.variable_management.variable_server import extracted_private_variable_from_template, generate_private_variable_replace
from utils.assertions import assert_equal
from utils.time_parse import now_utc_strtime

cn_voice_send_path = "/api/2/in/message_portal/template/cn/voice/send"
app_id = 10000


class TestTemplateSend(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_template(self, env, mysql):
        return init_sms_voice_template(env, mysql)

    sms_voice_template_send_cn_keys = "case_name,template_name,replace_values,recipient,message_id_number"
    sms_voice_template_send_cn_cases = [
        ("正案例_正常接听", "SMS_voice_alarm_L_R_repeat", "all", "+8617610551933", 1),
        # ("正案例_不接听", "SMS_voice_alarm_L_R_repeat", "all", "+8613691178976", 1),
        # ("正案例_空号", "SMS_voice_alarm_L_R_repeat", "all", "+8617610551934", 1),
        # ("正案例_停机", "SMS_voice_alarm_L_R_repeat", "all", "+8617000000000", 1),
    ]
    sms_voice_template_send_cn_ids = [f"{case[0]}" for case in sms_voice_template_send_cn_cases]

    # @pytest.mark.skip("manual")
    @pytest.mark.parametrize(sms_voice_template_send_cn_keys, sms_voice_template_send_cn_cases, ids=sms_voice_template_send_cn_ids)
    def test_sms_voice_template_send_cn(self, env, cmdopt, mysql, case_name, template_name, replace_values, recipient, message_id_number, prepare_template):
        """
            # /api/2/message_tracker/tencent_voice_cb

            http://showdoc.nevint.com/index.php?s=/647&page_id=32238
            tencent_voice_cb:
            TencentSMSService.voiceAlarmSdkAppId:1400582412
            TencentSMSService.voiceAlarmTemplateId:1158248

            tencent_voice_cb:412d7aca-3de4-11ec-9ec3-525400d3fe87
            97ca0565-1f88-425e-b4b5-bef535f005f5
            ea56f082-2f66-4046-ab3b-d52de16c7bb0

        """
        with allure.step("调用打电话接口，准备消息ID"):
            template_id_map = prepare_template
            template_id = template_id_map.get(template_name)
            template_detail = get_template_detail(env, template_id)
            template_content = template_detail.get("data").get("template_str")
            private_variable = extracted_private_variable_from_template(template_content)
            generate_replace_values, json_dict = [], {}
            message_id_list = []
            for i in range(message_id_number):
                if private_variable and replace_values:
                    part_user, part_variable = False, False
                    if "part_value" == replace_values:
                        part_variable = True
                    elif "part_user" in replace_values:
                        part_user = True
                    generate_replace_values = generate_private_variable_replace(recipient, private_variable, part_user, part_variable)
                with allure.step('CN语音短信发送接口'):
                    json_dict = {
                        "type": "sms",
                        "recipients": recipient,
                        "template_id": template_id,
                        "replace_values": generate_replace_values
                    }
                    json_dict = {k: v for k, v in json_dict.items() if v}
                    inputs = {
                        "host": env['host']['app_in'],
                        "path": cn_voice_send_path,
                        "method": "POST",
                        "headers": {"Content-Type": "application/json"},
                        "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                        "json": json_dict
                    }
                    response = hreq.request(env, inputs)
                    assert response['result_code'] == 'success'
                    details = response["data"]["details"]
                    for detail in details:
                        message_id = detail.get("message_id")
                        res = mysql['nmp_app'].fetch("message_state", {"message_id": message_id}, retry_num=70)
                        utc_time = now_utc_strtime()[:13]
                        create_time = res[0].get("create_time")[:13]
                        assert create_time == utc_time, f"create_time is not utc time, Expect {utc_time} Actual {create_time}"
                        update_time = res[0].get("update_time")[:13]
                        assert update_time == utc_time, f"update_time is not utc time, Expect {utc_time} Actual {update_time}"
                        message_id_list.append()
                    message_ids = ','.join(message_id_list)
                    time.sleep(120)
        with allure.step("查询trace接口"):
            inputs = {
                "host": env['host']['app_in'],
                "path": "/api/2/in/message_tracker/trace/info",
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {
                    "app_id": "10000",
                    "hash_type": "sha256",
                    'nonce': 'MrVIRwkCLBKySgCG',
                    "sign": ''
                },
                "json": {
                    'message_ids': message_ids,
                }

            }
            response = hreq.request(env, inputs)
            message_state_in_mysql = mysql['nmp_app'].fetch("message_state", where_model={"message_id in": message_ids.split(',')})

            format_mysql_data = format_to_message_state(message_state_in_mysql)
            response.pop("request_id")
            response.pop("server_time")
            expected_result = {
                "data": format_mysql_data,
                "result_code": "success",
            }
            assert_equal(response, expected_result)
