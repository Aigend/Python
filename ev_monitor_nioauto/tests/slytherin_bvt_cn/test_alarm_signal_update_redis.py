#!/usr/bin/env python
# coding=utf-8


import random
import time
import json
import pytest
import allure

from nio_messages import wti
from utils.assertions import assert_equal

index_names = [['WTI-BMS-2', 'WTI-BC-6', 'WTI-EP-15'], ['WTI-EP-17', 'WTI-EP-2', 'WTI-BMS-4'],
               ['WTI-BMS-3', 'WTI-BSD-1', 'WTI-FCTA-1'], ['WTI-FCTA-2', 'WTI-SA-1', 'WTI-BMS-8'],
               ['WTI-TPMS-28', 'WTI-TPMS-27', 'WTI-EP-31'], ['WTI-TPMS-26', 'WTI-TPMS-25', 'WTI-SCM-1']]


class TestAlarmSignalUpdate(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, mysql):
        original_mileage_in_mysql = mysql['rvs'].fetch('status_vehicle',
                                                       {"id": vid
                                                        },
                                                       ['mileage']
                                                       )[0]['mileage']

        return {'original_mileage': original_mileage_in_mysql}

    def test_wont_update_status(self, vid, checker, redis_key_front, publish_msg, prepare):
        with allure.step("校验alarm signal update事件的position等不落库到redis，因为它的数据不能保证正确性"):
            # 支持staging环境
            # cmdopt = 'staging' if cmdopt == 'stg' else cmdopt
            keys = ['PositionStatus', 'DrivingData', 'TyreStatus',
                    'OccupantStatus', 'BmsStatus', 'SocStatus', 'HvacStatus',
                    'ExteriorStatus', 'ExtremumData', 'DrivingMotor']
            # 支持马克波罗服务测试
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key_front = f'{remote_vehicle_key_front}:vehicle_status:{vid}'
            old_status = {key: checker.redis.get(f'{key_front}:{key}') for key in keys}

            # 构造并上报消息
            nextev_message, alarm_signal_update_obj = publish_msg('alarm_signal_update_event',
                                                                  sample_points={'vehicle_status': {
                                                                      "mileage": prepare['original_mileage'] + 1}},
                                                                  sleep_time=2
                                                                  )
            new_status = {key: checker.redis.get(f'{key_front}:{key}') for key in keys}
            # 校验
            assert_equal(new_status, old_status)
