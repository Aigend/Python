#!/usr/bin/env python
# coding=utf-8

"""
:file: test_driving_behaviour_event_mysql.py
:author: zhiqiang.zhu
:Date: Created on 2017/1/12 下午7:17
:Description: 驾驶行为事件上报，包含驾驶行为数据。
"""
import pytest


@pytest.mark.skip("status_driving_behv表已停止更新")
class TestDrivingBehaviourMsg(object):
    def test_driving_behaviour_event(self, checker, publish_msg):
        # 构造并上报消息
        nextev_message, driving_behaviour_obj = publish_msg('driving_behaviour_event')

        # 校验
        tables = ['status_driving_behv']
        checker.check_mysql_tables(driving_behaviour_obj, tables)



