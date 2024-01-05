#!/usr/bin/env python
# coding=utf-8

"""
:file: test_periodical_charge_update_mysql.py
:Description: 周期性充电消息上报，包含position_status数据，driving_data数据，vehicle_status数据，occupant_status数据，soc_status数据，
:alarm数据，driving_motor数据，extremum数据。
"""
import random
import time

import pytest
import allure

from utils import message_formator
from utils.assertions import assert_equal
from utils.time_parse import timestamp_to_utc_strtime


class TestChargeUpdateMsg(object):
    @pytest.fixture(scope='function', autouse=True)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    def test_periodical_charge_update(self, vid, prepare, checker, publish_msg):
        # 构造并上报消息
        mileage = prepare['original_mileage'] + 1
        nextev_message, charge_update_obj = publish_msg('periodical_charge_update',
                                                        sample_points=
                                                        [{
                                                            "vehicle_status": {"mileage": mileage}
                                                        }])

        # 校验
        tables = ['status_position', 'status_vehicle', 'status_soc',
                  'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                  'status_extremum_data', 'status_driving_data', 'status_hvac',
                  'status_tyre']
        for sample_point in charge_update_obj['sample_points']:
            checker.check_mysql_tables(sample_point, tables)

    def test_periodical_charge_update_merge_reissue(self, vid, prepare, checker, publish_msg):

        mileage = prepare['original_mileage'] + 1
        # 记录mysql初始状态
        original_mysql = checker.mysql.fetch('status_soc', {"id": vid},
                                             exclude_fields=['update_time', 'chg_subsys_len', 'chrg_disp_crrt',
                                                             'chg_subsys_encoding', 'chrg_disp_lamp_req',
                                                             'charger_type', 'in_volt_ac', 'chrg_disp_volt',
                                                             'in_volt_dc', 'in_curnt_ac', 'chrg_pwr',
                                                             'estimate_chrg_time'])[0]
        # 上报补发消息
        nextev_message_1st, charge_update_obj_1st = publish_msg('periodical_charge_update',
                                                                reissue=True,
                                                                sleep_time=0.1,
                                                                sample_points=
                                                                [{
                                                                    "vehicle_status": {"mileage": mileage}
                                                                }])
        # 上报补发消息后0.1s立即查询mysql状态是否改变
        mysql_after_1st_publish = checker.mysql.fetch('status_soc', {"id": vid},
                                                      exclude_fields=['update_time', 'chg_subsys_len', 'chrg_disp_crrt',
                                                                      'chg_subsys_encoding', 'chrg_disp_lamp_req',
                                                                      'charger_type', 'in_volt_ac', 'chrg_disp_volt',
                                                                      'in_volt_dc', 'in_curnt_ac', 'chrg_pwr',
                                                                      'estimate_chrg_time'])[0]
        # 校验mysql状态不改变
        assert_equal(original_mysql, mysql_after_1st_publish)
        # 上报空soc字段消息
        nextev_message_2nd, charge_update_obj_2nd = publish_msg('periodical_charge_update',
                                                                reissue=False,
                                                                sleep_time=2,
                                                                clear_fields=['sample_points[0].soc_status.soc'],
                                                                sample_points=
                                                                [{
                                                                    "vehicle_status": {"mileage": mileage}
                                                                }])
        # 查询mysql
        mysql_after_2nd_publish = checker.mysql.fetch('status_soc', {"id": vid, "sample_time": timestamp_to_utc_strtime(charge_update_obj_2nd['sample_points'][0]['sample_ts'])},
                                                      exclude_fields=['update_time', 'chg_subsys_len', 'chrg_disp_crrt',
                                                                      'chg_subsys_encoding', 'chrg_disp_lamp_req',
                                                                      'charger_type', 'in_volt_ac', 'chrg_disp_volt',
                                                                      'in_volt_dc', 'in_curnt_ac', 'chrg_pwr',
                                                                      'estimate_chrg_time', 'battery_pack_cap'])[0]

        charge_update_obj_2nd['sample_points'][0]['soc_status']['soc'] = charge_update_obj_1st['sample_points'][0]['soc_status']['soc']
        # 校验reissue后是merge
        formator = message_formator.MessageFormator(vid, charge_update_obj_2nd['sample_points'][0]['sample_ts'])

        soc_status_in_message = formator.to_mysql_status_soc(charge_update_obj_2nd['sample_points'][0]['soc_status'])
        assert_equal(mysql_after_2nd_publish, soc_status_in_message)

    def test_mileage_wont_update(self, vid, checker, prepare, publish_msg):
        """
        更新mileage时，与对redis中存储的车辆里程数据和时间戳进行对比，而非mysql
        redis查询：hget data_collection_test: mileage_prefix <vid>
        确保运行该case时较上一次里程更新不超过大概5小时的时间
        """

        with allure.step("校验当传入mileage为0，stataus_vehicle表中mileage字段不更新"):
            publish_msg('periodical_charge_update', sample_points=[{"vehicle_status": {"mileage": 0}}])
            mileage_in_mysql = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])[0]
            assert_equal(mileage_in_mysql['mileage'], prepare['original_mileage'])

        with allure.step("校验当传入mileage较上次里程减少时，stataus_vehicle表中mileage字段不更新"):
            publish_msg('periodical_charge_update', sample_points=[{"vehicle_status": {"mileage": prepare['original_mileage'] - 1}}])
            mileage_in_mysql = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])[0]
            assert_equal(mileage_in_mysql['mileage'], prepare['original_mileage'])

        # 当里程较上次更新增加大于500km且小于50000km时，将检查其平均每天里程不超过2000km，即平均每秒的里程增加不超过0.02314815km，才允许更新。
        with allure.step("校验里程较上次更新增加大于500km且小于50000km时，平均每秒的里程增加超过0.02314815km，不会更新"):
            publish_msg('periodical_charge_update', sample_points=[{"vehicle_status": {"mileage": prepare['original_mileage'] + 501}}])
            mileage_in_mysql = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])[0]
            assert_equal(mileage_in_mysql['mileage'], prepare['original_mileage'])

        # 当里程较上次更新增加大于50000km时，将检查其平均每天里程不超过1200km，即平均每秒的里程增加不超过0.01388889km，才允许更新。
        with allure.step("校验里程较上次更新增加大于50000km时，其平均每秒的里程增加超过0.01388889km，不会更新"):
            publish_msg('periodical_charge_update', sample_points=[{"vehicle_status": {"mileage": prepare['original_mileage'] + 50001}}])
            mileage_in_mysql = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])[0]
            assert_equal(mileage_in_mysql['mileage'], prepare['original_mileage'])

    def test_same_mileage_update_slampleTs(self, vid, redis_key_front, publish_msg, redis):
        with allure.step("校验报同一个里程，更新redis中的sample_ts，以redis缓存的里程为准"):
            data_collection_key_front = redis_key_front['data_collection']
            key_front = f'{data_collection_key_front}:{vid}'
            original_data_in_redis = redis['cluster'].hash_hget(key_front, 'mileage_prefix').split('|')
            publish_msg('periodical_charge_update', sample_points=[{"vehicle_status": {"mileage": int(original_data_in_redis[1])}}])
            new_data_in_redis = redis['cluster'].hash_hget(key_front, 'mileage_prefix').split('|')
            assert_equal(original_data_in_redis[0] == new_data_in_redis[0], False)
            assert_equal(original_data_in_redis[1], new_data_in_redis[1])

    @pytest.mark.test
    def test_reissue(self, vid, checker, prepare, publish_msg):
        mileage = prepare['original_mileage'] + 1
        with allure.step("校验当reissue为True时，mysql数据库仍会更新"):
            # 构造并上报消息
            nextev_message, charge_update_obj = publish_msg('periodical_charge_update',
                                                            reissue=True,
                                                            sample_points=
                                                            [{
                                                                "vehicle_status": {"mileage": mileage}
                                                            }])

            # 校验
            tables = ['status_position', 'status_vehicle', 'status_soc',
                      'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre']

            for sample_point in charge_update_obj['sample_points']:
                checker.check_mysql_tables(sample_point, tables)

    @pytest.mark.test
    def test_posng_valid_type(self, vid, prepare, checker, publish_msg):
        with allure.step("校验 位置信息标为无效时，只要经纬度不为0或null，status_position仍会保存位置信息"):
            # 上报
            mileage = prepare['original_mileage'] + 1
            nextev_message, obj = publish_msg('periodical_charge_update',
                                              sample_points=
                                              [{
                                                  "vehicle_status": {"mileage": mileage},
                                                  "position_status": {
                                                      "posng_valid_type": random.choice([1, 2])
                                                  }
                                              }]
                                              )

            # 校验
            tables = ['status_position', 'status_vehicle', 'status_soc',
                      'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre']

            for sample_point in obj['sample_points']:
                checker.check_mysql_tables(sample_point, tables)

    @pytest.mark.test
    def test_latitude_longitude_is_zero(self, vid, prepare, checker, publish_msg):
        with allure.step("校验 当经度或纬度为0时，不管位置信息标识为有效还是无效，status_position都不会保存位置信息"):
            # 上报
            mileage = prepare['original_mileage'] + 1
            original_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]

            position_status = random.choice(
                [{'longitude': 110.111111, 'latitude': 0}, {'longitude': 0, 'latitude': 35.333333}])

            nextev_message, obj = publish_msg('periodical_charge_update',
                                              sample_points=
                                              [{
                                                  "vehicle_status": {"mileage": mileage},
                                                  "position_status": position_status
                                              }]
                                              )

            # 校验
            # Check other tables will update
            tables = ['status_vehicle', 'status_soc',
                      'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre']

            for sample_point in obj['sample_points']:
                checker.check_mysql_tables(sample_point, tables)

            # Check position won't update
            new_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            assert_equal(original_position_status_in_mysql, new_position_status_in_mysql)

    def test_latitude_longitude_is_null(self, vid, prepare, checker, publish_msg):
        with allure.step("校验 当经度或纬度为null时，不管位置信息标识为有效还是无效，status_position都不会保存位置信息"):
            mileage = prepare['original_mileage'] + 1
            original_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]

            clear_field = random.choice(['sample_points[0].position_status.longitude', 'sample_points[0].position_status.latitude'])
            nextev_message, obj = publish_msg('periodical_charge_update',
                                              sample_points=
                                              [{
                                                  "vehicle_status": {"mileage": mileage},
                                              }],
                                              clear_fields=[clear_field]
                                              )

            # 校验
            # Check other tables will update
            tables = ['status_vehicle', 'status_soc',
                      'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre']

            for sample_point in obj['sample_points']:
                checker.check_mysql_tables(sample_point, tables)

            # Check position won't update
            new_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            assert_equal(original_position_status_in_mysql, new_position_status_in_mysql)

    @pytest.mark.test
    def test_invalid_btry_pak_sn(self, vid, prepare, publish_msg, checker):
        # 校验 soc_status的btry_paks不会存入status_btry_packs表中，如果btry_pak_sn=0

        # 构造并上报消息
        event_name = 'periodical_charge_update'
        mileage = prepare['original_mileage'] + 1
        nextev_message, obj = publish_msg(event_name,
                                          sample_points=
                                          [{
                                              "vehicle_status": {"mileage": mileage},
                                              "soc_status": {"btry_paks": [{
                                                  'btry_pak_sn': 0
                                              }]}
                                          }],
                                          )

        # 校验其他表能正常存入数据
        tables = ['status_position', 'status_vehicle', 'status_soc',
                  'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                  'status_extremum_data', 'status_driving_data',  'status_hvac',
                  'status_tyre']
        checker.check_mysql_tables(obj['sample_points'][0], tables, event_name=event_name)

        # 校验status_btry_packs表不存入btry_pak_sn为0的数据
        btry_paks_status_in_mysql = checker.mysql.fetch('status_btry_packs',
                                                        {"id": vid, "serial_num":
                                                            obj['sample_points'][0]['soc_status']['btry_paks'][0][
                                                                'btry_pak_sn']},
                                                        retry_num=10)
        assert_equal(len(btry_paks_status_in_mysql), 0)

    @pytest.mark.test
    def test_gps_time_less_than_sample_ts(self, prepare, vid, publish_msg, checker):
        with allure.step('校验上报的sample_ts-gps_ts>24小时，position_status数据不落库'):
            # 构造并上报消息
            event_name = 'periodical_charge_update'
            mileage = prepare['original_mileage'] + 1
            original_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            sample_ts = round(time.time() * 1000)
            nextev_message, obj = publish_msg(event_name,
                                              sample_points=
                                              [{
                                                  "vehicle_status": {"mileage": mileage},
                                                  'sample_ts': sample_ts,
                                                  'position_status': {
                                                      'gps_ts': sample_ts - 24 * 60 * 60 * 1000 - 1
                                                  }
                                              }],
                                              )

            # 校验其他表能正常存入数据
            tables = ['status_vehicle', 'status_soc',
                      'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre', 'status_btry_packs']
            checker.check_mysql_tables(obj['sample_points'][0], tables, event_name=event_name)
            # 校验status_positon表不落库
            new_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            assert_equal(original_position_status_in_mysql, new_position_status_in_mysql)

    def test_gps_time_null(self, prepare, vid, publish_msg, checker):
        with allure.step('校验上报的gps_time为null时，position_status数据不落库'):
            # 构造并上报消息
            event_name = 'periodical_charge_update'
            mileage = prepare['original_mileage'] + 1
            clear_fields = ['sample_points[0].position_status.gps_ts']
            original_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]

            nextev_message, obj = publish_msg(event_name,
                                              sample_points=
                                              [{
                                                  "vehicle_status": {"mileage": mileage},
                                              }],
                                              clear_fields=clear_fields
                                              )

            # 校验其他表能正常存入数据
            tables = ['status_vehicle', 'status_soc',
                      'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre', 'status_btry_packs']
            checker.check_mysql_tables(obj['sample_points'][0], tables, event_name=event_name)
            # 校验status_positon表不落库
            new_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            assert_equal(original_position_status_in_mysql, new_position_status_in_mysql)

    def test_gps_time_lager_than_sample_ts(self, prepare, vid, publish_msg, checker):
        """
        当gps_ts在以下范围内时，才能够将其更新到status_position中。
        sample_ts - 1day <= gps_ts <= 服务器当前时间 + 1hour
        """
        with allure.step('校验上报的gps_ts大于sample_ts时，position_status数据落库'):
            old_update_time = checker.mysql.fetch('status_position', {"id": vid})[0]["update_time"]
            # 构造并上报消息
            event_name = 'periodical_charge_update'
            mileage = prepare['original_mileage'] + 1
            original_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            sample_ts = round(time.time() * 1000)
            nextev_message, obj = publish_msg(event_name,
                                              sample_points=
                                              [{
                                                  "vehicle_status": {"mileage": mileage},
                                                  'sample_ts': sample_ts,
                                                  'position_status': {
                                                      'gps_ts': sample_ts - 24 * 60 * 60 * 1000 - 1
                                                  }
                                              }],
                                              )

            # 校验除 status_position 的所有表都能正常存入数据
            tables = ['status_vehicle', 'status_soc',
                      'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre', 'status_btry_packs']
            checker.check_mysql_tables(obj['sample_points'][0], tables, event_name=event_name)
            # 校验 status_position 表不会更新
            new_update_time = checker.mysql.fetch('status_position', {"id": vid})[0]["update_time"]
            assert_equal(new_update_time, old_update_time)

    def test_parse_can_msg(self, vid, prepare, publish_msg, checker):
        """
        https://jira.nioint.com/browse/CVS-14698
        携带can id为623，信号名为BMSBatteryPackCap的can消息，解析出BMSBatteryPackCap，写入soc_status表的字段battery_pack_cap里
        http://venus.nioint.com/#/detailWorkflow/wf-20220424145320-l2
        携带can id为537，590解析VCUChrgDispLampReq,VCUChrgDispCrrt,VCUChrgDispVolt,VCUChrgPwr字段，存储到stauts_soc表中
        :param vid:
        :param prepare:
        :param publish_msg:
        :param checker:
        :return:
        """
        with allure.step("上报携带BMSBatteryPackCap的can消息的instant_status_resp事件"):
            event_name = 'periodical_charge_update'
            mileage = prepare['original_mileage'] + 1
            nextev_message, obj = publish_msg(event_name,
                                              sample_points=[{"vehicle_status": {"mileage": mileage},
                                                             'can_msg': {
                                                                'can_data': [
                                                                    {
                                                                        'msg_id': 623,
                                                                        'value': b'\x00\x02\x14\x16\x23\x10\x11\x02'
                                                                    },
                                                                    {
                                                                        'msg_id': 537,
                                                                        'value': '3101f02000214062'
                                                                    },
                                                                    {
                                                                        'msg_id': 590,
                                                                        'value': 'ffffffffffffffff'
                                                                    }
                                                                ]
                                                             }
                                              }])

        with allure.step("校验status_soc表的存储"):
            status_soc_in_mysql = checker.mysql.fetch_one('status_soc',
                                                          {"id": vid, "sample_time": timestamp_to_utc_strtime(obj['sample_points'][0]['sample_ts'])},
                                                          exclude_fields=['update_time', 'chg_subsys_len', 'chrg_pwr', 'chg_subsys_encoding',
                                                                          'chrg_disp_crrt', 'chrg_disp_volt'])
            formator = message_formator.MessageFormator(vid, obj['sample_points'][0]['sample_ts'])
            soc_status_in_message = formator.to_mysql_status_soc(obj['sample_points'][0]['soc_status'], obj['sample_points'][0]['charging_info'])
            soc_status_in_message['battery_pack_cap'] = 1
            # soc_status_in_message['chrg_pwr'] = 523.5
            # soc_status_in_message['chrg_disp_crrt'] = 4553.5
            # soc_status_in_message['chrg_disp_volt'] = 1023.5
            soc_status_in_message['chrg_disp_lamp_req'] = 7
            assert_equal(status_soc_in_mysql, soc_status_in_message)

        with allure.step("校验mongo can_msg,电池信息上报10分钟之内在mongo查询，超过10分钟查询mysql"):
            can_msg_in_mongo = checker.mongodb.find("can_msg", {"_id": f"{vid}_623"})[0]
            assert can_msg_in_mongo['timestamp'] == obj['sample_points'][0]['sample_ts']
            assert can_msg_in_mongo['value']['BMSBatteryPackCap'] == 1
