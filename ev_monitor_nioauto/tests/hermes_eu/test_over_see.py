#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2022/04/08 10:58
@contact: hongzhen.bi@nio.com
@description: 脚本描述【必填】
"""
import pytest

"""
ABSSignalProcessor 中消费can_signal做限制 can_signal.removable=false
ConnStatusProcessor 中消费status_client做限制 cgw.client.removable=false
DataReportPeriodicalProcessor 中消费evm_periodical_topic做限制 cgw.client.removable=false
DataReportProcessor 中消费data_report做限制 evm_topic.removable=false
ECallEventProcessor 中消费ecall topic做限制 ecall.removable=false
FodEventProcessor 中消费fod topic做限制 fod.removable=false
PushEventProcessor 中消费push_event做限制 push.event.removable=false
WtiAlarmProcessor 中消费wti_alarm做限制 wti_topic.removable=false

车辆状态推送开关配置 app.vehl_status.push.switch=true
WTI告警和ecall告警推送开关配置 user.notify.sync.switch=true
月旅程报告推送开关配置 app.journey.push.switc=false
"""


@pytest.mark.skip("eu")
class TestPushEvent(object):
    def test_push_event(self):
        pass