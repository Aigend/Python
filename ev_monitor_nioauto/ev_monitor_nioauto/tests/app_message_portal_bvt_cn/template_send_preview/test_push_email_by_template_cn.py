# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_template_add.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/10 4:02 下午
# @Description :

import time
import allure
import pytest
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from tests.app_message_portal.template_management.template_server import init_email_template, get_template_detail
from tests.app_message_portal.variable_management.variable_server import extracted_private_variable_from_template, generate_private_variable_replace

recipients = "550736273@qq.com,842244250@qq.com"
app_id = 10000
cn_email_send_path = "/api/2/in/message_portal/template/cn/email/send"
allow_environment = ["test", "stg"]

# @pytest.mark.skip("manual")
class TestTemplateSendEmail(object):
    @pytest.fixture(scope="class", autouse=False)
    def prepare_template(self, env, mysql):
        return init_email_template(env, mysql)

    @pytest.mark.parametrize("case_name,template_name,replace_values", [
        ("正案例_公共变量+自定义变量模板_有多个重复变量", "L_R_repeat", "all"),
    ])
    def test_email_template_send_email_cn(self, env, cmdopt, mysql, redis, case_name, template_name, replace_values, prepare_template):
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
        with allure.step(f"【{cmdopt}】环境,清理{10022}频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete(f"rate.limiting:cn/email_direct_push_10022")
        region = "cn"
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        with allure.step(f"【{cmdopt}】环境,清理10022频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete("rate.limiting:cn/email_direct_push_10022")
            else:
                logger.debug("非test环境，没有权限清理redis数据")
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
                "channel": "email",
                "recipients": recipients,
                "sender_name": "notification@nio.com",
                "subject": "根据模板发送邮件",
                "template_id": template_id,
                "category": "ads",
                "replace_values": generate_replace_values
            }
            inputs = {
                "host": env['host']['app_in'],
                "path": cn_email_send_path,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "params": {"region": region, "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
                "json": json_dict
            }
            response = hreq.request(env, inputs)
            assert response['result_code'] == 'success'
