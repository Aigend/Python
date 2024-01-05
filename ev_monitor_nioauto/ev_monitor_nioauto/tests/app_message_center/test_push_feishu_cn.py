# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_push_feishu_cn.py
# @Author : qiangwei.zhang.o
# @CreateTime : 2021/4/23 4:06 下午
# @Description :
"""
    1）推送飞书接口
        接口文档 http://showdoc.nevint.com/index.php?s=/647&page_id=30577
        api: /api/2/in/message/employee/cn/feishu_push
        接口文档 http://showdoc.nevint.com/index.php?s=/647&page_id=30576
        api: /api/2/in/message/employee/eu/feishu_push
        入库校验：数据库不记录

        字段说明：
            * recipients: 收件人
                * 限制数量100
                * 飞书企业账号（正常为邮箱账号）
            * title: 主题{不支持变量名称，接口不限制长度}
            * content: 内容{不支持变量名称，接口不限制长度}
                * 文本
                * 不支持html
                * markdown
                    标题
                    字体
                    链接
                    表格
                    图片
                        正常解析的key
                            图片类型
                                JPG
                                JPEG
                                PNG
                                BMP
                                WEBP
                                GIF
                        多个图片
                        错误的key
    emoji
            * url: 跳转链接，非必填
            topic: swc-cvs-nmp-cn-test-push-feishu
            topic: swc-cvs-nmp-cn-stg-push-feishu
            """
from utils.assertions import assert_equal
from utils.random_tool import random_string

"""
测试场景：
    1.recipients用户重复/重复用户会收到多条消息
    2.recipients用户超过100个/最多100
    3.recipients用户1个
    4.recipients不存在/接口返回成功
    5.recipients部分不存在/接口返回成功,存在的能收到
    6.recipients为空/接口报错
    7.recipients不传/接口报错
    8.title，content字符串,暂无长度限制/
    9.title，content为空/接口报错
    10.title，content不传/接口报错
    11.url不传/接口成功，可收到消息
    12.url传正常可解析值/接口成功，可收到消息，点击消息可跳转到链接
    13.url传符合url格式，无法解析的值/接口成功，可收到消息，点击消息可跳转到无法解析的链接
    14.url传不符合url格式的值/接口返回失败
"""

import time
import pytest
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from data.email_content import markdown_file_title, markdown_file_font, markdown_file_url, markdown_file_img, markdown_file_form, markdown_file_emoji, fei_shu_card, fei_shu_card1
from utils.collection_message_states import collection_message_states

allow_environment = ['test', 'stg', "test_alps"]


@pytest.mark.run(order=2)
class TestPushFeiShuCN(object):
    push_fei_shu_cn_keys = 'case_name,host_key, data_key, content,custom_content_tag'
    push_fei_shu_cn_cases = [
        # ("正案例_TOC_文件标题", 'app_in', 'nmp_app', markdown_file_title, False),
        ("正案例_TOC_字体", 'app_in', 'nmp_app', markdown_file_font, False),
        # ("正案例_TOC_URL", 'app_in', 'nmp_app', markdown_file_url, False),
        ("正案例_TOC_图片", 'app_in', 'nmp_app', markdown_file_img, False),
        # ("正案例_TOC_表格", 'app_in', 'nmp_app', markdown_file_form, False),
        # ("正案例_TOC_emoji", 'app_in', 'nmp_app', markdown_file_emoji, False),
        # ("正案例_TOC_卡片消息带title和url", 'app_in', 'nmp_app', fei_shu_card, True),
        # ("正案例_TOC_emoji", 'app_in', 'nmp_app', fei_shu_card, False),
        ("正案例_TOB_图片", 'app_tob_in', 'nmp_app_tob', markdown_file_img, False),
        # ("正案例_TOB_表格", 'app_tob_in', 'nmp_app_tob', markdown_file_form, False),
        ("正案例_TOB_emoji", 'app_tob_in', 'nmp_app_tob', markdown_file_emoji, False),
    ]
    push_fei_shu_cn_ids = [f"{case[0]}" for case in push_fei_shu_cn_cases]

    @pytest.mark.parametrize(push_fei_shu_cn_keys, push_fei_shu_cn_cases, ids=push_fei_shu_cn_ids)
    def test_push_feishu_cn(self, env, cmdopt, mysql, case_name, host_key, data_key, content, custom_content_tag):
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        path = "/api/2/in/message/employee/cn/feishu_push"
        recipients = "qiangwei.zhang@nio.com"
        app_id = 10000
        title = f"【{cmdopt}】{host_key}环境，custom_content_tag:{custom_content_tag}飞书推送time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
        inputs = {
            "host": env['host'][host_key],
            "path": path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": {
                "recipients": recipients,
                "title": title,
                "content": content,
                "url": "https://open.feishu.cn/document/ukTMukTMukTM/uADOwUjLwgDM14CM4ATN",
                "custom_content_tag": custom_content_tag
            }
        }
        response = hreq.request(env, inputs)
        assert response['result_code'] == 'success'
        assert response['data']['details'][0]["result"] == 'success'

    push_fei_shu_card_cn_keys = 'case_name,host_key, data_key, content,custom_content_tag'
    push_fei_shu_card_cn_cases = [
        ("正案例_TOC_飞书卡片消息", 'app_in', 'nmp_app', fei_shu_card, True),
        ("正案例_TOB_飞书卡片消息", 'app_tob_in', 'nmp_app_tob', fei_shu_card, True),
    ]
    push_fei_shu_card_cn_ids = [f"{case[0]}" for case in push_fei_shu_card_cn_cases]

    @pytest.mark.parametrize(push_fei_shu_card_cn_keys, push_fei_shu_card_cn_cases, ids=push_fei_shu_card_cn_ids)
    def test_push_fei_shu_card_cn(self, env, cmdopt, mysql, case_name, host_key, data_key, content, custom_content_tag):
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        path = "/api/2/in/message/employee/cn/feishu_push"
        recipients = "qiangwei.zhang@nio.com"
        app_id = 10000
        inputs = {
            "host": env['host'][host_key],
            "path": path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": {
                "recipients": recipients,
                "content": content,
                "custom_content_tag": custom_content_tag
            }
        }
        response = hreq.request(env, inputs)
        assert response['result_code'] == 'success'
        assert response['data']['details'][0]["result"] == 'success'

    recipients_105 = ",".join([random_string(12) for i in range(105)])
    push_fei_shu_batch_cn_keys = 'case_name,host_key, data_key, content,custom_content_tag,recipients'
    push_fei_shu_batch_cn_cases = [
        # ("反案例_TOC_超过100个收件人", 'app_in', 'nmp_app', fei_shu_card, True, recipients_105),
        ("正案例_TOC_飞书卡片消息", 'app_in', 'nmp_app', fei_shu_card, True, "qiangwei.zhang@nio.com,colin.li@nio.com"),
        ("正案例_TOB_飞书卡片消息", 'app_tob_in', 'nmp_app_tob', fei_shu_card1, True, "qiangwei.zhang@nio.com,colin.li@nio.com"),
    ]
    push_fei_shu_batch_cn_ids = [f"{case[0]}" for case in push_fei_shu_batch_cn_cases]

    @pytest.mark.parametrize(push_fei_shu_batch_cn_keys, push_fei_shu_batch_cn_cases, ids=push_fei_shu_batch_cn_ids)
    def test_push_fei_shu_batch_cn(self, env, cmdopt, mysql, case_name, host_key, data_key, content, custom_content_tag, recipients):
        if cmdopt not in allow_environment:
            logger.debug(f"该案例允许执行的环境为{allow_environment};不在【{cmdopt}】环境执行")
            return 0
        path = "/api/2/in/message/employee/cn/feishu_push"
        app_id = 10000
        inputs = {
            "host": env['host'][host_key],
            "path": path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": app_id, "sign": ""},
            "json": {
                "recipients": recipients,
                "content": content,
                "custom_content_tag": custom_content_tag
            }
        }
        response = hreq.request(env, inputs)
        if "正案例" in case_name:
            assert response['result_code'] == 'success'
            assert response['data']['details'][0]["result"] == 'success'
        else:
            response.pop("request_id")
            response.pop("server_time")
            expect_res = {
                "result_code": "invalid_param",
                "debug_msg": "exceed limit, max receiver is 100"
            }

            assert_equal(expect_res,response)
