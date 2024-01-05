#!/usr/bin/env python
# coding=utf-8
from utils.assertions import assert_equal
from utils.time_parse import timestamp_to_utc_strtime


class TestLvBattChargingMsg(object):
    def test_lv_batt_charging_event_mysql(self, vid, checker, publish_msg):
        """
        since BL250，小电池相关数据从特殊事件改为小电池充电事件上报，上报的字段及数据都有不同，原先为rvs处理更新。
        根据can信号中msg_id为850和852的值，解析出mysql状态表status_lv_battery和历史表history_lv_battery中的字段（两表使用方VMS）。
        """
        # 构造并上报消息
        nextev_message, lv_batt_charging_obj = publish_msg('lv_batt_charging_event', can_msg={
            'can_data': [
                {
                    'msg_id': 850,
                    'value': '6800500000'
                },
                {
                    'msg_id': 852,
                    'value': '0000000000000000'
                }
            ]
        })

        # 校验
        tables = ['history_lv_battery', 'status_lv_battery']
        checker.check_mysql_tables(lv_batt_charging_obj, tables)

    def test_dont_record_without_PreCgwLogInfo(self, vid, checker, publish_msg):
        """
        lv_batt_charging_event一秒上报一次
        存储history_lv_battery表时只存储每次唤醒上报的第一条数据，即具有PreCgwLogInfo该字段的那条数据。
        所有的上报都会记录在Cassandra vehicle_data表里，只是mysql里只存每次唤醒的第一条
        """
        # 构造并上报消息
        nextev_message, lv_batt_charging_obj = publish_msg('lv_batt_charging_event', can_msg={
            'can_data': [
                {
                    'msg_id': 850,
                    'value': '6800500000'
                },
                {
                    'msg_id': 852,
                    'value': '0000000000000000'
                }
            ]
        }, clear_fields=['pre_cgw_log_info'])

        # 校验
        tables = ['history_lv_battery']
        sample_time = timestamp_to_utc_strtime(lv_batt_charging_obj['sample_ts'])
        history_lv_battery_in_mysql = checker.mysql.fetch('history_lv_battery',
                                                          {"vehicle_id": vid,
                                                           "sample_time": sample_time},
                                                          retry_num=10)

        assert_equal(len(history_lv_battery_in_mysql), 0)
