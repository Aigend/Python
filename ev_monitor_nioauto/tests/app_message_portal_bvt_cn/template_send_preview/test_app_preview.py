# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_APP_preview_cn.py
# @Author : qiangwei.zhang
# @time: 2021/08/25
# @api: POST_/api/2/in/message_portal/template/tob/app/preview
# @showdoc: http://showdoc.nevint.com/index.php?s=/647&page_id=31803
# @Description :脚本描述
import time
import allure
import pytest
from utils.http_client import TSPRequest as hreq
from tests.app_message_portal.template_management.template_server import init_app_template, get_template_detail
from tests.app_message_portal.variable_management.variable_server import extracted_private_variable_from_template, generate_private_variable_replace, verify_variable
from utils.logger import logger

tob_app_preview_path = "/api/2/in/message_portal/template/tob/app/preview"
toc_app_preview_path = "/api/2/in/message_portal/template/toc/app/preview"
app_id = 10000


class TestAppReview(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_template(self, env, mysql):
        return init_app_template(env, mysql)

    app_template_preview_keys = "case_name,template_name,replace_values,host_key,data_key"
    app_template_preview_cases = [
        ("TOC_正案例_公共变量+自定义变量模板_有多个重复变量", "APP_L_R_repeat", "all", "app_in", "nmp_app"),
        ("TOC_正案例_公共变量+自定义变量模板_变量不重复", "APP_L_R_no_repeat", "all", "app_in", "nmp_app"),
        ("TOB_正案例_无变量模板", "APP_TOB_no_variable", None, "app_tob_in", "nmp_app_tob"),
        ("TOB_正案例_只有公共变量模板_变量无重复", "APP_TOB_R_no_repeat", None, "app_tob_in", "nmp_app_tob"),
        ("TOB_正案例_只有自定义变量模板_变量有重复", "APP_TOB_L_repeat", "all", "app_tob_in", "nmp_app_tob"),
        ("TOB_正案例_公共变量+自定义变量模板_有多个重复变量", "APP_TOB_L_R_repeat", "all", "app_tob_in", "nmp_app_tob"),
    ]
    app_template_preview_ids = [f"{case[0]}" for case in app_template_preview_cases]

    @pytest.mark.parametrize(app_template_preview_keys, app_template_preview_cases, ids=app_template_preview_ids)
    def test_app_template_preview(self, env, cmdopt, mysql, case_name, template_name, replace_values, prepare_template, host_key, data_key):
        if host_key == "app_tob_in" and cmdopt not in ['test_marcopolo', 'stg_marcopolo']:
            logger.debug(f"【{cmdopt}】环境暂不支持{host_key}服务邮件推送")
            return 0
        template_id_map = prepare_template
        template_id = template_id_map.get(template_name)
        template_detail = get_template_detail(env, template_id)
        template_content = template_detail.get("data").get("template_str")
        logger.debug(f"template_content:{template_content}")
        template_content = template_content.replace("true", "True")
        private_variable = extracted_private_variable_from_template(template_content)
        account_ids = "100,101,102,103"
        generate_replace_values = generate_private_variable_replace(account_ids, private_variable)
        with allure.step('APP发送内容预览接口'):
            json_dict = {
                "account_ids": account_ids,
                "template_id": template_id,
                "replace_values": generate_replace_values
            }
            inputs = {
                "host": env['host']["app_in"],
                "path": tob_app_preview_path if host_key == "app_tob_in" else toc_app_preview_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": json_dict
            }
            response = hreq.request(env, inputs)
            assert response['result_code'] == 'success'
        with allure.step('验证替换参数正常替换'):
            verify_variable(response, account_ids, generate_replace_values)
