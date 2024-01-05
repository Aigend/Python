#!/usr/bin/env python
# coding=utf-8

"""
:file: test_light_change_event_cassandra.py
:author: chunming.liu
:Date: Created on 2019/1/12
:Description: 电灯变化事件，包含电灯状态数据
"""


class TestLightChangeMsg(object):
    def test_light_change_event(self, publish_msg, checker):
        # 构造并上报消息
        nextev_message, light_change_obj = publish_msg('light_change_event')

        # 校验
        tables ={'vehicle_data':['vehicle_id',
                                 'light_status',
                                 'sample_ts']
                 }
        checker.check_cassandra_tables(light_change_obj, tables, event_name='light_change_event')
