# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_im_push_cn.py
# @Author : qiangwei.zhang
# @time: 2021/08/25
# @api: POST_/api/2/in/message_portal/template/tob/im/push
# @showdoc: http://showdoc.nevint.com/index.php?s=/647&page_id=31803
# @Description :脚本描述
import time
import allure
import pytest
from utils.http_client import TSPRequest as hreq
from tests.app_message_portal.template_management.template_server import init_im_template, get_template_detail
from tests.app_message_portal.variable_management.variable_server import extracted_private_variable_from_template, generate_private_variable_replace, verify_variable
from utils.logger import logger

tob_im_push_path = "/api/2/in/message_portal/template/cn/im/send"
toc_im_push_path = "/api/2/in/message_portal/template/cn/im/send"
tob_im_push_eu_path = "/api/2/in/message_portal/template/eu/im/send"
toc_im_push_eu_path = "/api/2/in/message_portal/template/eu/im/send"
app_id = 10000


class TestImReview(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_template(self, env, mysql):
        return init_im_template(env, mysql)

    im_template_push_keys = "case_name,template_name,replace_values,host_key,data_key"
    im_template_push_cases = [
        # TOC
        ("TOC_正案例_无变量模板", "IM_no_variable_V1", "all", "app_in", "nmp_app"),
        ("TOC_正案例_IM_By_Account", "IM_L_R_repeat_No_From_V1", "all", "app_in", "nmp_app"),
        ("TOC_正案例_只有公共变量模板_变量无重复", "IM_R_no_repeat_V1", "all", "app_in", "nmp_app"),
        ("TOC_正案例_只有公共变量模板_变量有重复", "IM_R_repeat_V1", "all", "app_in", "nmp_app"),
        ("TOC_正案例_只有自定义变量模板_变量无重复", "IM_L_no_repeat_V1", "all", "app_in", "nmp_app"),
        ("TOC_正案例_只有自定义变量模板_变量有重复", "IM_L_repeat_V1", "all", "app_in", "nmp_app"),
        ("TOC_正案例_公共变量+自定义变量模板_有多个重复变量", "IM_L_R_repeat_V1", "all", "app_in", "nmp_app"),
        ("TOC_正案例_公共变量+自定义变量模板_变量不重复", "IM_L_R_no_repeat_V1", "all", "app_in", "nmp_app"),
        ("TOC_反案例_公共变量_部分有对应url", "IM_R_part_value_V1", "all", "app_in", "nmp_app"),
        ("TOC_反案例_公共变量_全部无对应url", "IM_R_no_value_V1", "all", "app_in", "nmp_app"),
        ("TOC_反案例_公共变量_部分用户有对应url", "IM_R_part_user_V1", "all", "app_in", "nmp_app"),
        ("TOC_反案例_自定义变量_部分字段有替换", "IM_L_part_value_V1", "part_value", "app_in", "nmp_app"),
        ("TOC_反案例_自定义变量_全部字段无替换", "IM_L_no_value_V1", "all", "app_in", "nmp_app"),
        ("TOC_反案例_自定义变量_部分用户有替换", "IM_L_part_user_V1", "part_user", "app_in", "nmp_app"),
        ("TOC_反案例_自定义变量_全部用户无替换", "IM_L_no_user_V1", "all", "app_in", "nmp_app"),
        ("TOC_反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值", "IM_L_value_R_part_value_V1", "all", "app_in", "nmp_app"),
        ("TOC_反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分用户有对应替换值", "IM_L_user_R_part_user_V1", "all", "app_in", "nmp_app"),
        ("TOC_反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量无对应替换值", "IM_L_value_R_no_value_V1", "all", "app_in", "nmp_app"),
        ("TOC_反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量全部无替换值", "IM_R_L_no_value_V1", "all", "app_in", "nmp_app"),
        ("TOC_反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分字段有替换值", "IM_R_L_part_value_V1", "part_value", "app_in", "nmp_app"),
        ("TOC_反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分用户有替换值", "IM_R_L_part_user_V1", "part_user", "app_in", "nmp_app"),
    ]
    im_template_push_ids = [f"{case[0]}" for case in im_template_push_cases]

    @pytest.mark.parametrize(im_template_push_keys, im_template_push_cases, ids=im_template_push_ids)
    def test_im_template_push(self, env, cmdopt, mysql, case_name, template_name, replace_values, prepare_template, host_key, data_key):
        if cmdopt in ['test_marcopolo', 'stg_marcopolo'] and 'IM_By_Account' in case_name:
            logger.debug(f"【{cmdopt}】环境暂不支持IM push by account")
            return 0
        template_id_map = prepare_template
        template_id = template_id_map.get(template_name)
        template_detail = get_template_detail(env, template_id)
        template_content = template_detail.get("data").get("template_str")
        logger.debug(f"template_content:{template_content}")
        template_content = template_content.replace("true", "True")
        private_variable = extracted_private_variable_from_template(template_content)
        target_app_id = ("10001", "10002")
        if "marcopolo" in cmdopt:
            target_app_id = ("1000003", "1000004")
        user_info_mysql = mysql["nmp_app"].fetch("bindings", where_model={'visible': 1, 'user_id>': 1000, 'app_id in': target_app_id}, fields=["account_id", "user_id"],
                                                 suffix=f"group by user_id limit 2")
        # account_ids = "14967171,1223211"
        account_ids = ",".join([str(u.get("user_id")) for u in user_info_mysql])
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
                "recipients": account_ids,
                "template_id": template_id,
                "replace_values": generate_replace_values,
            }
            if 'No_From' in template_name:
                json_dict["from"] = user_info_mysql[0].get("user_id")
            inputs = {
                "host": env['host']["app_in"],
                "path": tob_im_push_eu_path if "marcopolo" in cmdopt else tob_im_push_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": json_dict
            }
            response = hreq.request(env, inputs)
            assert response['result_code'] == 'success'
