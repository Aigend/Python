#!/usr/bin/env python
# coding=utf-8

"""
:file: test_driving_behaviour_event_cassandra.py
:author: zhiqiang.zhu
:Date: Created on 2017/1/12 下午7:17
:Description: 驾驶行为事件上报，包含驾驶行为数据。
"""


class TestDrivingBehaviourMsg(object):
    def test_driving_behaviour_event(self, publish_msg, checker):
        # 构造并上报消息
        nextev_message, driving_behaviour_obj = publish_msg('driving_behaviour_event')

        # 校验
        tables ={'vehicle_data':['vehicle_id',
                                 'driving_behaviour',
                                 'sample_ts']
                 }
        checker.check_cassandra_tables(driving_behaviour_obj, tables, event_name='driving_behaviour_event')
