#!/usr/bin/env python
# coding=utf-8


class TestLvBattChargingMsg(object):
    def test_lv_batt_charging_event_cassandra(self, publish_msg_by_kafka, checker):
        # 构造并上报消息
        nextev_message, lv_batt_charging_event_obj = publish_msg_by_kafka('lv_batt_charging_event')

        # 校验
        tables = {'vehicle_data': ['vehicle_id',
                                   'lv_batt_charging_status',
                                   'can_msg',
                                   'vehicle_status',
                                   'sample_ts']}

        lv_batt_charging_event_obj['can_msg'].pop('can_news')
        checker.check_cassandra_tables(lv_batt_charging_event_obj, tables, event_name='lv_batt_charging_event')

