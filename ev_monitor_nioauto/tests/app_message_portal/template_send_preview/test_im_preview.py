# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_im_preview_cn.py
# @Author : qiangwei.zhang
# @time: 2021/08/25
# @api: POST_/api/2/in/message_portal/template/tob/im/preview
# @showdoc: http://showdoc.nevint.com/index.php?s=/647&page_id=31803
# @Description :脚本描述
import time
import allure
import pytest
from utils.http_client import TSPRequest as hreq
from tests.app_message_portal.template_management.template_server import init_im_template, get_template_detail
from tests.app_message_portal.variable_management.variable_server import extracted_private_variable_from_template, generate_private_variable_replace, verify_variable
from utils.logger import logger

tob_im_preview_path = "/api/2/in/message_portal/template/cn/im/preview"
tob_im_preview_eu_path = "/api/2/in/message_portal/template/eu/im/preview"
toc_im_preview_path = "/api/2/in/message_portal/template/cn/im/send"
app_id = 10000


class TestImReview(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_template(self, env, mysql):
        return init_im_template(env, mysql)

    im_template_preview_keys = "case_name,template_name,replace_values,host_key,data_key"
    im_template_preview_cases = [
        # TOC
        ("TOC_正案例_无变量模板", "IM_no_variable_V1", None, "app_in", "nmp_app"),
        ("TOC_正案例_只有公共变量模板_变量无重复", "IM_R_no_repeat_V1", None, "app_in", "nmp_app"),
        ("TOC_正案例_只有公共变量模板_变量有重复", "IM_R_repeat_V1", None, "app_in", "nmp_app"),
        ("TOC_正案例_只有自定义变量模板_变量无重复", "IM_L_no_repeat_V1", "all", "app_in", "nmp_app"),
        ("TOC_正案例_只有自定义变量模板_变量有重复", "IM_L_repeat_V1", "all", "app_in", "nmp_app"),
        ("TOC_正案例_公共变量+自定义变量模板_有多个重复变量", "IM_L_R_repeat_V1", "all", "app_in", "nmp_app"),
        ("TOC_正案例_公共变量+自定义变量模板_变量不重复", "IM_L_R_no_repeat_V1", "all", "app_in", "nmp_app"),
        ("TOC_反案例_公共变量_部分有对应url", "IM_R_part_value_V1", None, "app_in", "nmp_app"),
        ("TOC_反案例_公共变量_全部无对应url", "IM_R_no_value_V1", None, "app_in", "nmp_app"),
        ("TOC_反案例_公共变量_部分用户有对应url", "IM_R_part_user_V1", None, "app_in", "nmp_app"),
        ("TOC_反案例_自定义变量_部分字段有替换", "IM_L_part_value_V1", "part_value", "app_in", "nmp_app"),
        ("TOC_反案例_自定义变量_全部字段无替换", "IM_L_no_value_V1", None, "app_in", "nmp_app"),
        ("TOC_反案例_自定义变量_部分用户有替换", "IM_L_part_user_V1", "part_user", "app_in", "nmp_app"),
        ("TOC_反案例_自定义变量_全部用户无替换", "IM_L_no_user_V1", None, "app_in", "nmp_app"),
        ("TOC_反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值", "IM_L_value_R_part_value_V1", "all", "app_in", "nmp_app"),
        ("TOC_反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分用户有对应替换值", "IM_L_user_R_part_user_V1", "all", "app_in", "nmp_app"),
        ("TOC_反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量无对应替换值", "IM_L_value_R_no_value_V1", "all", "app_in", "nmp_app"),
        ("TOC_反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量全部无替换值", "IM_R_L_no_value_V1", None, "app_in", "nmp_app"),
        ("TOC_反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分字段有替换值", "IM_R_L_part_value_V1", "part_value", "app_in", "nmp_app"),
        ("TOC_反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分用户有替换值", "IM_R_L_part_user_V1", "part_user", "app_in", "nmp_app"),
    ]
    im_template_preview_ids = [f"{case[0]}" for case in im_template_preview_cases]

    @pytest.mark.parametrize(im_template_preview_keys, im_template_preview_cases, ids=im_template_preview_ids)
    def test_im_template_preview(self, env, cmdopt, mysql, case_name, template_name, replace_values, prepare_template, host_key, data_key):
        # if cmdopt in ['test_marcopolo', 'stg_marcopolo']:
        #     logger.debug(f"【{cmdopt}】环境暂不支持{host_key}服务邮件推送")
        #     return 0
        template_id_map = prepare_template
        template_id = template_id_map.get(template_name)
        template_detail = get_template_detail(env, template_id)
        template_content = template_detail.get("data").get("template_str")
        logger.debug(f"template_content:{template_content}")
        template_content = template_content.replace("true", "True")
        private_variable = extracted_private_variable_from_template(template_content)
        account_ids = "113,434343444,78492741,38747927434"
        generate_replace_values, json_dict = [], {}
        if private_variable and replace_values:
            part_user, part_variable = False, False
            if "part_value" == replace_values:
                part_variable = True
            elif "part_user" in replace_values:
                part_user = True
            generate_replace_values = generate_private_variable_replace(account_ids, private_variable, part_user, part_variable)
        with allure.step('im发送内容预览接口'):
            json_dict = {
                "account_ids": account_ids,
                "template_id": template_id,
                "replace_values": generate_replace_values
            }
            inputs = {
                "host": env['host']["app_in"],
                "path": tob_im_preview_eu_path if "marcopolo" in cmdopt else tob_im_preview_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": json_dict
            }
            response = hreq.request(env, inputs)
            assert response['result_code'] == 'success'
        with allure.step('验证替换参数正常替换'):
            verify_variable(response, account_ids, generate_replace_values)
