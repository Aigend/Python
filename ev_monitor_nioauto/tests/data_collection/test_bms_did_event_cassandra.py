#!/usr/bin/env python
# coding=utf-8


class TestBMSDidMsg(object):
    def test_bms_dids_event_cassandra(self, publish_msg_by_kafka, checker):
        # 构造并上报消息
        nextev_message, bms_dids_event_obj = publish_msg_by_kafka('bms_did_event')

        # 校验
        tables = {'vehicle_data': ['vehicle_id',
                                   'bms_did_info',
                                   'sample_ts']}

        checker.check_cassandra_tables(bms_dids_event_obj, tables, event_name='bms_did_event')

