#!/usr/bin/env python
# coding=utf-8

"""
:file: test_charge_start_event_mysql.py
:author: chunming.liu
:Date: Created on 2019/1/11
:Description: 充电开始事件，包含电池数据
"""
import allure
import random

from utils import message_formator
from utils.assertions import assert_equal
from utils.time_parse import timestamp_to_utc_strtime
import pytest


class TestChargeStartMsg(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    def test_charge_start_event(self, vid, prepare, publish_msg, checker):
        # 构造并上报消息
        mileage = prepare['original_mileage'] + 1
        nextev_message, charge_start_obj = publish_msg('charge_start_event', sleep_time=5,
                                                       vehicle_status={"mileage": mileage})

        # 校验
        tables = ['status_position', 'status_vehicle', 'status_soc', 'status_btry_packs']

        checker.check_mysql_tables(charge_start_obj, tables, event_name='charge_start_event')

    def test_posng_valid_type(self, vid, prepare, checker, publish_msg):
        with allure.step("校验 位置信息标为无效时，只要经纬度不为0或null，status_position仍会保存位置信息"):
            mileage = prepare['original_mileage'] + 1
            nextev_message, obj = publish_msg('charge_start_event', sleep_time=5,
                                              vehicle_status={"mileage": mileage},
                                              position_status={"posng_valid_type": random.choice([1, 2])}
                                              )

            tables = ['status_position', 'status_vehicle', 'status_soc', 'status_btry_packs']
            checker.check_mysql_tables(obj, tables, event_name='charge_start_event')

    def test_latitude_longitude_is_zero(self, vid, prepare, checker, publish_msg):
        with allure.step("校验 当经度或纬度为0时，不管位置信息标识为有效还是无效，status_position都不会保存位置信息"):
            mileage = prepare['original_mileage'] + 1

            original_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]

            position_status = random.choice([{'longitude': 110.111111, 'latitude': 0}, {'longitude': 0, 'latitude': 35.333333}])
            nextev_message, obj = publish_msg('charge_start_event', sleep_time=5,
                                              vehicle_status={"mileage": mileage},
                                              position_status=position_status
                                              )

            # Check other tables will update
            tables = ['status_vehicle', 'status_soc', 'status_btry_packs']
            checker.check_mysql_tables(obj, tables, event_name='charge_start_event')

            # Check position won't update
            new_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            assert_equal(original_position_status_in_mysql, new_position_status_in_mysql)

    def test_latitude_longitude_is_null(self, vid, prepare, checker, publish_msg):
        with allure.step("校验 当经度或纬度为null时，不管位置信息标识为有效还是无效，status_position都不会保存位置信息"):
            mileage = prepare['original_mileage'] + 1

            original_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]

            clear_field = random.choice(['position_status.longitude', 'position_status.latitude'])
            nextev_message, obj = publish_msg('charge_start_event',
                                              vehicle_status={"mileage": mileage},
                                              clear_fields=[clear_field]
                                              )

            # Check other tables will update
            tables = ['status_vehicle', 'status_soc', 'status_btry_packs']
            checker.check_mysql_tables(obj, tables, event_name='charge_start_event')

            # Check position won't update
            new_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            assert_equal(original_position_status_in_mysql, new_position_status_in_mysql)

    def test_invalid_btry_pak_sn(self, vid, prepare, publish_msg, checker):
        # 校验 soc_status的btry_paks不会存入status_btry_packs表中，如果btry_pak_sn=0

        # 构造并上报消息
        event_name = 'charge_start_event'
        mileage = prepare['original_mileage'] + 1
        nextev_message, obj = publish_msg(event_name,
                                          vehicle_status={"mileage": mileage},
                                          soc_status={"btry_paks": [{
                                              'btry_pak_sn': 0
                                          }]}
                                          )

        # 校验其他表能正常存入数据
        tables = ['status_position', 'status_vehicle', 'status_soc']
        checker.check_mysql_tables(obj, tables, event_name=event_name)

        # 校验status_btry_packs表不存入btry_pak_sn为0的数据
        btry_paks_status_in_mysql = checker.mysql.fetch('status_btry_packs',
                                                        {"id": vid, "serial_num": obj['soc_status']['btry_paks'][0]['btry_pak_sn']})
        assert_equal(len(btry_paks_status_in_mysql), 0)

    def test_invalid_soc(self, publish_msg, vid, checker, prepare):
        with allure.step('校验 soc <0 或者>100时，soc字段不会存在mysql中，其他字段照常存入'):
            event_name = 'charge_start_event'
            soc = random.choice([-1, 101])

            status_soc_in_mysql_old = checker.mysql.fetch('status_soc', {"id": vid}, exclude_fields=['update_time', 'chg_subsys_len', 'chg_subsys_encoding', 'max_soc', 'battery_pack_cap'])[0]
            status_vehicle_in_mysql_old = checker.mysql.fetch('status_vehicle', {"id": vid}, exclude_fields=['update_time'])[0]

            nextev_message, obj = publish_msg(event_name,
                                              vehicle_status={'soc': soc, 'mileage': prepare['original_mileage']},
                                              soc_status={"soc": soc}
                                              )
            formator = message_formator.MessageFormator(vid, obj['sample_ts'])
            soc_status_in_message = formator.to_mysql_status_soc(obj['soc_status'], obj['charging_info'])
            soc_status_in_message.pop('soc')

            with allure.step('校验除status_soc 与 status_vehicle表外其他表能正常存入数据'):
                tables = ['status_position']
                checker.check_mysql_tables(obj, tables, event_name=event_name)

            with allure.step('校验status_soc表soc字段值为上报之前的值'):
                status_soc_in_mysql_new = checker.mysql.fetch('status_soc', {"id": vid, "sample_time": timestamp_to_utc_strtime(obj['sample_ts'])},
                                                              exclude_fields=['update_time', 'chg_subsys_len', 'chrg_pwr',
                                                                          'chg_subsys_encoding', 'chrg_disp_crrt', 'battery_pack_cap',
                                                                          'chrg_disp_lamp_req', 'chrg_disp_volt'])[0]
                assert_equal(status_soc_in_mysql_old['soc'], status_soc_in_mysql_new['soc'])

            with allure.step('校验status_soc表除soc以外的字段照常存入新值'):
                status_soc_in_mysql_new.pop('soc')
                assert_equal(status_soc_in_mysql_new, soc_status_in_message)

            with allure.step('校验status_vehicle表除soc以外的字段照常存入新值'):
                status_vehicle_in_mysql_new = checker.mysql.fetch('status_vehicle', {"id": vid}, exclude_fields=['update_time'])[0]
                assert_equal(status_vehicle_in_mysql_old['soc'], status_vehicle_in_mysql_new['soc'])

            with allure.step('校验status_vehicle表soc字段值为上报之前的值'):
                status_vehicle_in_mysql_new.pop('soc')
                assert_equal(status_soc_in_mysql_new, soc_status_in_message)

    def test_invalid_remaining_range(self, publish_msg, vid, checker):
        with allure.step('校验 remaining_range <0 或者>1000时，remaining_range字段不会存在mysql中，其他字段照常存入'):
            event_name = 'charge_start_event'
            remaining_range = random.choice([-0.5, 1000.5])

            status_soc_in_mysql_old = checker.mysql.fetch('status_soc', {"id": vid}, exclude_fields=['update_time', 'chg_subsys_len', 'chg_subsys_encoding', 'max_soc', 'battery_pack_cap'])[0]

            nextev_message, obj = publish_msg(event_name,
                                              soc_status={"remaining_range": remaining_range}
                                              )
            formator = message_formator.MessageFormator(vid, obj['sample_ts'])
            soc_status_in_message = formator.to_mysql_status_soc(obj['soc_status'], obj['charging_info'])

            with allure.step('校验除status_soc表外其他表能正常存入数据'):
                tables = ['status_position']
                checker.check_mysql_tables(obj, tables, event_name=event_name)

            with allure.step('校验status_soc表remaining_range字段值为上报之前的值'):
                status_soc_in_mysql_new = checker.mysql.fetch_one('status_soc',
                                                                  {"id": vid, "sample_time": timestamp_to_utc_strtime(obj['sample_ts'])},
                                                                  exclude_fields=['update_time', 'chg_subsys_len', 'chrg_pwr', 'chg_subsys_encoding', 'battery_pack_cap',
                                                                                  'chrg_disp_crrt', 'chrg_disp_lamp_req', 'chrg_disp_volt'])
                assert_equal(status_soc_in_mysql_old['remaining_range'], status_soc_in_mysql_new['remaining_range'])

            with allure.step('校验status_soc表除remaining_range以外的字段照常存入新值'):
                status_soc_in_mysql_new.pop('remaining_range')
                soc_status_in_message.pop('remaining_range')
                assert_equal(status_soc_in_mysql_new, soc_status_in_message)

    def test_outside_china_position(self, publish_msg, vid, checker, prepare):
        with allure.step('校验 position的纬度latitude及经度longitude在中国范围内。若不在，则该两字段不更新，其他字段照常更新'):
            event_name = 'charge_start_event'

            status_position_mysql_old = checker.mysql.fetch('status_position', {"id": vid}, exclude_fields=['update_time', 'area_code'])[0]

            latitude, longitude = random.choice([
                (52, 115), (50, 130), (43, 133), (21, 105), (21, 107),
                (30, 70), (30, -70), (-30, -70), (-30, 70),
                (90, 180), (-90, -180)
            ])
            nextev_message, obj = publish_msg(event_name,
                                              vehicle_status={"mileage": prepare['original_mileage']},
                                              position_status={'latitude': latitude, 'longitude': longitude},
                                              sleep_time=4
                                              )

            formator = message_formator.MessageFormator(vid, obj['sample_ts'])
            status_position_msg = formator.to_mysql_status_position(obj['position_status'])

            with allure.step('校验除status_position表外其他表能正常存入数据'):
                tables = ['status_vehicle', 'status_soc', 'status_btry_packs']
                checker.check_mysql_tables(obj, tables, event_name=event_name)

            with allure.step('校验status_position表latitude, longitude字段值为上报之前的值'):
                status_position_mysql_new = checker.mysql.fetch('status_position', {"id": vid}, exclude_fields=['update_time', 'area_code'])[0]
                assert_equal(status_position_mysql_old['latitude_wgs84'], status_position_mysql_new['latitude_wgs84'])
                assert_equal(status_position_mysql_old['longitude_wgs84'], status_position_mysql_new['longitude_wgs84'])

            with allure.step('校验status_position表除latitude, longitude以外的字段照常存入新值'):
                status_position_mysql_new.pop('latitude_wgs84')
                status_position_mysql_new.pop('longitude_wgs84')
                status_position_msg.pop('latitude_wgs84')
                status_position_msg.pop('longitude_wgs84')
                status_position_mysql_new.pop('latitude_gcj02')
                status_position_mysql_new.pop('longitude_gcj02')
                status_position_msg.pop('latitude_gcj02')
                status_position_msg.pop('longitude_gcj02')
                assert_equal(status_position_mysql_new, status_position_msg)
