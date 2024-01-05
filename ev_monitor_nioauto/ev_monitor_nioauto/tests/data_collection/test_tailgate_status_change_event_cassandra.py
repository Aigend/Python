#!/usr/bin/env python
# coding=utf-8

"""
:file: test_tailgate_status_change_event_cassandra.py
:author: chunming.liu
:Date: Created on 2019/1/12 下午7:12
:Description: 后备箱状态变更事件存储到Cassandra的vehicle_data的door_status字段
"""


class TestTailgateChangeMsg(object):
    def test_tailgate_status_change_event_cassandra(self, publish_msg, checker):
        # 构造并上报消息
        nextev_message, tailgate_status_change_event_obj = publish_msg('tailgate_status_change_event')

        # 校验
        tables ={'vehicle_data':['vehicle_id',
                                 'door_status',
                                 'sample_ts']
                 }
        checker.check_cassandra_tables(tailgate_status_change_event_obj, tables, event_name='tailgate_status_change_event')

