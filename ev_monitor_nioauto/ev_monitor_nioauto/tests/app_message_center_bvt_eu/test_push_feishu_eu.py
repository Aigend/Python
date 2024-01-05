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
from data.email_content import long_text, html5, markdown_file_title, markdown_file_font, markdown_file_url, markdown_file_img, markdown_file_form, markdown_file_emoji


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
        path = "/api/2/in/message/employee/eu/feishu_push"
        recipients = "qiangwei.zhang@nio.com"
        app_id = 10000
        inputs = {
            "host": env['host']['app_in'],
            "path": path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                "sign": ""
            },
            "json": {
                "recipients": recipients,
                "title": f"【BVT】{cmdopt}飞书time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "content": f"【BVT】【{cmdopt}】环境{path}API，飞书推送测试，如有误收请忽略",
                "url": "https://nio.feishu.cn/docs/doccntRo2MGjg51qDbQ0xgFEh0g"
            }
        }
        response = hreq.request(env, inputs)
        assert response['result_code'] == 'success'
