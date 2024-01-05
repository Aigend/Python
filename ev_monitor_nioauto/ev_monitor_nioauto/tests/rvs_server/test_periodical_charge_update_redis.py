#!/usr/bin/env python
# coding=utf-8

"""
:file: test_periodical_charge_update_redis.py
:author: yry
:Date: Created on 2017/1/12 下午8:01
:Description: 周期性充电消息上报
"""
import pytest
import allure
from utils.assertions import assert_equal
import json


class TestChargeUpdateMsg(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    def test_charge_update_event_status_redis(self, vid, redis_key_front, checker, publish_msg, prepare):
        with allure.step("校验正常逻辑充电更新，查看redis中对应数据更新"):

            keys = ['PositionStatus', 'DrivingData', 'TyreStatus',
                    'OccupantStatus', 'SocStatus', 'HvacStatus',
                    'ExteriorStatus', 'ExtremumData','DrivingMotor']
            # 清除redis 缓存
            # 增加staging环境支持
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            # 支持马克波罗服务测试
            key_front = f'{remote_vehicle_key_front}:vehicle_status:{vid}'
            for key in keys:
                checker.redis.delete(f'{key_front}:{key}')
            # 构造并上报消息
            nextev_message, charge_update_obj = publish_msg('periodical_charge_update',sample_points=[{'vehicle_status':{
                                                                          "mileage": prepare['original_mileage'] + 1},
                'can_msg': {
                    'can_data': [
                        {
                            'msg_id': 623,
                            'value': b'\x00\x02\x14\x86\x23\x10\x11\x02'
                        },
                        {
                            'msg_id': 537,
                            'value': b'\xff\xff\xff\xff\xff\xff\xff\xff'
                        }
                    ]
                }
            }], clear_fields=['sample_points[0].alarm_signal']) #充电周期事件如果携带alarm信号, v2l_status不会写入redis

            # 校验
            charge_update_obj['sample_points'][0]['soc_status']['chrg_req'] = 7
            charge_update_obj['sample_points'][0]['soc_status']['battery_pack_cap'] = 8
            checker.check_redis(charge_update_obj['sample_points'][0], keys,
                                event_name='charge_update_event',
                                clear_none=True,
                                sample_ts=charge_update_obj['sample_points'][0]['sample_ts']
                                )

    def test_charge_update_soc_is_0_redis_is_0(self, vid, redis_key_front, checker, publish_msg, prepare):
        keys = ['PositionStatus', 'DrivingData', 'TyreStatus', 'SocStatus',
                'OccupantStatus', 'BmsStatus', 'HvacStatus',
                'ExteriorStatus', 'ExtremumData', 'DrivingMotor']
        # 清除redis 缓存
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        # 支持马克波罗服务测试
        key_front = f'{remote_vehicle_key_front}:vehicle_status:{vid}'
        for key in keys:
            checker.redis.delete(f'{key_front}:{key}')

        with allure.step("校验正常充电更新情况，即全量上报soc=0，查看redis中对应数据更新为0"):
            # 构造并上报消息
            nextev_message, charge_update_obj = publish_msg('periodical_charge_update',
                                                            sample_points=[{'vehicle_status':{
                                                                      "mileage": prepare['original_mileage'] + 1},
                                                                        'soc_status': {'soc': 0}}],
                                                            clear_fields=['sample_points[0].can_msg',
                                                                          'sample_points[0].alarm_signal'])  # 包含alarm_signal会触发slytherin同步redis和mysql的记录

            # 校验
            keys = ['SocStatus']
            checker.check_redis(charge_update_obj['sample_points'][0], keys,
                                event_name='charge_update_event',
                                clear_none=True,
                                sample_ts=charge_update_obj['sample_points'][0]['sample_ts']
                                )

    def test_charge_update_position(self, checker, publish_msg, prepare, redis_key_front, vid, redis):
        with allure.step("校验充电更新事件，上报position中 gps_time小于redis中存储的sampletime-gps time>24h，redis中数据不更新"):
            # 支持马克波罗服务测试
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            redis_key = f'{remote_vehicle_key_front}:vehicle_status:{vid}:PositionStatus'
            redis_value_before = json.loads(redis['cluster'].get(redis_key))
            nextev_message, charge_end_event_obj = publish_msg('periodical_charge_update',
                                                               sample_points=[{'position_status':{'gps_ts':redis_value_before['gps_time']-25*3600*1000},
                                                                 'vehicle_status':{
                                                                     "mileage": prepare['original_mileage'] + 1}}]
                                                                  )

            # 校验

            redis_value_after = json.loads(redis['cluster'].get(redis_key))
            assert_equal(redis_value_after, redis_value_before)


    def test_missing_some_fields(self, checker, redis_key_front, publish_msg,vid,vin):
        with allure.step("校验上报车辆数据若少字段，若redis中之前有该字段，则该字段值为原先的值"):
            # 清除redis 缓存
            # 支持马克波罗服务测试
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            redis_key = f'{remote_vehicle_key_front}:vehicle_status:{vid}:PositionStatus'
            checker.redis.delete(redis_key)
            # 构造全部数据并上报消息
            nextev_message, instant_status_resp_obj_old = publish_msg('periodical_charge_update')
            longitude_old = json.loads(checker.redis.get(redis_key))['longitude']
            # 构造没有经纬度的数据并上报
            clear_fields = ['sample_points[0].position_status.longitude']
            nextev_message, instant_status_resp_obj_new = publish_msg('periodical_charge_update',clear_fields=clear_fields)
            # 校验
            longitude_new = json.loads(checker.redis.get(redis_key))['longitude']
            assert_equal(longitude_old,longitude_new)