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

from tests.app_message_center.clear_rate_limit import clear_rate_limit
from utils.http_client import TSPRequest as hreq

from tests.app_message_portal.template_management.template_server import init_sms_template, get_template_detail
from tests.app_message_portal.variable_management.variable_server import extracted_private_variable_from_template, generate_private_variable_replace

eu_sms_send_path = "/api/2/in/message_portal/template/eu/sms/send"
eu_sms_voice_send_path = "/api/2/in/message_portal/template/eu/voice/send"

test_data_map = {"recipients": "+8617610551933", "user_ids": "1234,2345", "account_ids": "1234,2345"}
app_id = 10000


@pytest.mark.skip("manual")
class TestTemplateSend(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_template(self, env, mysql):
        return init_sms_template(env, mysql)

    sms_template_send_eu_keys = "case_name,template_name,replace_values,user_key"
    sms_template_send_eu_cases = [
        # ("正案例_无变量模板", "SMS_no_variable", None, "recipient"),
        # ("正案例_只有公共变量模板_变量无重复", "SMS_R_no_repeat", None, "recipient"),
        # ("正案例_只有公共变量模板_变量有重复", "SMS_R_repeat", None, "recipient"),
        # ("正案例_只有自定义变量模板_变量无重复", "SMS_L_no_repeat", "all", "recipient"),
        # ("正案例_只有自定义变量模板_变量有重复", "SMS_L_repeat", "all", "recipient"),
        ("正案例_公共变量+自定义变量模板_有多个重复变量", "SMS_L_R_repeat", "all", "recipient"),
        # ("正案例_公共变量+自定义变量模板_变量不重复", "SMS_L_R_no_repeat", "all", "recipient"),
        # ("反案例_公共变量_部分有对应url", "SMS_R_part_value", None, "recipient"),
        # ("反案例_公共变量_全部无对应url", "SMS_R_no_value", None, "recipient"),
        # ("反案例_公共变量_部分用户有对应url", "SMS_R_part_user", None, "recipient"),
        # ("反案例_自定义变量_部分字段有替换", "SMS_L_part_value", "part_value", "recipient"),
        # ("反案例_自定义变量_全部字段无替换", "SMS_L_no_value", None, "recipient"),
        # ("反案例_自定义变量_部分用户有替换", "SMS_L_part_user", "part_user", "recipient"),
        # ("反案例_自定义变量_全部用户无替换", "SMS_L_no_user", None, "recipient"),
        # ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值", "SMS_L_value_R_part_value", "all", "recipient"),
        # ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分用户有对应替换值", "SMS_L_user_R_part_user", "all", "recipient"),
        # ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量无对应替换值", "SMS_L_value_R_no_value", "all", "recipient"),
        # ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量全部无替换值", "SMS_R_L_no_value", None, "recipient"),
        # ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分字段有替换值", "SMS_R_L_part_value", "part_value", "recipient"),
        # ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分用户有替换值", "SMS_R_L_part_user", "part_user", "recipient"),
    ]
    sms_template_send_eu_ids = [f"{case[0]}" for case in sms_template_send_eu_cases]

    @pytest.mark.parametrize(sms_template_send_eu_keys, sms_template_send_eu_cases, ids=sms_template_send_eu_ids)
    def test_sms_template_send_eu(self, env, redis, cmdopt, mysql, case_name, template_name, replace_values, prepare_template, user_key):
        """
        7）send by template
            接口文档 http://showdoc.nevint.com/index.php?s=/647&pag/\_id=31438
            api: api/2/in/message/template/cn/send

            字段说明：
            body params:
                * channel: 频道
                    ✅* 必填
                    ✅* email
                    * sms
                ✅* recipients: 收件人
                    ✅* 条件非必填
                    ✅* 多个
                    ✅* 多个有重复
                ✅* subject: 主题
                   ✅ * 条件非必填
                   ✅ * 邮件必填
                   ✅ * 短信非必填
                * template_id: 模板ID
                    ✅* 必填
                * category: 渠道
                    ✅* 必填
                * replace_values: 替换的值
                    ✅* 非必填
                    ✅* list
                    ✅* 多个用户
                    ✅* 多个替换值
                    ✅* 相同的替换内容
                """
        clear_rate_limit(redis, cmdopt, 10022)
        template_id_map = prepare_template
        template_id = template_id_map.get(template_name)
        template_detail = get_template_detail(env, template_id)
        template_content = template_detail.get("data").get("template_str")
        private_variable = extracted_private_variable_from_template(template_content)
        generate_replace_values, json_dict = [], {}
        user_info = env["push_sms"].get(user_key)
        # user_info = "+8618612709129"
        if private_variable and replace_values:
            part_user, part_variable = False, False
            if "part_value" == replace_values:
                part_variable = True
            elif "part_user" in replace_values:
                part_user = True
            generate_replace_values = generate_private_variable_replace(user_info, private_variable, part_user, part_variable)
        with allure.step('CN短信发送内容预览接口'):
            json_dict = {
                "channel": "sms",
                f"{user_key}s": user_info,
                "template_id": template_id,
                "category": "ads",
                "replace_values": generate_replace_values
            }
            json_dict = {k: v for k, v in json_dict.items() if v}
            inputs = {
                "host": env['host']['app_in'],
                "path": eu_sms_send_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": json_dict
            }
            response = hreq.request(env, inputs)
            assert response['result_code'] == 'success'
            # assert len(response.get("data")) == len(user_info.split(",")) + 1

    sms_voice_template_send_eu_keys = "case_name,template_name,replace_values,user_key"
    sms_voice_template_send_eu_cases = [
        # ("正案例_无变量模板", "SMS_no_variable", None, "recipient"),
        # ("正案例_只有公共变量模板_变量无重复", "SMS_R_no_repeat", None, "recipient"),
        # ("正案例_只有公共变量模板_变量有重复", "SMS_R_repeat", None, "recipient"),
        # ("正案例_只有自定义变量模板_变量无重复", "SMS_L_no_repeat", "all", "recipient"),
        # ("正案例_只有自定义变量模板_变量有重复", "SMS_L_repeat", "all", "recipient"),
        ("正案例_公共变量+自定义变量模板_有多个重复变量", "SMS_L_R_repeat", "all", "recipient"),
        # ("正案例_公共变量+自定义变量模板_变量不重复", "SMS_L_R_no_repeat", "all", "recipient"),
        # ("反案例_公共变量_部分有对应url", "SMS_R_part_value", None, "recipient"),
        # ("反案例_公共变量_全部无对应url", "SMS_R_no_value", None, "recipient"),
        # ("反案例_公共变量_部分用户有对应url", "SMS_R_part_user", None, "recipient"),
        # ("反案例_自定义变量_部分字段有替换", "SMS_L_part_value", "part_value", "recipient"),
        # ("反案例_自定义变量_全部字段无替换", "SMS_L_no_value", None, "recipient"),
        # ("反案例_自定义变量_部分用户有替换", "SMS_L_part_user", "part_user", "recipient"),
        # ("反案例_自定义变量_全部用户无替换", "SMS_L_no_user", None, "recipient"),
        # ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值", "SMS_L_value_R_part_value", "all", "recipient"),
        # ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分用户有对应替换值", "SMS_L_user_R_part_user", "all", "recipient"),
        # ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量无对应替换值", "SMS_L_value_R_no_value", "all", "recipient"),
        # ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量全部无替换值", "SMS_R_L_no_value", None, "recipient"),
        # ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分字段有替换值", "SMS_R_L_part_value", "part_value", "recipient"),
        # ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分用户有替换值", "SMS_R_L_part_user", "part_user", "recipient"),
    ]
    sms_voice_template_send_eu_ids = [f"{case[0]}" for case in sms_voice_template_send_eu_cases]

    @pytest.mark.parametrize(sms_voice_template_send_eu_keys, sms_voice_template_send_eu_cases, ids=sms_voice_template_send_eu_ids)
    def test_sms_voice_template_send_eu(self, env, cmdopt, mysql, case_name, template_name, replace_values, prepare_template, user_key):
        """
        7）send by template
            接口文档 http://showdoc.nevint.com/index.php?s=/647&pag/\_id=31438
            api: api/2/in/message/template/cn/send

            字段说明：
            body params:
                * channel: 频道
                    ✅* 必填
                    ✅* email
                    * sms
                ✅* recipients: 收件人
                    ✅* 条件非必填
                    ✅* 多个
                    ✅* 多个有重复
                ✅* subject: 主题
                   ✅ * 条件非必填
                   ✅ * 邮件必填
                   ✅ * 短信非必填
                * template_id: 模板ID
                    ✅* 必填
                * category: 渠道
                    ✅* 必填
                * replace_values: 替换的值
                    ✅* 非必填
                    ✅* list
                    ✅* 多个用户
                    ✅* 多个替换值
                    ✅* 相同的替换内容
                """
        template_id_map = prepare_template
        template_id = template_id_map.get(template_name)
        template_detail = get_template_detail(env, template_id)
        template_content = template_detail.get("data").get("template_str")
        private_variable = extracted_private_variable_from_template(template_content)
        generate_replace_values, json_dict = [], {}
        user_info = env["push_sms"].get(user_key)
        # user_info = "+8618612709129"
        if private_variable and replace_values:
            part_user, part_variable = False, False
            if "part_value" == replace_values:
                part_variable = True
            elif "part_user" in replace_values:
                part_user = True
            generate_replace_values = generate_private_variable_replace(user_info, private_variable, part_user, part_variable)
        with allure.step('EU语音短信发送接口'):
            json_dict = {
                "channel": "sms",
                f"{user_key}s": user_info,
                "template_id": template_id,
                "category": "ads",
                "replace_values": generate_replace_values
            }
            json_dict = {k: v for k, v in json_dict.items() if v}
            inputs = {
                "host": env['host']['app_in'],
                "path": eu_sms_voice_send_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": json_dict
            }
            response = hreq.request(env, inputs)
            assert response['result_code'] == 'success'
            # assert len(response.get("data")) == len(user_info.split(",")) + 1
