#!/usr/bin/env python
# coding=utf-8


import allure

from utils.assertions import assert_equal


class TestAlarmSignalMsg(object):
    def test_alarm_signal_update(self, publish_msg, checker):
        with allure.step("校验 alarm_signal_update 事件不更新所有状态表"):

            tables = ['status_position', 'status_vehicle', 'status_soc',
                      'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre']

            data_mysql_old = checker.get_mysql_status_tables(tables)

            nextev_message, alarm_signal_update = publish_msg('alarm_signal_update_event')

            data_mysql_new = checker.get_mysql_status_tables(tables)

            assert_equal(data_mysql_old, data_mysql_new)

