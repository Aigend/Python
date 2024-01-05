#!/usr/bin/env python
# coding=utf-8

"""
:file: test_door_change_event_cassandra.py
:author: chunming.liu
:Date: Created on 2019/1/12 下午7:12
:Description: 车门状态变更事件存到Cassandra的vehicle_data的door_status字段
"""


class TestDoorStatusChangeMsg(object):
    def test_door_status_change_event_cassandra(self, publish_msg, checker):
        # 构造并上报消息
        nextev_message, door_status_obj = publish_msg('door_change_event')

        # 校验
        tables ={'vehicle_data':['vehicle_id',
                                 'door_status',
                                 'sample_ts']
                 }
        checker.check_cassandra_tables(door_status_obj, tables, event_name='door_change_event')
