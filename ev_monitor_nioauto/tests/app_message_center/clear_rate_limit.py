# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : clear_rate_limit.py
# @Author : qiangwei.zhang
# @time: 2022/06/09
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import allure


def clear_rate_limit(redis, cmdopt="test", app_id=10000):
    with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
        if "test" in cmdopt:
            redis["app_message"].delete(f"rate.limiting:employee/email_push_{app_id}")
            redis["app_message"].delete(f"rate.limiting:cn/email_push_{app_id}")
            redis["app_message"].delete(f"rate.limiting:eu/email_push_{app_id}")
            redis["app_message"].delete(f"rate.limiting:cn/email_direct_push_{app_id}")
            redis["app_message"].delete(f"rate.limiting:eu/email_direct_push_{app_id}")
            redis["app_message"].delete(f"rate.limiting:employee/email_direct_push_{app_id}")
            redis["app_message"].delete(f"rate.limiting:cn/sms_push_{app_id}")
            redis["app_message"].delete(f"rate.limiting:eu/sms_push_{app_id}")
            redis["app_message"].delete(f"rate.limiting:marketing_sms_{app_id}")
