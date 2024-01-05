#!/usr/bin/env python
# coding=utf-8

"""
:file: test_periodical_journey_update_redis.py
:author: yry
:Date: Created on 2019/14/24 下午8:01
:Description: 周期性充电消息上报
"""
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


