#!/usr/bin/env python
# coding=utf-8

"""
:file: test_journey_end_event_cassandra.py
:author: chunming.liu
:Date: Created on 2019/1/11
:Description: 行程开始事件，包含position数据。
"""


class TestJourneyEndMsg(object):
    def test_journey_end_event(self, publish_msg, checker):
        # 构造并上报消息
        nextev_message, journey_end_obj = publish_msg('journey_end_event')

        # 校验
        tables ={'vehicle_data':['vehicle_id',
                                 'soc_status',
                                 'position_status',
                                 'vehicle_status',
                                 'process_id as journey_id',
                                 'sample_ts']
                 }
        checker.check_cassandra_tables(journey_end_obj, tables, event_name='journey_end_event')

