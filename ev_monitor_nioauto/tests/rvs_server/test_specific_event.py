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

    def test_nfc_op_no_action(self, publish_msg, checker):
        """
        test_nfc_op所属的一种特殊case，如果上报的事件中没有传action值，会根据extend_info的值来补充
        """
        # 上报
        nextev_message, obj = publish_msg('specific_event', event_type='nfc_op', data={'status': 'success'}, clear_fields={'action'})

        # # 校验
        if obj['extend_info'] == 'SuccessUnlockDoors':
            obj['action'] = "unlock_door"
        else:
            obj['action'] = "lock_doors"
        tables = ['history_nfc_op']
        checker.check_mysql_tables(obj, tables)

    def test_nfc_op_null_action(self, publish_msg, checker):
        """
        test_nfc_op所属的一种特殊case，如果上报的事件中action值为空，会根据extend_info的值来补充
        """
        # 上报
        nextev_message, obj = publish_msg('specific_event', event_type='nfc_op', data={'action': '', 'status': 'success'})

        # # 校验
        if obj['extend_info'] == 'SuccessUnlockDoors':
            obj['action'] = "unlock_door"
        else:
            obj['action'] = "lock_doors"
        tables = ['history_nfc_op']
        checker.check_mysql_tables(obj, tables)

    def test_power_home_auth_failure(self, vid, publish_msg, checker):
        # 上报
        nextev_message, power_home_auth_failure_in_message = publish_msg('specific_event',
                                                                                  event_type='power_home_auth_failure',
                                                                                  sleep_time=3)

        # 校验
        power_home_auth_failure_in_mysql = checker.mysql.fetch('history_specific_event',
                                                               {"vehicle_id": vid,
                                                                "event_type": "power_home_auth_failure",
                                                                "sample_time": timestamp_to_utc_strtime(
                                                                    power_home_auth_failure_in_message['sample_ts'])},
                                                               fields=['event_data'])[0]
        assert_equal(power_home_auth_failure_in_message,
                     ast.literal_eval(power_home_auth_failure_in_mysql['event_data']))

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
            key = remote_vehicle_key_front+ ':vehicle_status:' + vid + ':SpecialStatus'
            swapping_in_redis = json.loads(checker.redis.get(key))
            assert_equal(swapping_in_redis['swapping'], 1)

            # 上报power_swap_end或power_swap_failure事件，并校验redis中的swapping字段置为0
            publish_msg('specific_event', event_type=random.choice(['power_swap_end', 'power_swap_failure']))
            swapping_in_redis = json.loads(checker.redis.get(key))
            assert_equal(swapping_in_redis['swapping'], 0)

    # TODO 马克波罗服务暂不支持，先跳过
    @pytest.mark.marcopolo_skip
    def test_ac_plan_exec(self, vid, publish_msg, checker):
        """
        空调预约启动事件
        如果预约启动失败，RVS Server调用APP Msg（APP中台）接口api/1/in/app_msg/common 往APP push 信息。详情见test_ac_plan_exec.py
        """

        # 上报
        nextev_message, ac_plan_exec_in_message = publish_msg('specific_event', event_type='ac_plan_exec')

        # 校验
        ac_plan_exec_in_mysql = checker.mysql.fetch('history_specific_event',
                                                    {"vehicle_id": vid,
                                                     "event_type": "ac_plan_exec",
                                                     "sample_time": timestamp_to_utc_strtime(ac_plan_exec_in_message['sample_ts'])},
                                                    fields=['event_data'])[0]
        assert_equal(ac_plan_exec_in_message, ast.literal_eval(ac_plan_exec_in_mysql['event_data']))

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

    @pytest.mark.parametrize("status", ['success', 'failure'])
    def test_toby_upgrade_event(self, vid, publish_msg, checker, status):
        # 上报
        event_type = "toby_event"
        nextev_message, toby_event_in_message = publish_msg('specific_event', event_type=event_type,
                                                                     data={'event_type': 'toby_upgrade',
                                                                           'event_detail': {'imei': str(random.randint(0, 10000)),
                                                                                            'upgrade_status': status,
                                                                                            'current_version': 'test_toby.'+str(random.randint(0, 1000))}})

        # 校验
        toby_event_in_mysql = checker.mysql.fetch('history_specific_event',
                                                  {"vehicle_id": vid,
                                                   "event_type": event_type,
                                                   "sample_time": timestamp_to_utc_strtime(toby_event_in_message['sample_ts'])},
                                                  fields=['event_data'])[0]
        assert_equal(toby_event_in_message, ast.literal_eval(toby_event_in_mysql['event_data']))

        # 检验是否将toby版本存到vehicle_soft_config表
        toby_version = checker.mysql.fetch_one('vehicle_soft_config',
                                               {"vehicle_id": vid,
                                                "sample_time": timestamp_to_utc_strtime(
                                                    toby_event_in_message['sample_ts'])})
        if status == 'success':
            assert toby_version['value'] == toby_event_in_message['event_detail']['current_version']
        else:
            assert not toby_version

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


    # TODO 马克波罗服务暂不支持，先跳过
    @pytest.mark.marcopolo_skip
    def test_rain_wrm_event(self, vid, publish_msg, checker, kafka):
        """
        rvs_server转发special event上报的rain_wrm_event事件数据到kafka
        swc-cvs-tsp-test-80001-push_event (http://showdoc.nevint.com/index.php?s=/11&page_id=24395 )

        hermes监测到RainDetected之后，判断窗户和天窗状态，如果未关闭，向用户推送
        prd:https://confluence.nioint.com/pages/viewpage.action?pageId=276272698 
        """
        # 重置offset
        kafka['cvs'].set_offset_to_end(kafka['topics']['push_event'])
        # 上报
        nextev_message, rain_wrm_event_in_message = publish_msg('specific_event', event_type='rain_wrm_event')

        with allure.step('校验kafka {}'.format(kafka['topics']['push_event'])):
            is_found = False
            for data in kafka['cvs'].consume(kafka['topics']['push_event'], timeout=10):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if kafka_msg['data']['sample_ts'] == rain_wrm_event_in_message['sample_ts'] and vid == kafka_msg['vehicle_id']:
                    is_found = True
                    break
            assert_equal(True, is_found)
            assert_equal(kafka_msg['data'], rain_wrm_event_in_message)

        with allure.step('校验mysql'):
            rain_wrm_event_in_mysql = checker.mysql.fetch('history_specific_event',
                                                          {"vehicle_id": vid,
                                                           "event_type": "rain_wrm_event",
                                                           "sample_time": timestamp_to_utc_strtime(rain_wrm_event_in_message['sample_ts'])},
                                                          fields=['event_data'])[0]
            assert_equal(rain_wrm_event_in_message, ast.literal_eval(rain_wrm_event_in_mysql['event_data']))

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
        """
        由于以下失败原因数据量过多，对其做了过滤
        Connection timed out, Function not implemented, enable_notify_timeout, Connection reset by peer
        NT1 BLE时间上报情况：https://nio.feishu.cn/docs/doccnHHqENzZgJVILr52Tbvij8b
        """
        # 上报
        nextev_message, ble_op_event_in_message = publish_msg('specific_event', event_type='ble_op_event')

        with allure.step('校验mysql history_ble_op'):
            checker.check_mysql_tables(ble_op_event_in_message, ['history_ble_op'])

    def test_nkc_nfc_event(self, vid, publish_msg, checker):
        # NT2 NFC卡事件上报
        nextev_message, ble_op_event_in_message = publish_msg('specific_event', event_type='nkc_nfc_op')

        with allure.step('校验mysql history_nkc_op'):
            checker.check_mysql_tables(ble_op_event_in_message, ['history_nkc_op'])

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

    @pytest.mark.skip("manual")
    def test_ventilation_dry_event(self, env, vid, redis_key_front, publish_msg, checker):
        """
        运行此条case之前，须登录nio app
        因为消息平台要在数据库message_test_new的表bindings检查account id是否存在和设备的绑定关系，来确认用户是否在登录态，只有在登录态会push
        :param env:
        :param vid:
        :param redis_key_front:
        :param publish_msg:
        :param checker:
        :return:
        """
        # 清除缓存
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        account_id = env['vehicles']['normal']['account_id']
        key = f'{remote_vehicle_key_front}:app_push:ven_dry:{vid}:{account_id}'
        checker.redis.delete(key)

        # 上报ventilation_dry_event事件，车辆满足条件
        nextev_message, modem_event_in_message = publish_msg('specific_event',
                                                                      event_type='ventilation_dry_event',
                                                                      data={
                                                                          'event_detail': random.choice(
                                                                              ['timeout', 'seat_occp_frnt_ri_exist',
                                                                               'anti_theft_warn_on', 'soc_low',
                                                                               'unkonwn_reason', 'insufficient mileage',
                                                                               'dcdc_status_not_working', 'invalid']
                                                                          )
                                                                      })

        # 校验
        with allure.step("校验不会向app push"):
            status_dry_in_redis = checker.redis.get(key)
            assert status_dry_in_redis is None

        # 上报ventilation_dry_event事件，车辆不满足条件
        nextev_message, modem_event_in_message = publish_msg('specific_event',
                                                                      event_type='ventilation_dry_event',
                                                                      data={
                                                                          'event_detail': random.choice(
                                                                              ['vehl_not_parked', 'comfort_enable_on']
                                                                          )
                                                                      })

        # 校验
        with allure.step("校验已push干燥功能存入Redis"):
            status_dry_in_redis = json.loads(checker.redis.get(key))
            assert status_dry_in_redis['result_code'] == 'success'

    def test_ble_apu_wal_event(self, vid, publish_msg, checker):
        """
        https://nio.feishu.cn/docs/doccngBldauXY8qeaI9wVAdxL1b?hash=70d3e26021e6199198b08d9de338c585#
        :param vid:
        :param publish_msg:
        :param checker:
        :return:
        """
        # 上报
        nextev_message, ble_apu_wal_message = publish_msg('specific_event', event_type='ble_apu_wal_event')

        with allure.step('校验mysql'):
            ble_apu_wal_event_in_mysql = checker.mysql_rvs_data.fetch('history_ble_apu_wal',
                                                          {"vehicle_id": vid,
                                                           "sample_ts": timestamp_to_utc_strtime(ble_apu_wal_message['sample_ts'])})[0]

            assert ble_apu_wal_event_in_mysql['device_address'] == ble_apu_wal_message['device_address']
            assert ble_apu_wal_event_in_mysql['device_type'] == ble_apu_wal_message['device_type']
            assert ble_apu_wal_event_in_mysql['trigger_reason'] == ble_apu_wal_message['trigger_reason']
            assert_equal(ast.literal_eval(ble_apu_wal_event_in_mysql['signal_content']), ble_apu_wal_message['signal'])

    def test_fota_package_download_switch(self, vid, publish_msg, checker):
        """
        https://nio.feishu.cn/docs/doccnxzQdCswXr7jaFJaTJIIeEg
        :param vid:
        :param publish_msg:
        :param checker:
        :return:
        """
        # 上报
        nextev_message, fota_package_download_switch = publish_msg('specific_event', event_type='fota_package_download_switch')

        with allure.step('校验mysql'):
            fota_package_download_switch_in_mysql = checker.mysql.fetch('history_specific_event',
                                                          {"vehicle_id": vid,
                                                           "event_type": "fota_package_download_switch",
                                                           "sample_time": timestamp_to_utc_strtime(fota_package_download_switch['sample_ts'])},
                                                          fields=['event_data'])[0]
            assert_equal(fota_package_download_switch, ast.literal_eval(fota_package_download_switch_in_mysql['event_data']))

            res = checker.mysql.fetch_one('vehicle_soft_config', {"vehicle_id": vid, "sample_time": timestamp_to_utc_strtime(fota_package_download_switch['sample_ts'])})

            assert res['type'] == 'switch_fota_pkg_download'
            assert res['value'] == fota_package_download_switch['switch_sts']

    @pytest.mark.parametrize('event_type', ['air_conditioner_event', 'steer_wheel_heating_event', 'seat_heating_event', 'seat_ventilation_event', 'cdc_pin2_immo_event'])
    def test_specific_event_push_hermes(self, vid, publish_msg, checker, kafka, event_type):
        # 重置offset
        kafka['cvs'].set_offset_to_end(kafka['topics']['push_event'])
        # 上报
        _, message = publish_msg('specific_event', event_type=event_type)

        with allure.step('校验mysql'):
            cdc_pin2_immo_event_in_mysql = checker.mysql.fetch('history_specific_event',
                                                               {"vehicle_id": vid,
                                                                "event_type": event_type,
                                                                "sample_time": timestamp_to_utc_strtime(message['sample_ts'])},
                                                               fields=['event_data'])[0]
            assert_equal(message, ast.literal_eval(cdc_pin2_immo_event_in_mysql['event_data']))

        with allure.step('校验kafka {}'.format(kafka['topics']['push_event'])):
            is_found = False
            for data in kafka['cvs'].consume(kafka['topics']['push_event'], timeout=30):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if kafka_msg['data']['sample_ts'] == message['sample_ts'] and vid == kafka_msg['vehicle_id']:
                    is_found = True
                    break
            assert_equal(True, is_found)
            assert_equal(kafka_msg['data'], message)
