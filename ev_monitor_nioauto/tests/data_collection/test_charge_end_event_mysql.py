#!/usr/bin/env python
# coding=utf-8

import random
import pytest
import allure

from utils import message_formator
from utils.assertions import assert_equal


class TestChargeEndMsg(object):

    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    def test_charge_end_event_mysql(self, prepare, publish_msg, checker):
        # 构造并上报消息
        nextev_message, charge_end_obj = publish_msg('charge_end_event',
                                                     vehicle_status={"mileage": prepare['original_mileage'] + 1})

        # 校验
        tables = ['status_position', 'status_vehicle', 'status_soc', 'status_btry_packs']
        checker.check_mysql_tables(charge_end_obj, tables)

    def test_charge_end_event_merge_mysql(self, vid, prepare, publish_msg, checker):
        # 记录mysql初始状态
        original_mysql = checker.mysql.fetch('status_soc', {"id": vid},
                                             exclude_fields=['update_time', 'chg_subsys_len', 'chrg_pwr',
                                                             'chg_subsys_encoding', 'chrg_disp_crrt',
                                                             'charger_type', 'in_volt_ac', 'chrg_disp_volt',
                                                             'in_volt_dc', 'in_curnt_ac', 'battery_pack_cap',
                                                             'estimate_chrg_time', 'chrg_disp_lamp_req'])[0]
        # 第一次上报消息
        nextev_message_1st, charge_end_obj_1st = publish_msg('charge_end_event',
                                                             vehicle_status={
                                                                 "mileage": prepare['original_mileage'] + 1},
                                                             sleep_time=0.1)
        # 第一次上报消息后0.1s立即查询mysql状态
        mysql_after_1st_publish = checker.mysql.fetch('status_soc', {"id": vid},
                                                      exclude_fields=['update_time', 'chg_subsys_len', 'chrg_pwr',
                                                                      'chg_subsys_encoding', 'chrg_disp_crrt',
                                                                      'charger_type', 'in_volt_ac', 'chrg_disp_volt',
                                                                      'in_volt_dc', 'in_curnt_ac', 'battery_pack_cap',
                                                                      'estimate_chrg_time', 'chrg_disp_lamp_req'])[0]
        # 校验mysql状态不改变
        assert_equal(original_mysql, mysql_after_1st_publish)
        # 第二次上报消息
        nextev_message_2nd, charge_end_obj_2nd = publish_msg('charge_end_event',
                                                             vehicle_status={
                                                                 "mileage": prepare['original_mileage'] + 1},
                                                             clear_fields=['soc_status.soc'],
                                                             sleep_time=30 if checker.cmdopt == 'stg' else 2)
        # 第二次上报消息2s后查询mysql状态
        mysql_after_2nd_publish = checker.mysql.fetch('status_soc', {"id": vid},
                                                      exclude_fields=['update_time', 'chg_subsys_len', 'chrg_pwr',
                                                                      'chg_subsys_encoding', 'chrg_disp_crrt',
                                                                      'charger_type', 'in_volt_ac', 'chrg_disp_volt',
                                                                      'in_volt_dc', 'in_curnt_ac', 'battery_pack_cap',
                                                                      'estimate_chrg_time', 'chrg_disp_lamp_req'])[0]
        # 校验merge
        charge_end_obj_2nd['soc_status']['soc'] = charge_end_obj_1st['soc_status']['soc']
        formator = message_formator.MessageFormator(vid, charge_end_obj_2nd['sample_ts'])
        soc_status_in_message = formator.to_mysql_status_soc(charge_end_obj_2nd['soc_status'])
        assert_equal(mysql_after_2nd_publish, soc_status_in_message)

    def test_charge_end_event_mysql_dont_update_mileage(self, vid, prepare, publish_msg, checker):
        # 校验当传入mileage小于Mysql中的数值时，stataus_vehicle表中mileage字段不更新
        nextev_message, charge_end_obj = publish_msg('charge_end_event',
                                                     vehicle_status={"mileage": prepare['original_mileage'] - 1})

        mileage_in_mysql = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])[0]
        with allure.step("校验当传入mileage小于DB中存的值，stataus_vehicle表中mileage字段不更新"):
            # Check other tables will update
            tables = ['status_position', 'status_soc', 'status_btry_packs']
            checker.check_mysql_tables(charge_end_obj, tables)

            # Check other fields in status_vehicle will update
            status_vehicle_in_mysql = \
                checker.mysql.fetch('status_vehicle', {"id": vid}, exclude_fields=['update_time', 'vehl_mode'])[0]
            formator = message_formator.MessageFormator(vid, charge_end_obj['sample_ts'])
            vehicle_status_in_message = formator.to_mysql_status_vehicle(charge_end_obj['vehicle_status'])
            vehicle_status_in_message.pop('mileage')
            status_vehicle_in_mysql.pop('mileage')
            assert_equal(vehicle_status_in_message, status_vehicle_in_mysql)

            # Check mileage won't update
            assert_equal(mileage_in_mysql['mileage'], prepare['original_mileage'])

    def test_posng_valid_type(self, prepare, publish_msg, vid, checker):
        with allure.step("校验 位置信息标为无效时，只要经纬度不为0或null，status_position仍会保存位置信息"):
            nextev_message, charge_end_obj = publish_msg('charge_end_event',
                                                         vehicle_status={
                                                             "mileage": prepare['original_mileage'] + 1
                                                         },
                                                         position_status={
                                                             "posng_valid_type": random.choice([1, 2])
                                                         }
                                                         )

            tables = ['status_position', 'status_vehicle', 'status_soc', 'status_btry_packs']
            checker.check_mysql_tables(charge_end_obj, tables)

    def test_latitude_longitude_is_zero(self, vid, prepare, publish_msg, checker):
        with allure.step("校验 当经度或纬度为0时，不管位置信息标识为有效还是无效，status_position都不会保存位置信息"):
            mileage = prepare['original_mileage']

            original_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]

            position_status = random.choice(
                [{'longitude': 110.111111, 'latitude': 0}, {'longitude': 0, 'latitude': 35.333333}])

            nextev_message, charge_end_obj = publish_msg('charge_end_event',
                                                         vehicle_status={
                                                             "mileage": prepare['original_mileage'] + 1
                                                         },
                                                         position_status=position_status,
                                                         )

            # Check other tables will update
            tables = ['status_vehicle', 'status_soc', 'status_btry_packs']
            checker.check_mysql_tables(charge_end_obj, tables)

            # Check position won't update
            new_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            assert_equal(original_position_status_in_mysql, new_position_status_in_mysql)

    def test_latitude_longitude_is_null(self, prepare, publish_msg, vid, checker):
        with allure.step("校验 当经度或纬度为null时，不管位置信息标识为有效还是无效，status_position都不会保存位置信息"):
            original_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]

            clear_field = random.choice(['position_status.longitude', 'position_status.latitude'])
            nextev_message, charge_end_obj = publish_msg('charge_end_event',
                                                         vehicle_status={
                                                             "mileage": prepare['original_mileage'] + 1
                                                         },
                                                         clear_fields=[clear_field]
                                                         )

            # Check other tables will update
            tables = ['status_vehicle', 'status_soc', 'status_btry_packs']
            checker.check_mysql_tables(charge_end_obj, tables)

            # Check position won't update
            new_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            assert_equal(original_position_status_in_mysql, new_position_status_in_mysql)

    def test_invalid_btry_pak_sn(self, vid, prepare, publish_msg, checker):
        # 校验 soc_status的btry_paks不会存入status_btry_packs表中，如果btry_pak_sn=0

        # 构造并上报消息
        event_name = 'charge_end_event'
        nextev_message, obj = publish_msg(event_name,
                                          vehicle_status={"mileage": prepare['original_mileage'] + 1},
                                          soc_status={"btry_paks": [{
                                              'btry_pak_sn': 0
                                          }]}
                                          )

        # 校验其他表能正常存入数据
        tables = ['status_position', 'status_vehicle', 'status_soc']
        checker.check_mysql_tables(obj, tables, event_name=event_name)

        # 校验status_btry_packs表不存入btry_pak_sn为0的数据
        btry_paks_status_in_mysql = checker.mysql.fetch('status_btry_packs',
                                                        {"id": vid, "serial_num": obj['soc_status']['btry_paks'][0][
                                                            'btry_pak_sn']},
                                                        retry_num=10)

        assert_equal(len(btry_paks_status_in_mysql), 0)
