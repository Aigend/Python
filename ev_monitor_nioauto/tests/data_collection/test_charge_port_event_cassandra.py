#!/usr/bin/env python
# coding=utf-8

"""
:file: test_charge_port_event_cassandra.py
:author: zhiqiang.zhu
:Date: Created on 2017/1/12 下午7:12
:Description: 充电口事件上报存到Cassandra的vehicle_data的door_status字段
"""


class TestChargePortChangeMsg(object):
    def test_charge_port_event_cassandra(self, publish_msg, checker):
        # 构造并上报消息
        nextev_message, charge_port_obj = publish_msg('charge_port_event')

        # 校验
        tables ={'vehicle_data':['vehicle_id',
                                 'door_status',
                                 'sample_ts']
                 }
        checker.check_cassandra_tables(charge_port_obj, tables, event_name='charge_port_event')

