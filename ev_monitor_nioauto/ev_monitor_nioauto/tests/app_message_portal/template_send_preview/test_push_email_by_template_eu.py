# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_template_add.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/10 4:02 下午
# @Description :

import os
import time

import allure
import pytest

from tests.app_message_center.clear_rate_limit import clear_rate_limit
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from config.settings import BASE_DIR
from tests.app_message_portal.template_management.template_server import init_email_template, get_template_detail
from tests.app_message_portal.variable_management.variable_server import extracted_private_variable_from_template, generate_private_variable_replace

app_id = 10000
eu_email_send_path = "/api/2/in/message_portal/template/eu/email/send"
allow_environment = ["test_marcopolo", "stg_marcopolo"]


# @pytest.mark.skip("manual")
class TestTemplateReview(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_template(self, env, mysql):
        return init_email_template(env, mysql)

    @pytest.fixture(scope="class")
    def prepare_eu_email_account(self, env, cmdopt):
        cmdopt = "test_marcopolo" if cmdopt == 'test' else cmdopt
        # 消息平台test环境和test_marcopolo环境对应留资test_marcopolo环境
        file_path = f'{BASE_DIR}/config/{cmdopt}/email_account_info_{cmdopt}.txt'
        account_list = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    account_msg = {}
                    account_msg_list = line.split(',')
                    account_msg['account_id'] = account_msg_list[0]
                    account_msg['user_id'] = account_msg_list[1]
                    account_msg['recipient'] = account_msg_list[2]
                    account_msg['password'] = account_msg_list[3]
                    account_list.append(account_msg)
            return account_list
        else:
            logger.error(f"请先配置数据文件{file_path}\n数据格式：account_id,user_id,email,password,pseudo_email,create_time")

    @pytest.mark.parametrize("case_name,template_name,replace_values,user_key", [
        # ("正案例_无变量模板", "no_variable", None, "recipient"),
        # ("正案例_只有公共变量模板_变量无重复", "R_no_repeat", None, "recipient"),
        # ("正案例_只有公共变量模板_变量有重复", "R_repeat", None, "account_id"),
        # ("正案例_只有自定义变量模板_变量无重复", "L_no_repeat", "all", "recipient"),
        # ("正案例_只有自定义变量模板_变量有重复", "L_repeat", "all", "recipient"),
        # ("正案例_公共变量+自定义变量模板_有多个重复变量", "L_R_repeat", "all", "user_id"),
        # ("正案例_公共变量+自定义变量模板_变量不重复", "L_R_no_repeat", "all", "user_id"),
        ("正案例_公共变量+自定义变量模板_H5模板", "H5_R_L", "all", "recipient"),
        # ("反案例_公共变量_部分有对应url", "R_part_value", None, "user_id"),
        # ("反案例_公共变量_全部无对应url", "R_no_value", None, "user_id"),
        # ("反案例_公共变量_部分用户有对应url", "R_part_user", None, "user_id"),
        # ("反案例_自定义变量_部分字段有替换", "L_part_value", "part_value", "user_id"),
        # ("反案例_自定义变量_全部字段无替换", "L_no_value", None, "user_id"),
        # ("反案例_自定义变量_部分用户有替换", "L_part_user", "part_user", "user_id"),
        # ("反案例_自定义变量_全部用户无替换", "L_no_user", None, "user_id"),
        # ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分字段有对应替换值", "L_value_R_part_value", "all", "user_id"),
        # ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量只有部分用户有对应替换值", "L_user_R_part_user", "all", "user_id"),
        # ("反案例_公共变量+自定义变量模板_自定义变量全有替换值，公共变量无对应替换值", "L_value_R_no_value", "all", "user_id"),
        # ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量全部无替换值", "R_L_no_value", None, "user_id"),
        # ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分字段有替换值", "R_L_part_value", "part_value", "user_id"),
        # ("反案例_公共变量+自定义变量模板_公共变量全有替换值，自定义变量部分用户有替换值", "R_L_part_user", "part_user", "user_id"),
    ])
    def test_email_template_review_eu(self, env, cmdopt, mysql, redis, case_name, template_name, replace_values, user_key, prepare_template, prepare_eu_email_account):
        """
            接口文档 http://showdoc.nevint.com/index.php?s=/647&page_id=31438
            api: /api/2/in/message_portal/template/eu/email/preview
        """
        clear_rate_limit(redis, cmdopt, 10022)
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        template_id_map = prepare_template
        template_id = template_id_map.get(template_name)
        template_detail = get_template_detail(env, template_id)
        template_content = template_detail.get("data").get("template_str")
        private_variable = extracted_private_variable_from_template(template_content)
        generate_replace_values, json_dict = [], {}
        # user_info = f"{prepare_eu_email_account[0].get(user_key)},{prepare_eu_email_account[1].get(user_key)}"
        user_info = f"{prepare_eu_email_account[1].get(user_key)}"
        if private_variable and replace_values:
            part_user, part_variable = False, False
            if "part_value" == replace_values:
                part_variable = True
            elif "part_user" in replace_values:
                part_user = True

            generate_replace_values = generate_private_variable_replace(user_info, private_variable, part_user, part_variable)
        with allure.step('EU邮件发送接口'):
            json_dict = {
                "channel": "email",
                f"{user_key}s": user_info,
                "subject": "根据模板发送邮件",
                "template_id": template_id,
                "category": "verify",
                "replace_values": generate_replace_values
            }
            json_dict = {k: v for k, v in json_dict.items() if v}
            inputs = {
                "host": env['host']['app_in'],
                "path": eu_email_send_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": "eu", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": json_dict
            }
            stime = time.time()
            response = hreq.request(env, inputs)
            etime = time.time()
            logger.debug(f"rt:{etime-stime}")
            with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
                if "test" in cmdopt:
                    redis["app_message"].delete("rate.limiting:eu/email_direct_push_10022")
            assert response['result_code'] == 'success'
        with allure.step(f'【{cmdopt}】环境,校验数据存入mysql'):
            details = response["data"]["details"]
            for detail in details:
                if detail["result"] == 'success':
                    message_id = detail['message_id']
                    email_history = mysql["nmp_app"].fetch("email_history", {"message_id": message_id})
                    email_history_meta_info = mysql["nmp_app"].fetch("email_history_meta_info", {"message_id": message_id})
                    assert email_history
                    assert email_history_meta_info
