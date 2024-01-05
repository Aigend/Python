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

    def test_journey_start_position(self, publish_msg_by_kafka, prepare, redis_key_front, vid, redis):
        with allure.step("校验行程开始事件，上报position中 gps_time小于redis中存储的sampletime-gps time>24h，redis中数据不更新"):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            redis_key = remote_vehicle_key_front + ':vehicle_status:' + vid + ':PositionStatus'
            redis_value_before = json.loads(redis['cluster'].get(redis_key))
            nextev_message, charge_end_event_obj = publish_msg_by_kafka('charge_start_event',
                                                               position_status={'gps_ts':redis_value_before['gps_time']-25*3600*1000},
                                                               vehicle_status={"mileage": prepare['mileage'] + 1})

            # 校验
            redis_value_after = json.loads(redis['cluster'].get(redis_key))
            assert_equal(redis_value_after, redis_value_before)

    def test_max_mileage_redis(self, vid, checker, publish_msg_by_kafka, redis_key_front):
        with allure.step("校验上报大于200万的mileage消息后，消息中的mileage字段不能落库redis"):
            # 清除redis 缓存
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key = f'{remote_vehicle_key_front}:vehicle_status:{vid}:ExteriorStatus'
            checker.redis.delete(key)
            illegal_mileage = 2000000 + 1
            # 上报不合法的mileage信息
            publish_msg_by_kafka('journey_start_event', vehicle_status={"mileage": illegal_mileage})
            # 校验redis（mileage字段缺失，其他字段会正常落库）
            status_driving_in_redis = json.loads(checker.redis.get(key))
            assert_equal('mileage' in status_driving_in_redis, False)

    def test_ntester_None_to_False(self, vid, checker, prepare, publish_msg_by_kafka, redis_key_front):
        with allure.step("校验上报的ntester为空时，将处理为false"):
            # 清除redis 缓存
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key = f'{remote_vehicle_key_front}:vehicle_status:{vid}:ExteriorStatus'
            checker.redis.delete(key)
            # 构造并上报消息
            mileage = prepare['mileage'] + 1
            publish_msg_by_kafka('journey_start_event', vehicle_status={"mileage": mileage}, clear_fields=['vehicle_status.ntester'])
            # 校验
            status_vehicle_in_redis = json.loads(checker.redis.get(key))
            assert_equal(status_vehicle_in_redis['ntester'], False)

    def test_journey_start_event_pm25fil(self, vid, checker, publish_msg_by_kafka, prepare, redis_key_front):
        # 清除 redis 缓存
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        key_front = f'{remote_vehicle_key_front}:vehicle_status:{vid}'
        for key in ['PositionStatus', 'SocStatus', 'ExteriorStatus', 'HvacStatus']:
            checker.redis.delete(f'{key_front}:{key}')
        with allure.step("先上报周期性行程数据，使HvacStatus存在除pm25_fil以外的基础数据"):
            mileage = prepare['mileage'] + 1
            publish_msg_by_kafka('periodical_journey_update', sample_points=[{'vehicle_status': {"mileage": mileage}}],
                                 clear_fields=['sample_points[0].can_msg', 'sample_points[0].alarm_signal'])
            status_hvac_journey_update = json.loads(checker.redis.get(f'{remote_vehicle_key_front}:vehicle_status:{vid}:HvacStatus'))

        with allure.step("上报行程开始，校验PositionStatus、SocStatus、ExteriorStatus正确更新"):
            mileage = prepare['mileage'] + 2
            nextev_message, journey_start_obj = publish_msg_by_kafka('journey_start_event', vehicle_status={"mileage": mileage})
            # 校验
            keys = ['PositionStatus', 'SocStatus', 'ExteriorStatus']
            checker.check_redis(journey_start_obj, keys, event_name='journey_start_event', clear_none=True, sample_ts=journey_start_obj['sample_ts'])
        with allure.step("校验HvacStatus中的pm25_fil能够通过行程开始事件正确补充进来"):
            status_hvac_journey_start = json.loads(checker.redis.get(f'{remote_vehicle_key_front}:vehicle_status:{vid}:HvacStatus'))
            status_hvac_journey_update['pm25_fil'] = journey_start_obj['pm25_fil']
            status_hvac_journey_update['sample_time'] = int(journey_start_obj['sample_ts'] / 1000)
            assert_equal(status_hvac_journey_start, status_hvac_journey_update)
