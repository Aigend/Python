# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_push_feishu_cn.py
# @Author : qiangwei.zhang.o
# @CreateTime : 2021/4/23 4:06 下午
# @Description :

import time

import allure
import pytest
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from data.email_content import markdown_file_img
from utils.collection_message_states import collection_message_states

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


def test_push_feishu_cn(env, cmdopt):
    with allure.step(f"员工发送邮件接口"):
        inputs = {
            "host": env['host']['app_in'],
            "path": "/api/2/in/message/employee/cn/feishu_push",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {"region": "cn", "lang": "zh-cn", "hash_type": "sha256", "app_id": 10000, "sign": ""},
            "json": {
                "recipients": "qiangwei.zhang@nio.com",
                "title": f"【BVT】【{cmdopt}】环境，飞书推送time:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                "content": markdown_file_img,
                "url": "https://open.feishu.cn/document/ukTMukTMukTM/uADOwUjLwgDM14CM4ATN"
            }
        }
        response = hreq.request(env, inputs)
    with allure.step("员工发送邮件接口,校验result_code"):
        assert response['result_code'] == 'success'
