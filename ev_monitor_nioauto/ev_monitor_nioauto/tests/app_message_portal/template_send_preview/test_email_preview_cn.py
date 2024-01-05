# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_cn_email_preview.py
# @Author : qiangwei.zhang
# @time: 2021/08/06
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import time
import allure
import pytest
from utils.http_client import TSPRequest as hreq

from tests.app_message_portal.template_management.template_server import init_email_template, get_template_detail
from tests.app_message_portal.variable_management.variable_server import extracted_private_variable_from_template, generate_private_variable_replace, verify_variable

cn_email_preview_path = "/api/2/in/message_portal/template/cn/email/preview"
recipients = "550736273@qq.com,842244250@qq.com"
app_id = 10000


class TestTemplateReview(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_template(self, env, mysql):
        return init_email_template(env, mysql)

    @pytest.mark.parametrize("case_name,template_name,replace_values", [
        ("正案例_无变量模板", "no_variable", None),
        ("正案例_只有公共变量模板_变量无重复", "R_no_repeat", None),
        ("正案例_只有公共变量模板_变量有重复", "R_repeat", None),
        ("正案例_只有自定义变量模板_变量无重复", "L_no_repeat", "all"),
        ("正案例_只有自定义变量模板_变量有重复", "L_repeat", "all"),
        ("正案例_公共变量+自定义变量模板_有多个重复变量", "L_R_repeat", "all"),
        ("正案例_公共变量+自定义变量模板_变量不重复", "L_R_no_repeat", "all"),
        ("反案例_公共变量_部分有对应url", "R_part_value", None),
        ("反案例_公共变量_全部无对应url", "R_no_value", None),
        ("反案例_公共变量_部分用户有对应url", "R_part_user", None),
        ("反案例_自定义变量_部分字段有替换", "L_part_value", "part_value"),
        ("反案例_自定义变量_全部字段无替换", "L_no_value", None),
        ("反案例_自定义变量_部分用户有替换", "L_part_user", "part_user"),
        ("反案例_自定义变量_全部用户无替换", "L_no_user", None),
        ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值", "L_value_R_part_value", "all"),
        ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分用户有对应替换值", "L_user_R_part_user", "all"),
        ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量无对应替换值", "L_value_R_no_value", "all"),
        ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量全部无替换值", "R_L_no_value", None),
        ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分字段有替换值", "R_L_part_value", "part_value"),
        ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分用户有替换值", "R_L_part_user", "part_user"),
    ])
    def test_email_template_review_cn(self, env, cmdopt, mysql, case_name, template_name, replace_values, prepare_template):
        """
        7）send by template
            接口文档 http://showdoc.nevint.com/index.php?s=/647&page_id=31438
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
                "replace_values": generate_replace_values
            }
            json_dict = {k: v for k, v in json_dict.items() if v}
            inputs = {
                "host": env['host']['app_in'],
                "path": cn_email_preview_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": json_dict
            }
            response = hreq.request(env, inputs)
            assert response['result_code'] == 'success'
            assert len(response.get("data")) == len(recipients.split(",")) + 1
            with allure.step('验证替换参数正常替换'):
                verify_variable(response, recipients, generate_replace_values)
