#!/usr/bin/env python
# coding=utf-8

"""
:file: test_instant_status_resp_mysql.py
:author: muhan.chen
:Date: Created on 2018/5/30 下午5:18
:Description: 上报车辆的全量数据
"""
import random
import pytest
import time
import allure

from utils.assertions import assert_equal
from utils import message_formator, time_parse


@allure.feature('上报车辆的全量事件')
class TestInstantStatusMsg(object):
    @allure.story('车机处于离线状态，当恢复在线状态上报此事件，保证app显示为最新的车辆状态')
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    @pytest.mark.parametrize('clear_fields', [['sample_point.door_status.door_locks.account_id'], []], ids=['NT1', 'NT2'])
    def test_instant_status_resp(self, vid, prepare, checker, publish_msg, clear_fields):
        # 构造并上报消息
        mileage = prepare['original_mileage'] + 1
        nextev_message, instant_status_obj = publish_msg('instant_status_resp',
                                                         sample_point={
                                                             "vehicle_status": {
                                                                 "mileage": mileage}
                                                         },
                                                         platform_type=1 if clear_fields is None else 0,
                                                         clear_fields=clear_fields
                                                         )


        # 校验
        tables = ['status_position', 'status_vehicle', 'status_soc',
                  'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                  'status_extremum_data', 'status_driving_data', 'status_hvac',
                  'status_tyre', 'status_door', 'status_light', 'status_window']

        checker.check_mysql_tables(instant_status_obj['sample_point'], tables)

    def test_outside_sample_ts(self, vid, prepare, checker, publish_msg):
        # 校验当外层采样时间outside_sample_ts有值时，采样时间选用外层采样时间,不管外部采样时间比内部采样时间大还是小

        # 构造并上报消息
        mileage = prepare['original_mileage'] + 1
        nextev_message, instant_status_obj = publish_msg('instant_status_resp',
                                                         outside_sample_ts=int(round(time.time() * 1000))-1000,
                                                         sample_point={
                                                             "vehicle_status": {
                                                                 "mileage": mileage},
                                                             'sample_ts': int(round(time.time() * 1000))
                                                         }
                                                         )

        # 校验
        tables = ['status_position', 'status_vehicle', 'status_soc',
                  'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                  'status_extremum_data', 'status_driving_data', 'status_hvac',
                  'status_tyre', 'status_door', 'status_light', 'status_window']

        checker.check_mysql_tables(instant_status_obj['sample_point'], tables, sample_ts=instant_status_obj['sample_ts'])

    def test_mileage_wont_update(self, vid, checker, prepare, publish_msg):
        # 校验当传入mileage为0，stataus_vehicle表中mileage字段不更新
        nextev_message, instant_status_obj = publish_msg('instant_status_resp',
                                                         sample_point={
                                                             "vehicle_status": {
                                                                 "mileage": 0}
                                                         })

        with allure.step("校验当传入mileage为0，stataus_vehicle表中mileage字段不更新"):
            mileage_in_mysql = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])[0]
            assert_equal(mileage_in_mysql['mileage'], prepare['original_mileage'])

    def test_posng_valid_type(self, vid, prepare, checker, publish_msg):
        with allure.step("校验 位置信息标为无效时，只要经纬度不为0或null，status_position仍会保存位置信息"):
            # 上报
            vid = vid
            mileage = prepare['original_mileage'] + 1
            nextev_message, obj = publish_msg('instant_status_resp',
                                              sample_point=
                                              {
                                                  "vehicle_status": {"mileage": mileage},
                                                  "position_status":{
                                                      "posng_valid_type": random.choice([1, 2])
                                                  }
                                              }
                                              )

            # 校验
            tables = ['status_position', 'status_vehicle', 'status_soc',
                      'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre', 'status_door', 'status_light', 'status_window']
            checker.check_mysql_tables(obj['sample_point'], tables)

    def test_latitude_longitude_is_zero(self, vid, prepare, checker, publish_msg):
        with allure.step("校验 当经度或纬度为0时，不管位置信息标识为有效还是无效，status_position都不会保存位置信息"):
            # 上报
            mileage = prepare['original_mileage'] + 1
            original_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]

            position_status = random.choice([{'longitude':110.111111,'latitude':0},{'longitude':0,'latitude':35.333333}])

            nextev_message, obj = publish_msg('instant_status_resp',
                                              sample_point=
                                              {
                                                  "vehicle_status": {"mileage": mileage},
                                                  "position_status":position_status
                                              }
                                              )

            # 校验
            # Check other tables will update
            tables = ['status_vehicle', 'status_soc',
                      'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre', 'status_door', 'status_light', 'status_window']
            checker.check_mysql_tables(obj['sample_point'], tables)

            # Check position won't update
            new_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            assert_equal(original_position_status_in_mysql, new_position_status_in_mysql)

    def test_latitude_longitude_is_null(self, vid, prepare, checker, publish_msg):
        with allure.step("校验 当经度或纬度为null时，不管位置信息标识为有效还是无效，status_position都不会保存位置信息"):
            mileage = prepare['original_mileage'] + 1
            original_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]

            clear_field = random.choice(['sample_point.position_status.longitude','sample_point.position_status.latitude'])
            nextev_message, obj = publish_msg('instant_status_resp',
                                              sample_point=
                                              {
                                                  "vehicle_status": {"mileage": mileage},
                                              },
                                              clear_fields=[clear_field]
                                              )
            # 校验
            # Check other tables will update
            tables = ['status_vehicle', 'status_soc',
                      'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                      'status_extremum_data', 'status_driving_data', 'status_hvac',
                      'status_tyre', 'status_door', 'status_light', 'status_window']

            checker.check_mysql_tables(obj['sample_point'], tables)

            # Check position won't update
            new_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            assert_equal(original_position_status_in_mysql, new_position_status_in_mysql)

    @pytest.mark.test
    def test_invalid_btry_pak_sn(self, vid, prepare, publish_msg, checker):
        # 校验 soc_status的btry_paks不会存入status_btry_packs表中，如果btry_pak_sn=0

        # 构造并上报消息
        event_name = 'instant_status_resp'
        mileage = prepare['original_mileage'] + 1
        nextev_message, obj = publish_msg(event_name,
                                          sample_point=
                                          {
                                              "vehicle_status": {"mileage": mileage},
                                              "soc_status":{"btry_paks": [{
                                                           'btry_pak_sn': 0
                                                       }]}
                                          },
                                          )

        # 校验其他表能正常存入数据
        tables = ['status_position', 'status_vehicle', 'status_soc',
                   'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                  'status_extremum_data', 'status_driving_data', 'status_hvac',
                  'status_tyre']

        checker.check_mysql_tables(obj['sample_point'], tables, event_name=event_name)

        # 校验status_btry_packs表不存入btry_pak_sn为0的数据
        btry_paks_status_in_mysql = checker.mysql.fetch('status_btry_packs',
                                                       {"id": vid, "serial_num": obj['sample_point']['soc_status']['btry_paks'][0]['btry_pak_sn']},
                                                        retry_num=10)
        assert_equal(len(btry_paks_status_in_mysql), 0)

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
        with allure.step("上报携带623,537,590的can消息的instant_status_resp事件"):
            event_name = 'instant_status_resp'
            mileage = prepare['original_mileage'] + 1
            nextev_message, obj = publish_msg(event_name,
                                              sample_point={"vehicle_status": {"mileage": mileage},
                                                            'can_msg': {
                                                                'can_data': [
                                                                    {
                                                                        'msg_id': 623,
                                                                        'value': '0002140623101102'
                                                                    },
                                                                    {
                                                                        'msg_id': 537,
                                                                        'value': '3101102000214062'
                                                                    },
                                                                    {
                                                                        'msg_id': 590,
                                                                        'value': 'ffffffffffffffff'
                                                                    }
                                                                ]
                                                            }
                                              })

        with allure.step("校验status_soc表的存储"):
            status_soc_in_mysql = checker.mysql.fetch_one('status_soc',
                                                          {"id": vid, "sample_time": time_parse.timestamp_to_utc_strtime(obj['sample_point']['sample_ts'])},
                                                          exclude_fields=['update_time', 'chg_subsys_len', 'chg_subsys_encoding', 'chrg_pwr', 'chrg_disp_crrt', 'chrg_disp_volt'])
            formator = message_formator.MessageFormator(vid, obj['sample_point']['sample_ts'])
            soc_status_in_message = formator.to_mysql_status_soc(obj['sample_point']['soc_status'], obj['sample_point']['charging_info'])
            soc_status_in_message['battery_pack_cap'] = 0
            # soc_status_in_message['chrg_pwr'] = 523.5
            # soc_status_in_message['chrg_disp_crrt'] = 4553.5
            # soc_status_in_message['chrg_disp_volt'] = 1023.5
            soc_status_in_message['chrg_disp_lamp_req'] = 0
            assert_equal(status_soc_in_mysql, soc_status_in_message)

        with allure.step("校验mongo can_msg,电池信息上报10分钟之内在mongo查询，超过10分钟查询mysql"):
            can_msg_in_mongo = checker.mongodb.find("can_msg", {"_id": f"{vid}_623"})[0]
            assert can_msg_in_mongo['timestamp'] == obj['sample_point']['sample_ts']
            assert can_msg_in_mongo['value']['BMSBatteryPackCap'] == 0