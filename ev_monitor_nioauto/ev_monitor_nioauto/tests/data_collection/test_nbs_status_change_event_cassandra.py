#!/usr/bin/env python
# coding=utf-8


class TestNBSStatusChangeMsg(object):
    def test_nbs_status_change_event_cassandra(self, publish_msg_by_kafka, checker):
        # 构造并上报消息
        nextev_message, nbs_status_change_event_obj = publish_msg_by_kafka('nbs_status_change_event')

        # 校验
        tables = {'vehicle_data': ['vehicle_id',
                                   'nbs_status',
                                   'sample_ts']}

        checker.check_cassandra_tables(nbs_status_change_event_obj, tables, event_name='nbs_status_change_event')

