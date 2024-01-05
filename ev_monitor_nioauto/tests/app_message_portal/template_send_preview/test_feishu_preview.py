# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_feishu_preview_cn.py
# @Author : qiangwei.zhang
# @time: 2021/08/25
# @api: POST_/api/2/in/message_portal/template/cn/feishu/preview 【必填】
# @showdoc: http://showdoc.nevint.com/index.php?s=/647&page_id=31438
# @Description :脚本描述
import time
import allure
import pytest
from utils.http_client import TSPRequest as hreq

from tests.app_message_portal.template_management.template_server import init_feishu_template, get_template_detail
from tests.app_message_portal.variable_management.variable_server import extracted_private_variable_from_template, generate_private_variable_replace, \
    extracted_variable_from_template, verify_variable
from utils.logger import logger

eu_fei_shu_preview_path = "/api/2/in/message_portal/template/eu/feishu/preview"
cn_fei_shu_preview_path = "/api/2/in/message_portal/template/cn/feishu/preview"
# recipients = "qiangwei.zhang@nio.com,qiangwei.zhang1@nio.com,qiangwei.zhang2@nio.com"
test_data_map = {"recipients": "qiangwei.zhang@nio.com,qiangwei.zhang1@nio.com,qiangwei.zhang2@nio.com", "user_ids": "1234,2345", "account_ids": "1234,2345"}
app_id = 10000

cn_allow_environment = ['test', 'stg']
eu_allow_environment = ['test_marcopolo', 'stg_marcopolo']


class TestTemplateReview(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_template(self, env, mysql):
        return init_feishu_template(env, mysql)

    fei_shu_review_cn_keys = "case_name,template_name,replace_values,user_key"
    fei_shu_review_cn_cases = [
        ("正案例_无变量模板", "FEISHU_no_variable", None, "recipients"),
        ("正案例_只有公共变量模板_变量无重复", "FEISHU_R_no_repeat", None, "recipients"),
        ("正案例_只有公共变量模板_变量有重复", "FEISHU_R_repeat", None, "recipients"),
        ("正案例_只有自定义变量模板_变量无重复", "FEISHU_L_no_repeat", "all", "recipients"),
        ("正案例_只有自定义变量模板_变量有重复", "FEISHU_L_repeat", "all", "recipients"),
        ("正案例_公共变量+自定义变量模板_有多个重复变量", "FEISHU_L_R_repeat", "all", "recipients"),
        ("正案例_公共变量+自定义变量模板_变量不重复", "FEISHU_L_R_no_repeat", "all", "recipients"),
        ("反案例_公共变量_部分有对应url", "FEISHU_R_part_value", None, "recipients"),
        ("反案例_公共变量_全部无对应url", "FEISHU_R_no_value", None, "recipients"),
        ("反案例_公共变量_部分用户有对应url", "FEISHU_R_part_user", None, "recipients"),
        ("反案例_自定义变量_部分字段有替换", "FEISHU_L_part_value", "part_value", "recipients"),
        ("反案例_自定义变量_全部字段无替换", "FEISHU_L_no_value", None, "recipients"),
        ("反案例_自定义变量_部分用户有替换", "FEISHU_L_part_user", "part_user", "recipients"),
        ("反案例_自定义变量_全部用户无替换", "FEISHU_L_no_user", None, "recipients"),
        ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值", "FEISHU_L_value_R_part_value", "all", "recipients"),
        ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分用户有对应替换值", "FEISHU_L_user_R_part_user", "all", "recipients"),
        ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量无对应替换值", "FEISHU_L_value_R_no_value", "all", "recipients"),
        ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量全部无替换值", "FEISHU_R_L_no_value", None, "recipients"),
        ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分字段有替换值", "FEISHU_R_L_part_value", "part_value", "recipients"),
        ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分用户有替换值", "FEISHU_R_L_part_user", "part_user", "recipients"),
    ]
    fei_shu_review_cn_ids = [f"{case[0]}" for case in fei_shu_review_cn_cases]

    @pytest.mark.parametrize(fei_shu_review_cn_keys, fei_shu_review_cn_cases, ids=fei_shu_review_cn_ids)
    def test_fei_shu_review_cn(self, env, cmdopt, mysql, case_name, template_name, replace_values, prepare_template, user_key):
        """
            接口文档 http://showdoc.nevint.com/index.php?s=/647&page_id=32599
        """
        if cmdopt not in cn_allow_environment:
            logger.debug(f"该案例允许执行的环境为{cn_allow_environment};不在【{cmdopt}】环境执行")
            return 0
        template_id_map = prepare_template
        template_id = template_id_map.get(template_name)
        template_detail = get_template_detail(env, template_id)
        template_content = template_detail.get("data").get("template_str")
        private_variable = extracted_private_variable_from_template(template_content)
        generate_replace_values, json_dict = [], {}
        user_info = test_data_map.get(user_key)

        if private_variable and replace_values:
            part_user, part_variable = False, False
            if "part_value" == replace_values:
                part_variable = True
            elif "part_user" in replace_values:
                part_user = True
            generate_replace_values = generate_private_variable_replace(user_info, private_variable, part_user, part_variable)

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
                "path": cn_fei_shu_preview_path,
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

    fei_shu_review_eu_keys = "case_name,template_name,replace_values,user_key"
    fei_shu_review_eu_cases = [
        ("正案例_无变量模板", "FEISHU_no_variable", None, "recipients"),
        ("正案例_只有公共变量模板_变量无重复", "FEISHU_R_no_repeat", None, "recipients"),
        ("正案例_只有公共变量模板_变量有重复", "FEISHU_R_repeat", None, "recipients"),
        ("正案例_只有自定义变量模板_变量无重复", "FEISHU_L_no_repeat", "all", "recipients"),
        ("正案例_只有自定义变量模板_变量有重复", "FEISHU_L_repeat", "all", "recipients"),
        ("正案例_公共变量+自定义变量模板_有多个重复变量", "FEISHU_L_R_repeat", "all", "recipients"),
        ("正案例_公共变量+自定义变量模板_变量不重复", "FEISHU_L_R_no_repeat", "all", "recipients"),
        ("反案例_公共变量_部分有对应url", "FEISHU_R_part_value", None, "recipients"),
        ("反案例_公共变量_全部无对应url", "FEISHU_R_no_value", None, "recipients"),
        ("反案例_公共变量_部分用户有对应url", "FEISHU_R_part_user", None, "recipients"),
        ("反案例_自定义变量_部分字段有替换", "FEISHU_L_part_value", "part_value", "recipients"),
        ("反案例_自定义变量_全部字段无替换", "FEISHU_L_no_value", None, "recipients"),
        ("反案例_自定义变量_部分用户有替换", "FEISHU_L_part_user", "part_user", "recipients"),
        ("反案例_自定义变量_全部用户无替换", "FEISHU_L_no_user", None, "recipients"),
        ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值", "FEISHU_L_value_R_part_value", "all", "recipients"),
        ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分用户有对应替换值", "FEISHU_L_user_R_part_user", "all", "recipients"),
        ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量无对应替换值", "FEISHU_L_value_R_no_value", "all", "recipients"),
        ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量全部无替换值", "FEISHU_R_L_no_value", None, "recipients"),
        ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分字段有替换值", "FEISHU_R_L_part_value", "part_value", "recipients"),
        ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分用户有替换值", "FEISHU_R_L_part_user", "part_user", "recipients"),
    ]
    fei_shu_review_eu_ids = [f"{case[0]}" for case in fei_shu_review_eu_cases]

    @pytest.mark.parametrize(fei_shu_review_eu_keys, fei_shu_review_eu_cases, ids=fei_shu_review_eu_ids)
    def test_fei_shu_review_eu(self, env, cmdopt, mysql, case_name, template_name, replace_values, prepare_template, user_key):
        """
            接口文档 http://showdoc.nevint.com/index.php?s=/647&page_id=32599
        """
        if cmdopt not in eu_allow_environment:
            logger.debug(f"该案例允许执行的环境为{eu_allow_environment};不在【{cmdopt}】环境执行")
            return 0
        template_id_map = prepare_template
        template_id = template_id_map.get(template_name)
        template_detail = get_template_detail(env, template_id)
        template_content = template_detail.get("data").get("template_str")
        private_variable = extracted_private_variable_from_template(template_content)
        generate_replace_values, json_dict = [], {}
        user_info = test_data_map.get(user_key)
        if private_variable and replace_values:
            part_user, part_variable = False, False
            if "part_value" == replace_values:
                part_variable = True
            elif "part_user" in replace_values:
                part_user = True
            generate_replace_values = generate_private_variable_replace(user_info, private_variable, part_user, part_variable)

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
                "path": eu_fei_shu_preview_path,
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
