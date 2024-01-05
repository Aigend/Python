#!/usr/bin/env python
# coding=utf-8


class TestHeatingStatusChangeMsg(object):
    def test_heating_status_change_event_cassandra(self, publish_msg_by_kafka, checker):
        # 构造并上报消息
        nextev_message, heating_status_change_event_obj = publish_msg_by_kafka('heating_status_change_event')

        # 校验
        tables = {'vehicle_data': ['vehicle_id',
                                   'heating_status',
                                   'sample_ts']}

        checker.check_cassandra_tables(heating_status_change_event_obj, tables, event_name='heating_status_change_event')

