#!/usr/bin/env python
# coding=utf-8

"""
:file: test_engine_hood_status_change_event_cassandra.py
:author: chunming.liu
:Date: Created on 2019/1/12 下午7:12
:Description: 发动机罩变更事件存储到Cassandra的vehicle_data的door_status字段
"""


class TestEngineHoodChangeMsg(object):
    def test_engine_hood_status_change_event(self, publish_msg, checker):
        # 构造并上报消息
        nextev_message, engine_hood_status_change_obj = publish_msg('engine_hood_status_change_event')

        # 校验
        tables ={'vehicle_data':['vehicle_id',
                                 'door_status',
                                 'sample_ts']
                 }
        checker.check_cassandra_tables(engine_hood_status_change_obj, tables, event_name='engine_hood_status_change_event')

