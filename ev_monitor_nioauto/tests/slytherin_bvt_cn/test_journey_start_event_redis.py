#!/usr/bin/env python
# coding=utf-8


import allure
import pytest
from utils.assertions import assert_equal
import json

list_situation = [0, 1, 2]
case = []

for i in list_situation:
    srr = 'posng_valid_type=' + str(i)
    case.append(srr)


class TestJourneyStartMsg(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, env, mysql,vid):

        original_mileage_in_mysql = mysql['rvs'].fetch('status_vehicle',
                                                       {"id": vid
                                                        },
                                                       ['mileage']
                                                       )[0]
        return original_mileage_in_mysql

    @pytest.mark.parametrize("posng_valid_type", list_situation, ids=case)
    def test_journey_start_event_redis(self, vid, checker, publish_msg_by_kafka, prepare, posng_valid_type, redis_key_front):
        keys = ['PositionStatus', 'SocStatus', 'ExteriorStatus']
        # 清除redis 缓存
        # 支持马克波罗服务测试
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        key_front = f'{remote_vehicle_key_front}:vehicle_status:{vid}'
        for key in keys:
            checker.redis.delete('{key_front}:{key}'.format(key_front=key_front, key=key))
        # 构造并上报消息
        mileage = prepare['mileage'] + 1
        nextev_message, journey_start_obj = publish_msg_by_kafka('journey_start_event', vehicle_status={"mileage": mileage},
                                                                                      position_status={"posng_valid_type": posng_valid_type})
        # 校验
        checker.check_redis(journey_start_obj, keys, event_name='journey_start_event', clear_none=True,sample_ts=journey_start_obj['sample_ts'])

