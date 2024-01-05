# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_template_add.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/10 4:02 下午
# @Description :

import time
import allure
import pytest

from tests.app_message_center.clear_rate_limit import clear_rate_limit
from utils.logger import logger
from utils.http_client import TSPRequest as hreq
from tests.app_message_portal.template_management.template_server import init_email_template, get_template_detail
from tests.app_message_portal.variable_management.variable_server import extracted_private_variable_from_template, generate_private_variable_replace

employee_email_preview = "/api/2/in/message_portal/template/employee/email/preview"
employee_email_send_path = "/api/2/in/message_portal/template/employee/email/send"
recipients = "colin.li@nio.com,chunyan.liu1@nio.com"
bcc_recipients = "dun.yuan@nio.com"
cc_recipients = "qiangwei.zhang@nio.com"
app_id = 10000


# app_id = 100480
# app_id = 1000045


class TestTemplateReview(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_template(self, env, mysql):
        return init_email_template(env, mysql)

    @pytest.mark.parametrize("case_name,template_name,replace_values,cc_recipients,bcc_recipients", [
        # ("正案例_无变量模板", "no_variable", None, None, None),
        # ("正案例_公共变量+自定义变量模板_H5模板", "H5_R_L", "all", None, None),
        # ("正案例_只有公共变量模板_变量无重复", "R_no_repeat", None, None, None),
        # ("正案例_只有公共变量模板_变量有重复", "R_repeat", None, None, None),
        # ("正案例_只有自定义变量模板_变量无重复", "L_no_repeat", "all", None, None),
        # ("正案例_只有自定义变量模板_变量有重复", "L_repeat", "all", None, None),
        # ("正案例_公共变量+自定义变量模板_有多个重复变量", "L_R_repeat", "all", None, None),
        ("正案例_公共变量+自定义变量模板_变量不重复", "L_R_no_repeat", "all", cc_recipients, bcc_recipients),
        # ("反案例_公共变量_部分有对应url", "R_part_value", None, None, None),
        # ("反案例_公共变量_全部无对应url", "R_no_value", None, None, None),
        # ("反案例_公共变量_部分用户有对应url", "R_part_user", None, None, None),
        # ("反案例_自定义变量_部分字段有替换", "L_part_value", "part_value", None, None),
        # ("反案例_自定义变量_全部字段无替换", "L_no_value", None, None, None),
        # ("反案例_自定义变量_部分用户有替换", "L_part_user", "part_user", None, None),
        # ("反案例_自定义变量_全部用户无替换", "L_no_user", None, None, None),
        # ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值", "L_value_R_part_value", "all", None, None),
        # ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分用户有对应替换值", "L_user_R_part_user", "all", None, None),
        # ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量无对应替换值", "L_value_R_no_value", "all", None, None),
        # ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量全部无替换值", "R_L_no_value", None, None, None),
        # ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分字段有替换值", "R_L_part_value", "part_value", None, None),
        # ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分用户有替换值", "R_L_part_user", "part_user", None, None),
    ])
    def test_email_template_push_employee(self, env, cmdopt, mysql, redis, case_name, template_name, replace_values, prepare_template, cc_recipients, bcc_recipients):
        """
            接口文档 http://showdoc.nevint.com/index.php?s=/647&page_id=32670
        """
        clear_rate_limit(redis, cmdopt, 10022)
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
        with allure.step('employee邮件发送内容预览接口'):
            json_dict = {
                "recipients": recipients,
                "template_id": template_id,
                "replace_values": generate_replace_values,
                "cc_recipients": cc_recipients,
                "bcc_recipients": bcc_recipients,
            }
            inputs = {
                "host": env['host']['app_in'],
                "path": employee_email_send_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": json_dict
            }
            response = hreq.request(env, inputs)
            with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
                if "test" in cmdopt:
                    redis["app_message"].delete("rate.limiting:employee/email_direct_push_10022")
                else:
                    logger.debug("非test环境，没有权限清理redis数据")
            assert response['result_code'] == 'success'
            assert response.get("data").get("details")[0].get("result") == 'success'
