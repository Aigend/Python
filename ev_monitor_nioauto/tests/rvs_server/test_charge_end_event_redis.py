#!/usr/bin/env python
# coding=utf-8

"""
:author: rongyao.yang
"""
import time

import pytest
import allure
import json
from utils.assertions import assert_equal


class TestChargeEndMsg(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    @pytest.mark.marcopolo_skip
    def test_charge_end_event_status_redis(self, vid, checker, publish_msg, prepare, redis_key_front):
        # TODO 马克波罗服务需跳过@pytest.mark.skip('marcopolo app server')
        """
        车辆处于维修模式，charge_push的redis不会落库。
        应确保上报的ntester=false，且mysql中的维修工单vehicle_repair_order表的order_status_code为10。
        """
        # 清除redis 缓存
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        for key in ['PositionStatus', 'SocStatus', 'ExteriorStatus']:
            checker.redis.delete(f'{remote_vehicle_key_front}:vehicle_status:{vid}:{key}')

        # 构造并上报消息
        charge_id = time.strftime("%Y%m%d%M%S", time.localtime())
        nextev_message, charge_end_obj = publish_msg('charge_end_event', charge_id=charge_id, vehicle_status={"mileage": prepare['original_mileage']})
        # 校验
        keys = ['PositionStatus', 'SocStatus', 'ExteriorStatus', f'charge_push_end.{charge_id}']
        checker.check_redis(charge_end_obj, keys,
                            event_name='charge_end_event',
                            clear_none=True,
                            sample_ts=charge_end_obj['sample_ts'])

    def test_charge_end_soc_is_0_redis_is_0(self, checker, publish_msg, prepare):
        with allure.step("校验充电开始事件，即上报soc=0，查看redis中对应数据更新为0"):
            nextev_message, charge_end_event_obj = publish_msg('charge_end_event',
                                                               soc_status={'soc': 0},
                                                               vehicle_status={
                                                                   "mileage": prepare['original_mileage'] + 1}
                                                               )

            # 校验
            keys = ['SocStatus']
            checker.check_redis(charge_end_event_obj, keys, event_name='charge_end_event', clear_none=True,
                                sample_ts=charge_end_event_obj['sample_ts'])

    def test_charge_end_position(self, checker, publish_msg, prepare, redis_key_front, vid, redis):
        with allure.step("校验充电结束事件，上报position中 gps_time小于redis中存储的sampletime-gps time>24h，redis中数据不更新"):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            redis_key = f'{remote_vehicle_key_front}:vehicle_status:{vid}:PositionStatus'
            redis_value_before = json.loads(redis['cluster'].get(redis_key))
            nextev_message, charge_end_event_obj = publish_msg('charge_end_event',
                                                               position_status={'gps_ts': redis_value_before[
                                                                                              'gps_time'] - 25 * 3600 * 1000},
                                                               vehicle_status={
                                                                   "mileage": prepare['original_mileage'] + 1}
                                                               )
            # 校验
            redis_value_after = json.loads(redis['cluster'].get(redis_key))
            assert_equal(redis_value_after, redis_value_before)
