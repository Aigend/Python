#!/usr/bin/env python
# coding=utf-8

"""
:file: test_periodical_journey_update_redis.py
:author: yry
:Date: Created on 2019/14/24 下午8:01
:Description: 周期性充电消息上报
"""
import time
import pytest
import allure
from utils.assertions import assert_equal
import json


class TestJourneyUpdateMsg(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, mysql):
        original_mileage_in_mysql = mysql['rvs'].fetch('status_vehicle',
                                                       {"id": vid
                                                        },
                                                       ['mileage']
                                                       )[0]['mileage']

        return {'original_mileage': original_mileage_in_mysql}

    def test_journey_update_event_status_redis(self, vid, checker, publish_msg, prepare, redis_key_front):
        with allure.step("校验正常逻辑行程更新，查看redis中对应数据更新"):
            keys = ['PositionStatus', 'DrivingData', 'TyreStatus',
                    'OccupantStatus', 'SocStatus', 'HvacStatus',
                    'ExteriorStatus', 'ExtremumData','DrivingMotor']
            # 清除redis 缓存
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key_front = f'{remote_vehicle_key_front}:vehicle_status:{vid}'
            for key in keys:
                checker.redis.delete(f'{key_front}:{key}')
            # 构造并上报消息
            nextev_message, journey_update_obj = publish_msg('periodical_journey_update', clear_fields=['sample_points[0].can_msg', 'sample_points[0].alarm_signal'],
                                                             sample_points=[{'vehicle_status':{"mileage": prepare['original_mileage'] + 1}}])
            # 校验
            checker.check_redis(journey_update_obj['sample_points'][0], keys,
                                event_name='journey_update_event',
                                clear_none=True,
                                sample_ts=journey_update_obj['sample_points'][0]['sample_ts'])

    def test_journey_update_soc_is_0_redis_is_0(self, vid, checker, publish_msg, prepare, redis_key_front):
        keys = ['PositionStatus', 'DrivingData', 'TyreStatus',
                'OccupantStatus', 'BmsStatus', 'HvacStatus',
                'ExteriorStatus', 'ExtremumData', 'DrivingMotor']
        # 清除redis 缓存
        # 支持马克波罗服务测试
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        key_front = f'{remote_vehicle_key_front}:vehicle_status:{vid}'
        for key in keys:
            checker.redis.delete(f'{key_front}:{key}')

        with allure.step("校验正常充电更新情况，即全量上报soc=0，查看redis中对应数据更新为0"):
            # 构造并上报消息
            nextev_message, journey_update_obj = publish_msg('periodical_journey_update',sample_points=[{'vehicle_status':{
                                                                      "mileage": prepare['original_mileage'] + 1},
                                                                        'soc_status': {'soc': 0}}],
                                                             clear_fields=['sample_points[0].can_msg', 'sample_points[0].alarm_signal']
                                                                  )

            # 校验
            keys = ['SocStatus']
            checker.check_redis(journey_update_obj['sample_points'][0], keys, event_name='journey_update_event',
                                clear_none=True,
                                sample_ts=journey_update_obj['sample_points'][0]['sample_ts'])

    def test_journey_update_without_speed_key(self, vid, checker, publish_msg, prepare, redis_key_front):
        with allure.step("校验正常逻辑行程更新但没有上报speed（min max avg），查看redis中对应数据更新"):
            keys = ['PositionStatus', 'DrivingData', 'TyreStatus',
                    'OccupantStatus', 'BmsStatus', 'HvacStatus',
                    'ExteriorStatus', 'ExtremumData', 'DrivingMotor']
            # 清除redis 缓存
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key_front = f'{remote_vehicle_key_front}:vehicle_status:{vid}'
            for key in keys:
                checker.redis.delete(f'{key_front}:{key}')
            with allure.step("校验正常充电更新情况，即全量上报soc=0，查看redis中对应数据更新为0"):
                # 构造并上报消息
                clear_fields = ['sample_points[0].driving_data.max_speed',
                                'sample_points[0].driving_data.min_speed',
                                'sample_points[0].driving_data.average_speed',
                                'sample_points[0].vehicle_status.speed']
                nextev_message, journey_update_obj = publish_msg('periodical_journey_update',sample_points=[{'vehicle_status':{
                                                                          "mileage": prepare['original_mileage'] + 1},
                                                                            }],
                                                                 clear_fields=clear_fields
                                                                      )

                # 校验
                keys = ['DrivingData','ExteriorStatus']
                checker.check_redis(journey_update_obj['sample_points'][0], keys, event_name='charge_update_event',
                                    clear_none=True,
                                    sample_ts=journey_update_obj['sample_points'][0]['sample_ts'])

    def test_journey_update_position(self, checker, publish_msg, prepare, redis_key_front, vid, redis):
        with allure.step("校验带有position status字段的事件（charge start/update/end, journey start/update/end, instant），上报position中 gps_time小于redis中存储的sample_ts-gps_ts>24h,redis中数据不更新"):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            redis_key = f'{remote_vehicle_key_front}:vehicle_status:{vid}:PositionStatus'
            redis_value_before = json.loads(redis['cluster'].get(redis_key))
            nextev_message, charge_end_event_obj = publish_msg('periodical_journey_update',
                                                               sample_points=[{'position_status':{'gps_ts':redis_value_before['gps_time']-25*3600*1000},
                                                                 'vehicle_status':{
                                                                     "mileage": prepare['original_mileage'] + 1}}]
                                                                  )

            # 校验

            redis_value_after = json.loads(redis['cluster'].get(redis_key))
            assert_equal(redis_value_after, redis_value_before)

    @pytest.mark.parametrize("event_name", ['periodical_charge_update', 'periodical_journey_update'])
    def test_null_driving_motor(self, checker, publish_msg, prepare, redis_key_front, vid, redis, event_name):
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        with allure.step("校验行程更新事件，没有上报driving_motor时，redis中数据不更新"):
            redis_key = f'{remote_vehicle_key_front}:vehicle_status:{vid}:DrivingMotor'
            redis_value_before = json.loads(redis['cluster'].get(redis_key))
            nextev_message, journey_update_obj = publish_msg(event_name,
                                                             sample_points=[{'vehicle_status': {"mileage": prepare['original_mileage'] + 1}}],
                                                             clear_fields=["sample_points[0].driving_motor"])

            # 校验
            redis_value_after = json.loads(redis['cluster'].get(redis_key))
            assert_equal(redis_value_after, redis_value_before)

    @pytest.mark.parametrize("event_name", ['periodical_charge_update','periodical_journey_update'])
    def test_mileage_exceed_max(self,redis_key_front,redis,publish_msg,vid,event_name):
        """vehicle_status写redis时过滤里程小于16777215(0xFFFFFF)，如果redis里原来mileage有值则保留原值，没有值则不存储mileage字段"""
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        with allure.step("校验写redis的mileage时不会落库大于16777215(0xFFFFFF)的值"):
            redis_key = f'{remote_vehicle_key_front}:vehicle_status:{vid}:ExteriorStatus'
            redis['cluster'].delete(redis_key)
            nextev_message, journey_update_obj = publish_msg(event_name,
                                                             sample_points=[{'vehicle_status': {"mileage": 167772151}}],
                                                             clear_fields=["sample_points[0].driving_motor"])

            # 校验
            redis_value_after = redis['cluster'].get(redis_key)
            assert_equal('mileage' not in redis_value_after, True)

