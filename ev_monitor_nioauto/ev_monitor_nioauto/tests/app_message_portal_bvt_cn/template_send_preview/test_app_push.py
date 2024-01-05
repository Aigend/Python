# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_APP_push_cn.py
# @Author : qiangwei.zhang
# @time: 2021/08/25
# @api: POST_/api/2/in/message_portal/template/tob/app/push
# @showdoc: http://showdoc.nevint.com/index.php?s=/647&page_id=31803
# @Description :脚本描述
import time
import allure
import pytest
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from tests.app_message_portal.template_management.template_server import init_app_template, get_template_detail
from tests.app_message_portal.variable_management.variable_server import extracted_private_variable_from_template, generate_private_variable_replace

tob_app_send_path = "/api/2/in/message_portal/template/tob/app/send"
toc_app_send_path = "/api/2/in/message_portal/template/toc/app/send"
# account_ids = "397571871,17610551934"
app_id = 10000

content = {
    "target_link": "http://www.niohome.com",
    "description": "description【[#description#]】time:[#time#]",
    "title": "【[*name*]】你好，模板推送测试渠道推送测试,如有打扰请见谅【[#title#]】"
}



# app_id = 1000075


class TestAppPush(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_template(self, env, mysql):
        return init_app_template(env, mysql)

    app_template_push_keys = "case_name,template_name,replace_values,host_key,data_key"
    app_template_push_cases = [
        # TOC
        ("TOC_正案例_无变量模板", "APP_no_variable", None, "app_in", "nmp_app"),
        ("TOC_正案例_只有公共变量模板_变量无重复", "APP_R_no_repeat", None, "app_in", "nmp_app"),
        ("TOC_正案例_只有公共变量模板_变量有重复", "APP_R_repeat", None, "app_in", "nmp_app"),
        ("TOC_正案例_只有自定义变量模板_变量有重复", "APP_L_repeat", "all", "app_in", "nmp_app"),
        ("TOC_正案例_公共变量+自定义变量模板_有多个重复变量", "APP_L_R_repeat", "all", "app_in", "nmp_app"),
        ("TOC_正案例_公共变量+自定义变量模板_变量不重复", "APP_L_R_no_repeat", "all", "app_in", "nmp_app"),
        # # TOB
        ("TOB_正案例_无变量模板", "APP_TOB_no_variable", None, "app_tob_in", "nmp_app_tob"),
        ("TOB_正案例_只有公共变量模板_变量无重复", "APP_TOB_R_no_repeat", None, "app_tob_in", "nmp_app_tob"),
        ("TOB_正案例_公共变量+自定义变量模板_有多个重复变量", "APP_TOB_L_R_repeat", "all", "app_tob_in", "nmp_app_tob"),
    ]
    app_template_push_ids = [f"{case[0]}" for case in app_template_push_cases]

    @pytest.mark.parametrize(app_template_push_keys, app_template_push_cases, ids=app_template_push_ids)
    def test_app_template_notify(self, env, cmdopt, mysql, case_name, template_name, replace_values, prepare_template, host_key, data_key):
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
        target_app_id = eval(template_content).get("target_app_ids").split(",")[0]
        account_ids = str(env["app_message_keeper"][data_key][int(target_app_id)]["user1"]["account_id"])

        generate_replace_values, json_dict = [], {}
        if private_variable and replace_values:
            part_user, part_variable = False, False
            if "part_value" == replace_values:
                part_variable = True
            elif "part_user" in replace_values:
                part_user = True
            generate_replace_values = generate_private_variable_replace(account_ids, private_variable, part_user, part_variable)
        with allure.step('APP发送内容预览接口'):
            json_dict = {
                "account_ids": account_ids,
                "template_id": template_id,
                "replace_values": generate_replace_values
            }
            inputs = {
                "host": env['host']["app_in"],
                "path": tob_app_send_path if host_key == "app_tob_in" else toc_app_send_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": json_dict
            }
            response = hreq.request(env, inputs)
            assert response['result_code'] == 'success'
            assert len(response.get("data")) == len(account_ids.split(","))
