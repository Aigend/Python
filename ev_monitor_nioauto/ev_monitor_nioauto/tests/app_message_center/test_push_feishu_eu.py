# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_push_feishu_eu.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/4/23 4:07 下午
# @Description :

import time
import pytest
from utils.http_client import TSPRequest as hreq
from utils.collection_message_states import collection_message_states
from utils.logger import logger
from data.email_content import markdown_file_title, markdown_file_font, markdown_file_url, markdown_file_img, markdown_file_form, markdown_file_emoji, fei_shu_card

eu_fei_shu_push_path = "/api/2/in/message/employee/eu/feishu_push"
recipients = "qiangwei.zhang@nio.com,colin.li@nio.com"
server_app_id = 10000
allow_environment = ["test_marcopolo", "stg_marcopolo"]


@pytest.mark.run(order=2)
class TestPushFeiShuEU(object):
    """
    1）推送飞书接口
        接口文档 http://showdoc.nevint.com/index.php?s=/647&page_id=30576
        api: /api/2/in/message/employee/cn/feishu_push
        入库校验：数据库不记录
        字段说明：
            * recipients: 收件人
                * 限制数量100
                * 海外飞书企业账号（正常为邮箱账号）
            * title: 主题{不支持变量名称，接口不限制长度}
            * content: 内容{不支持变量名称，接口不限制长度}
                * 文本
                * 不支持html
            * url: 跳转链接，非必填
            topic: swc-cvs-nmp-cn-test-push-feishu
            topic: swc-cvs-nmp-cn-stg-push-feishu
            """

    def test_push_feishu_eu(self, env, cmdopt):
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        inputs = {
            "host": env['host']['app_in'],
            "path": eu_fei_shu_push_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": server_app_id,
                "sign": ""
            },
            "json": {
                "recipients": recipients,
                "title": f"{cmdopt}飞书time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "content": f"【{cmdopt}】环境{eu_fei_shu_push_path}API，飞书推送测试，如有误收请忽略",
                "url": "https://nio.feishu.cn/docs/doccntRo2MGjg51qDbQ0xgFEh0g"
            }
        }
        response = hreq.request(env, inputs)
        assert response['result_code'] == 'success'
        message_id = response['data']['message_id']
        expected_states = [21, 22, 24, 26]
        ms_st = f"{message_id}|{expected_states}|{eu_fei_shu_push_path}"
        collection_message_states(cmdopt, ms_st)

    push_fei_shu_eu_keys = 'case_name,host_key,data_key,content,custom_content_tag'
    push_fei_shu_eu_cases = [
        # ("正案例_TOC_文件标题", 'app_in', 'nmp_app', markdown_file_title, False),
        # ("正案例_TOC_字体", 'app_in', 'nmp_app', markdown_file_font, False),
        # ("正案例_TOC_URL", 'app_in', 'nmp_app', markdown_file_url, False),
        # ("正案例_TOC_图片", 'app_in', 'nmp_app', markdown_file_img, False),
        ("正案例_TOC_表格", 'app_in', 'nmp_app', markdown_file_form, False),
        # ("正案例_TOC_emoji", 'app_in', 'nmp_app', markdown_file_emoji, False),
        # ("正案例_TOB_文件标题", 'app_tob_in', 'nmp_app_tob', markdown_file_title, False),
        ("正案例_TOB_字体", 'app_tob_in', 'nmp_app_tob', markdown_file_font, False),
        # ("正案例_TOB_URL", 'app_tob_in', 'nmp_app_tob', markdown_file_url, False),
        # ("正案例_TOB_图片", 'app_tob_in', 'nmp_app_tob', markdown_file_img, False),
        # ("正案例_TOB_表格", 'app_tob_in', 'nmp_app_tob', markdown_file_form, False),
        # ("正案例_TOB_emoji", 'app_tob_in', 'nmp_app_tob', markdown_file_emoji, False),
        # ("正案例_TOC卡片消息带title和url", 'app_in', 'nmp_app', fei_shu_card, True),
        # ("正案例_TOB卡片消息带title和url", 'app_tob_in', 'nmp_app_tob', fei_shu_card, True),
    ]
    push_fei_shu_eu_ids = [f"{case[0]}custom_content_tag:{case[-1]}" for case in push_fei_shu_eu_cases]

    @pytest.mark.parametrize(push_fei_shu_eu_keys, push_fei_shu_eu_cases, ids=push_fei_shu_eu_ids)
    def test_push_feishu_eu(self, env, cmdopt, mysql, case_name, host_key, data_key, content, custom_content_tag):
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        title = f"【{cmdopt}】环境，飞书推送time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
        inputs = {
            "host": env['host'][host_key],
            "path": eu_fei_shu_push_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": server_app_id, "sign": ""},
            "json": {
                "recipients": recipients,
                "title": title,
                "content": content,
                # "url": "https://open.feishu.cn/document/ukTMukTMukTM/uADOwUjLwgDM14CM4ATN",
                "custom_content_tag": custom_content_tag
            }
        }
        response = hreq.request(env, inputs)
        assert response['result_code'] == 'success'
        assert response['data']['details'][0]["result"] == 'success'

    push_fei_shu_card_eu_keys = 'case_name,host_key,data_key,content,custom_content_tag'
    push_fei_shu_card_eu_cases = [
        ("正案例_TOC_飞书卡片消息", 'app_in', 'nmp_app', fei_shu_card, True),
        ("正案例_TOB_飞书卡片消息", 'app_tob_in', 'nmp_app_tob', fei_shu_card, True),
    ]
    push_fei_shu_card_eu_ids = [f"{case[0]}custom_content_tag:{case[-1]}" for case in push_fei_shu_card_eu_cases]

    @pytest.mark.parametrize(push_fei_shu_card_eu_keys, push_fei_shu_card_eu_cases, ids=push_fei_shu_card_eu_ids)
    def test_push_fei_shu_card_eu(self, env, cmdopt, mysql, case_name, host_key, data_key, content, custom_content_tag):
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        inputs = {
            "host": env['host'][host_key],
            "path": eu_fei_shu_push_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": server_app_id, "sign": ""},
            "json": {
                "recipients": recipients,
                "content": content,
                "custom_content_tag": custom_content_tag,
            }
        }
        response = hreq.request(env, inputs)
        assert response['result_code'] == 'success'
        assert response['data']['details'][0]["result"] == 'success'
