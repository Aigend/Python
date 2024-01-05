#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2022/04/08 17:22
@contact: hongzhen.bi@nio.com
@description: 脚本描述【必填】
"""
import pytest

"""
推送以下消息给APP:
    rain_wrm_event
    svt_event
    command_event (rvs_fota_trigger)
    
rvs_server转发special_event上报的rain_wrm_event和svt_event事件数据到kafka
swc-cvs-tsp-test-80001-push_event (http://showdoc.nevint.com/index.php?s=/11&page_id=24395 )

1.rain_wrm_event
    hermes监测到RainDetected之后，判断窗户和天窗状态，如果未关闭，向用户推送
    prd:https://confluence.nioint.com/pages/viewpage.action?pageId=276272698 
2.command_event
    该事件为APP下发fota/trigger后车机返回的command_result，vehicle_control消费后
    推送push_event kafka，hermes消费后推送APP。
    文案语言选择: 
        redis: hermes_test:user_lan:1003078433
        redis不存在查account接口 /acc/2/in/profile/query 并将结果写入
"""


@pytest.mark.skip("manual")
class TestPushEvent(object):
    def test_push_event(self):
        pass
