#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2020/07/15 22:19
@contact: hongzhen.bi@nio.com
@description: 行程补偿逻辑

当用户车辆行程数据上报丢失时，定时任务执行形成数据补偿

1.  消费 periodical_journey_update 事件， 在redis里记录此次journey的第一条记录和最后一条记录
    (key:  remote_vehicle_test:journey_first  remote_vehicle_test:journey_last)，
    当journey_start/journey_end 丢失数据时候(缺soc/dump_energy等 vehicle_journey_history需要的数据)，用redis的数据补
    redis缓存数据的ttl为72小时

2.  vehicle_journey_history 新增行程avg_speed, max_speed, min_speed, 此数据来源于 periodical_journey_update msg 中的DrivingData数据

3.  当丢失journey_start 或者journey_end时候，利用redis中存的first/last数据，来补偿此次丢失,
    这个补偿是在每天的 02:10 和 14:10 补偿， 补偿 vehicle_journey_history create_time 在(12h, 24h) 之间的数据丢失情况。

4.  补偿行程开始及行程结束时，期望改旅程开关状态为旅程结束前最近用户设置的行程开关状态

5.  上报行程结束失败后，使用journey_update数据补偿缺失字段后，is_end仍为0（is_end仅通过journey_end_event设置为0）
"""

import json
import time
import allure

from utils import message_formator
from utils.assertions import assert_equal


class TestFillFieldFromRedisJourney(object):
    def test_journey_update_redis(self, env, vid, redis_key_front, checker, publish_msg_by_kafka):
        journey_id = int(time.time())
        # 清除redis 缓存
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        key_first = f'{remote_vehicle_key_front}:journey_first:{vid}:{journey_id}'
        key_last = f'{remote_vehicle_key_front}:journey_last:{vid}:{journey_id}'
        checker.redis.delete(key_first)
        checker.redis.delete(key_last)
        with allure.step("不论是否上报行程开始，还是行程结束，只要上报行程更新，redis中就会缓存该行程数据"):
            publish_msg_by_kafka('periodical_journey_update', journey_id=str(journey_id))
            assert_equal(bool(checker.redis.get(key_first)), True)
            assert_equal(bool(checker.redis.get(key_last)), True)

