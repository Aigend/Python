#!/usr/bin/env python
# coding=utf-8

import allure

from utils.assertions import assert_equal


class TestDoorStatusChangeMsg(object):
    def test_door_status_change_event_redis(self, redis, publish_msg, redis_key_front, vid):
        """
        校验data_collection处理上报事件时，会往redis里记录事件的sample_ts
        """
        # 构造并上报消息
        nextev_message, door_status_obj = publish_msg('door_change_event', sleep_time=31)
        # 校验redis
        with allure.step("验证 door_change_event 时间戳存入 redis"):
            data_collection_key_front = redis_key_front['data_collection']
            name = f'{data_collection_key_front}:{vid}'
            key = 'record_exists:status_door'
            door_status_in_redis = redis['cluster'].hash_hget(name=name, key=key)
            assert_equal(door_status_in_redis, str(door_status_obj['sample_ts']))

