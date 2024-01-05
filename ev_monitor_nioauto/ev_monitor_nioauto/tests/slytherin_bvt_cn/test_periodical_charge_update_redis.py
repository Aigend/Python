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
                            'value': b'\x00\x02\x14\xa6\x23\x10\x11\x02'
                        },
                        {
                            'msg_id': 537,
                            'value': b'\xff\xff\xff\xff\xff\xff\xff\xff'
                        }
                    ]
                }
            }], clear_fields=['sample_points[0].alarm_signal'])

            # 校验
            charge_update_obj['sample_points'][0]['soc_status']['chrg_req'] = 7
            charge_update_obj['sample_points'][0]['soc_status']['battery_pack_cap'] = 10
            checker.check_redis(charge_update_obj['sample_points'][0], keys,
                                event_name='charge_update_event',
                                clear_none=True,
                                sample_ts=charge_update_obj['sample_points'][0]['sample_ts'])
