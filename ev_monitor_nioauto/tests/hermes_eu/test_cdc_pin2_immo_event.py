#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2022/05/10 16:57
@contact: hongzhen.bi@nio.com
"""
import pytest


@pytest.mark.skip("eu")
class TestCdcPin2ImmoEvent(object):

    def test_cdc_pin2_immo_event(self):
        """
        手势密码启动PRD: https://nio.feishu.cn/wiki/wikcnq8slQHFGMHIFgpT0j2Rw6b?hash=91eef6e14f9e87143ee7f86cc481e8ec#
        手势密码功能随账户，被授权人也可设置自己的手势密码，并收到推送消息

        rvs_server 接收车辆上报的特殊事件 cdc_pin2_immo_event，
        当事件内的 event_type 为enable或disable 时推送 80001-push_event kafka

        hermes 消费后查询account接口 /acc/2/in/profile/query 获取邮箱和语言，并根据 event_type 选择文案
        最终调用消息平台接口 /api/2/in/message/eu/email_direct_push 推送email

        注：hermes只根据消息里的account_id推送，不判断是否确为被授权人或车主
        """
        pass