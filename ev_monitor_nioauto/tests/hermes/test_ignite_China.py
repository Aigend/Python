#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2020/12/15 11:52
@contact: hongzhen.bi@nio.com
@description: 点亮中国

找GIS要来了四个兴趣点坐标以做测试用：
    成都杜甫草堂博物馆 104.02742,30.55691
    武侯祠博物馆 104.048126,30.646055
    上海海洋水族馆 121.500092,31.24102
    三里屯太古里 116.454315,39.93494
"""
import json
import random
import time

import allure
import pytest

from utils.assertions import assert_equal


class TestIgniteChina(object):
    @pytest.fixture(scope='function', autouse=True)
    def prepare(self, cmdopt, vid, redis, publish_msg_by_kafka, kafka):
        with allure.step("如果两次上报的兴趣点一样，则不会推送kafka，所以先清空redis"):
            key = f"hermes_{cmdopt}:ignite:{vid}"
            redis['cluster'].delete(key)

        kafka['comn'].set_offset_to_end(kafka['topics']['ignite'])

        with allure.step("内存数据每1分钟清一次，所以先报几次，使内存中有记录"):
            for i in range(3):
                publish_msg_by_kafka('periodical_journey_update',
                                     sample_points=[
                                         {
                                             "vehicle_status": {
                                                 "mileage": 1,  # mileage>0
                                                 "soc": random.randint(2, 200) * 0.5,  # soc >0
                                                 "vehl_state": 1,  # 只在驾驶过程中检测点亮中国
                                             },
                                             "position_status": {
                                                 "longitude": 121.500092,  # 上海海洋水族馆
                                                 "latitude": 31.24102,
                                                 "posng_valid_type": 0  # posng_valid_type=0
                                             }
                                         }
                                     ])

    def test_ignite_China(self, cmdopt, vid, publish_msg_by_kafka, redis, kafka):
        publish_msg_by_kafka('periodical_journey_update',
                             sample_points=[
                                 {
                                     "vehicle_status": {
                                         "mileage": 1,  # mileage>0
                                         "soc": random.randint(2, 200) * 0.5,  # soc >0
                                         "vehl_state": 1,   # 只在驾驶过程中检测点亮中国
                                     },
                                     "position_status": {
                                         "longitude": 121.500092,   # 上海海洋水族馆
                                         "latitude": 31.24102,
                                         "posng_valid_type": 0  # posng_valid_type=0
                                     }
                                 }
                             ], sleep_time=3)

        with allure.step("校验推送Kafka"):
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['ignite'], timeout=20):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if vid == kafka_msg['data']['vehicle_id']:
                    is_found = True
                    break
            assert_equal(True, is_found)

        with allure.step("校验存入redis"):
            # time.sleep(3)
            ignite_redis = redis['cluster'].get(f"hermes_{cmdopt}:ignite:{vid}")
            assert ignite_redis is not None
