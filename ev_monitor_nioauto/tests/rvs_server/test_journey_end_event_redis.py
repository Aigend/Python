#!/usr/bin/env python
# coding=utf-8


import pytest


class TestJourneyEndMsg(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, mysql):
        original_mileage_in_mysql = mysql['rvs'].fetch('status_vehicle',
                                                       {"id": vid
                                                        },
                                                       ['mileage']
                                                       )[0]
        return original_mileage_in_mysql

    def test_journey_end_event_redis(self, vid, checker, publish_msg_by_kafka, prepare, redis_key_front):
        # 清除redis 缓存
        keys = ['PositionStatus', 'SocStatus', 'ExteriorStatus']
        # 支持马克波罗服务测试
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        key_front = f'{remote_vehicle_key_front}:vehicle_status:{vid}'
        for key in keys:
            checker.redis.delete('{key_front}:{key}'.format(key_front=key_front, key=key))
        # 构造并上报消息
        mileage = prepare['mileage'] + 1
        nextev_message, journey_end_obj = publish_msg_by_kafka('journey_end_event',vehicle_status={"mileage": mileage})
        # 校验
        checker.check_redis(journey_end_obj, keys, event_name='journey_end_event', clear_none=True, sample_ts=journey_end_obj['sample_ts'])