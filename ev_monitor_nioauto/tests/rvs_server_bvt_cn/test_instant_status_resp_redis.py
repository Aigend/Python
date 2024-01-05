#!/usr/bin/env python
# coding=utf-8

"""
:author: rongyao.yang
"""
import pytest
import allure
import json
from utils.assertions import assert_equal


class TestInstantStsResp(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        key_front = checker.redis_key_front['remote_vehicle'] + ':vehicle_status:' + checker.vid
        key = key_front + ':ExteriorStatus'
        redis_result = json.loads(checker.redis.get(key))
        keys = ['PositionStatus', 'DrivingData', 'TyreStatus',
                'OccupantStatus', 'SocStatus', 'HvacStatus',
                'ExteriorStatus', 'ExtremumData', 'DrivingMotor']
        # 清除redis 缓存
        for key in keys:
            checker.redis.delete(f'{key_front}:{key}')
        return redis_result['mileage'] if 'mileage' in redis_result else 0

    def test_instant_status_resp_redis(self, checker, publish_msg, prepare):
        with allure.step("校验正常逻辑instant_redis情况，即全量上报后，查看redis中对应数据更新情况"):
            nextev_message, instant_status_resp_obj = publish_msg('instant_status_resp',
                                                                  sample_point={'vehicle_status':{
                                                                      "mileage": prepare + 1}},
                                                                  clear_fields=['sample_point.can_msg',
                                                                                'sample_point.alarm_signal'] #包含alarm_signal会触发slytherin同步redis和mysql的记录
                                                                  )

            # 校验
            keys = ['DoorStatus', 'PositionStatus', 'DrivingData', 'TyreStatus',
                    'OccupantStatus', 'SocStatus', 'HvacStatus',
                    'ExteriorStatus', 'LightStatus', 'ExtremumData', 'WindowStatus',
                    'DrivingMotor']
            checker.check_redis(instant_status_resp_obj['sample_point'], keys,
                                event_name='instant_status_resp',
                                sample_ts=instant_status_resp_obj.get('sample_point', {}).get('sample_ts'))
