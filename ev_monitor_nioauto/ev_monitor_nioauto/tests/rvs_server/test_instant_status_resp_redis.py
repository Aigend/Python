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
        return redis_result['mileage'] if 'mileage' in redis_result else 0

    def test_instant_status_resp_redis(self, checker, publish_msg,prepare):
        with allure.step("校验正常逻辑instant_redis情况，即全量上报后，查看redis中对应数据更新情况"):
            # 构造并上报消息
            nextev_message, instant_status_resp_obj = publish_msg('instant_status_resp', sleep_time=5, clear_fields=['sample_point.alarm_signal'],
                                                                  sample_point={'vehicle_status': {"mileage": prepare + 1},
                                                                                'can_msg': {
                                                                                    'can_data': [
                                                                                        {
                                                                                            'msg_id': 623,
                                                                                            'value': '0002140623101102'
                                                                                        }
                                                                                    ]
                                                                                }})

            # 校验
            keys = ['DoorStatus', 'PositionStatus', 'DrivingData', 'TyreStatus',
                    'OccupantStatus', 'SocStatus', 'HvacStatus',
                    'ExteriorStatus', 'LightStatus', 'ExtremumData', 'WindowStatus',
                    'DrivingMotor']
            instant_status_resp_obj['sample_point']['soc_status']['battery_pack_cap'] = 0
            checker.check_redis(instant_status_resp_obj['sample_point'], keys,
                                event_name='instant_status_resp',
                                sample_ts=instant_status_resp_obj.get('sample_point', {}).get('sample_ts'))

    def test_instant_status_soc_is_0_redis_is_0(self, vid, checker, publish_msg, prepare, redis_key_front):
        # 清除redis 缓存
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        checker.redis.delete(f'{remote_vehicle_key_front}:vehicle_status:{vid}:SocStatus')
        with allure.step("校验正常逻辑instant_redis情况，即全量上报soc=0，查看redis中对应数据更新为0"):
            nextev_message, instant_status_resp_obj = publish_msg('instant_status_resp',
                                                                  sample_point={'vehicle_status':{
                                                                      "mileage": prepare + 1},
                                                                      'soc_status': {'soc': 0}},
                                                                  clear_fields=['sample_point.can_msg', 'sample_point.alarm_signal']
                                                                  )

            # 校验
            keys = ['SocStatus']
            checker.check_redis(instant_status_resp_obj['sample_point'], keys,
                                event_name='instant_status_resp',
                                sample_ts=instant_status_resp_obj.get('sample_point', {}).get('sample_ts'))

    def test_charge_start_position(self, checker, publish_msg, prepare, redis_key_front, vid, redis):
        with allure.step("校验全量事件，上报position中 gps_time小于redis中存储的sampletime-gps time>24h，redis中数据不更新"):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            redis_key = remote_vehicle_key_front + ':vehicle_status:' + vid + ':PositionStatus'
            redis_value_before = json.loads(redis['cluster'].get(redis_key))
            nextev_message, charge_end_event_obj = publish_msg('instant_status_resp',
                                                               sample_point={'position_status':{'gps_ts':redis_value_before['gps_time']-25*3600*1000},
                                                                 'vehicle_status':{
                                                                     "mileage": prepare + 1}}
                                                                  )

            # 校验

            redis_value_after = json.loads(redis['cluster'].get(redis_key))
            assert_equal(redis_value_after, redis_value_before)



    def test_missing_some_fields(self, checker,redis_key_front, publish_msg,vid,vin):
        with allure.step("校验上报车辆数据若少字段，若redis中之前有该字段，则该字段值为原先的值"):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            # 清除redis 缓存
            # checker.redis.delete(f'{remote_vehicle_key_front}:vehicle_status:{vid}:PositionStatus')
            # 构造全部数据并上报消息
            nextev_message, instant_status_resp_obj_old = publish_msg('instant_status_resp')
            longitude_old = json.loads(checker.redis.get(f'{remote_vehicle_key_front}:vehicle_status:{vid}:PositionStatus'))['longitude']
            # 构造没有经纬度的数据并上报
            clear_fields = ['sample_point.position_status.longitude']
            nextev_message, instant_status_resp_obj_new = publish_msg('instant_status_resp',clear_fields=clear_fields)
            # 校验
            longitude_new = json.loads(checker.redis.get(f'{remote_vehicle_key_front}:vehicle_status:{vid}:PositionStatus'))['longitude']
            assert_equal(longitude_old,longitude_new)