#!/usr/bin/env python
# coding=utf-8
"""
https://confluence.nevint.com/display/CVS/Specific+Events+Report
"""
import ast
import json
import random

import allure
import pytest

from utils.assertions import assert_equal
from utils.time_parse import timestamp_to_utc_strtime


class TestSpecificEventMsg(object):
    def test_lv_batt_charging(self, publish_msg, checker):
        """
        For VMS
        BL260以后改用lv_batt_charging_event上报，sample_week和sample_month用于VMS筛选用，但目前已经弃用
        """
        # 上报
        nextev_message, obj = publish_msg('specific_event', event_type='lv_batt_charging', sleep_time=3)

        # # 校验
        tables = ['status_lv_battery', 'history_lv_battery']
        checker.check_mysql_tables(obj, tables)

    def test_nfc_op(self, publish_msg, checker):
        """
        若未上报ts_read_key字段，则数据库表对应read key time值为 1970-01-01
        若未上报ts_veri_key字段，则数据库表对应veri key time值为 1970-01-01
        若上报的字段为cert_serial_number 或 serial_number，则数据库表往serial_number字段存值
        """
        # 上报
        nextev_message, obj = publish_msg('specific_event', event_type='nfc_op')

        # # 校验
        tables = ['history_nfc_op']
        checker.check_mysql_tables(obj, tables)

    def test_fod_conf(self, vid, publish_msg, checker):
        # 上报
        nextev_message, fod_conf_in_message = publish_msg('specific_event', event_type='fod_conf')

        # 校验
        fod_conf_in_mysql = checker.mysql.fetch('history_specific_event',
                                                {"vehicle_id": vid,
                                                 "event_type": "fod_conf",
                                                 "sample_time": timestamp_to_utc_strtime(fod_conf_in_message['sample_ts'])},
                                                fields=['event_data'])[0]
        assert_equal(fod_conf_in_message, ast.literal_eval(fod_conf_in_mysql['event_data']))

    def test_max_charging_soc_event(self, redis_key_front, vid, publish_msg, checker):
        with allure.step("校验处理max soc specific event事件时，不再拦截历史时间戳"):
            """有变更就会上报，上报一次"""
            # 消息上报
            nextev_message, obj = publish_msg('specific_event', event_type='max_charging_soc_event')

            with allure.step("校验max_charging_soc_event事件存入MySQL的history_specific_event"):
                max_soc_event_in_mysql = checker.mysql.fetch('history_specific_event',
                                                             {"vehicle_id": vid,
                                                              "event_type": "max_charging_soc_event",
                                                              "sample_time": timestamp_to_utc_strtime(obj['sample_ts'])},
                                                             fields=['event_data'])[0]
                assert_equal(obj, ast.literal_eval(max_soc_event_in_mysql['event_data']))

            with allure.step("校验current_max_soc_value存入MySQL的状态表status_soc"):
                # set_max_soc_value字段没用，所以只校验current_max_soc_value
                max_soc_in_mysql = checker.mysql.fetch('status_soc', {'id': vid})[0]
                assert_equal(max_soc_in_mysql['max_soc'], obj['current_max_soc_value'])

            with allure.step("校验current_max_soc_value存入Redis"):
                remote_vehicle_key_front = redis_key_front['remote_vehicle']
                key = remote_vehicle_key_front + ':vehicle_status:' + vid + ':SocStatus'
                status_soc_in_redis = json.loads(checker.redis.get(key))
                assert_equal(status_soc_in_redis['max_soc'], obj['current_max_soc_value'])

            # 为了不影响其他case，校验之后要把max_soc变回100
            publish_msg('specific_event', event_type='max_charging_soc_event', data={'current_max_soc_value': 100})

    def test_swapping_in_redis(self, redis_key_front, vid, publish_msg, checker):
        with allure.step("校验当换电事件时，SpecialStatus会记录swapping 1/0=开始/结束，以及换电事件事件。连续相同的事件不会重复记录"):
            # 上报power_swap_start事件，并校验redis中的swapping字段置为1
            publish_msg('specific_event', event_type='power_swap_start')
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key = remote_vehicle_key_front + ':vehicle_status:' + vid + ':SpecialStatus'
            swapping_in_redis = json.loads(checker.redis.get(key))
            assert_equal(swapping_in_redis['swapping'], 1)

            # 上报power_swap_end或power_swap_failure事件，并校验redis中的swapping字段置为0
            publish_msg('specific_event', event_type=random.choice(['power_swap_end', 'power_swap_failure']))
            swapping_in_redis = json.loads(checker.redis.get(key))
            assert_equal(swapping_in_redis['swapping'], 0)

    def test_hv_battery_pre_heating(self, vid, publish_msg, checker):
        # 上报
        nextev_message, hv_battery_pre_heating_in_message = publish_msg('specific_event', event_type='hv_battery_pre_heating')

        # 校验
        hv_battery_pre_heating_in_mysql = checker.mysql.fetch('history_specific_event',
                                                              {"vehicle_id": vid,
                                                               "event_type": "hv_battery_pre_heating",
                                                               "sample_time": timestamp_to_utc_strtime(hv_battery_pre_heating_in_message['sample_ts'])},
                                                              fields=['event_data'])[0]
        assert_equal(hv_battery_pre_heating_in_message, ast.literal_eval(hv_battery_pre_heating_in_mysql['event_data']))

    def test_gd_alert_can_rate(self, vid, publish_msg, checker):
        # 上报
        nextev_message, gd_alert_can_rate_in_message = publish_msg('specific_event', event_type='gd_alert_can_rate')

        # 校验
        gd_alert_can_rate_in_mysql = checker.mysql.fetch('history_specific_event',
                                                         {"vehicle_id": vid,
                                                          "event_type": "gd_alert_can_rate",
                                                          "sample_time": timestamp_to_utc_strtime(gd_alert_can_rate_in_message['sample_ts'])},
                                                         fields=['event_data'])[0]
        assert_equal(gd_alert_can_rate_in_message, ast.literal_eval(gd_alert_can_rate_in_mysql['event_data']))

    def test_deep_sleep(self, vid, publish_msg, checker):
        # 上报
        nextev_message, deep_sleep_in_message = publish_msg('specific_event', event_type='deep_sleep')

        # 校验
        deep_sleep_in_mysql = checker.mysql.fetch('history_specific_event',
                                                  {"vehicle_id": vid,
                                                   "event_type": "deep_sleep",
                                                   "sample_time": timestamp_to_utc_strtime(deep_sleep_in_message['sample_ts'])},
                                                  fields=['event_data'])[0]
        assert_equal(deep_sleep_in_message, ast.literal_eval(deep_sleep_in_mysql['event_data']))

    def test_toby_event(self, vid, publish_msg, checker):
        # 上报
        event_type = "toby_event"
        nextev_message, toby_event_in_message = publish_msg('specific_event', event_type=event_type)

        # 校验
        toby_event_in_mysql = checker.mysql.fetch('history_specific_event',
                                                  {"vehicle_id": vid,
                                                   "event_type": event_type,
                                                   "sample_time": timestamp_to_utc_strtime(toby_event_in_message['sample_ts'])},
                                                  fields=['event_data'])[0]
        assert_equal(toby_event_in_message, ast.literal_eval(toby_event_in_mysql['event_data']))

    def test_fota_trigger_event(self, vid, publish_msg, checker):
        # 上报
        nextev_message, fota_trigger_event_in_message = publish_msg('specific_event', event_type='fota_trigger_event')

        # 校验
        fota_trigger_event_in_mysql = checker.mysql.fetch('history_specific_event',
                                                          {"vehicle_id": vid,
                                                           "event_type": "fota_trigger_event",
                                                           "sample_time": timestamp_to_utc_strtime(fota_trigger_event_in_message['sample_ts'])},
                                                          fields=['event_data'])[0]
        assert_equal(fota_trigger_event_in_message, ast.literal_eval(fota_trigger_event_in_mysql['event_data']))

    def test_fota_state_notify(self, vid, publish_msg, checker):
        # 上报
        nextev_message, fota_state_notify_in_message = publish_msg('specific_event', event_type='fota_state_notify')

        # 校验
        fota_state_notify_in_mysql = checker.mysql.fetch('history_specific_event',
                                                         {"vehicle_id": vid,
                                                          "event_type": "fota_state_notify",
                                                          "sample_time": timestamp_to_utc_strtime(fota_state_notify_in_message['sample_ts'])},
                                                         fields=['event_data'])[0]
        assert_equal(fota_state_notify_in_message, ast.literal_eval(fota_state_notify_in_mysql['event_data']))

    def test_bms_dtc_info(self, vid, publish_msg, checker):
        # 上报
        nextev_message, bms_dtc_info_in_message = publish_msg('specific_event', event_type='bms_dtc_info')

        # 校验
        bms_dtc_info_in_mysql = checker.mysql.fetch('history_specific_event',
                                                    {"vehicle_id": vid,
                                                     "event_type": "bms_dtc_info",
                                                     "sample_time": timestamp_to_utc_strtime(bms_dtc_info_in_message['sample_ts'])},
                                                    fields=['event_data'])[0]
        assert_equal(bms_dtc_info_in_message, ast.literal_eval(bms_dtc_info_in_mysql['event_data']))

    def test_modem_event(self, vid, publish_msg, checker):
        # 上报
        nextev_message, modem_event_in_message = publish_msg('specific_event', event_type='modem_event')

        # 校验
        checker.check_mysql_tables(modem_event_in_message, ['history_modem_event'])

    def test_ble_op_event(self, vid, publish_msg, checker):
        # 上报
        nextev_message, ble_op_event_in_message = publish_msg('specific_event', event_type='ble_op_event')

        with allure.step('校验mysql history_ble_op'):
            checker.check_mysql_tables(ble_op_event_in_message, ['history_ble_op'])

    def test_car_key_settings_event(self, vid, publish_msg, checker):
        # 上报
        nextev_message, car_key_settings_event_in_message = publish_msg('specific_event', event_type='car_key_settings_event')

        with allure.step("校验mysql history_specific_event"):
            car_key_settings_in_mysql = checker.mysql.fetch('history_specific_event',
                                                            {"vehicle_id": vid,
                                                             "event_type": "car_key_settings_event",
                                                             "sample_time": timestamp_to_utc_strtime(car_key_settings_event_in_message['sample_ts'])},
                                                            fields=['event_data'])[0]
            assert_equal(car_key_settings_event_in_message, ast.literal_eval(car_key_settings_in_mysql['event_data']))

        with allure.step('校验mysql status_car_key'):
            checker.check_mysql_tables(car_key_settings_event_in_message, ['status_car_key'])

