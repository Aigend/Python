#!/usr/bin/env python
# coding=utf-8

"""
:file: test_window_change_event_cassandra.py
:author: chunming.liu
:Date: Created on 2019/1/12 下午7:57
:Description: 车窗事件消息上报，包含车窗状态数据
"""


class TestWindowChangeMsg(object):
    def test_window_change_event_cassandra(self, publish_msg, checker):
        # 构造并上报消息
        nextev_message, window_change_event_obj = publish_msg('window_change_event')

        # 校验
        tables ={'vehicle_data':['vehicle_id',
                                 'window_status',
                                 'sample_ts']
                 }
        checker.check_cassandra_tables(window_change_event_obj, tables, event_name='window_change_event')

