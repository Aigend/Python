#!/usr/bin/env python
# coding=utf-8

"""
:file: test_instant_status_resp_mongodb.py
:author: muhan.chen
:Date: Created on 2018/5/30 下午5:18
:Description: 上报车辆的全量数据
"""
import random
import allure
import pytest

from utils.assertions import assert_equal


@allure.feature('上报车辆的全量事件')
class TestInstantStatusMsg(object):
    def test_instant_status_resp(self, checker, publish_msg):
        # 构造并上报消息
        event_name = 'instant_status_resp'
        nextev_message, obj = publish_msg(event_name)

        # 校验
        collections = ['vehicle_position']      # 停止更新mongoDB can_msg
        checker.check_mongodb_collections(obj['sample_point'], collections, event_name=event_name,
                                          sample_ts=obj['sample_point']['sample_ts'])

    def test_invalid_position_status(self, vid, checker, publish_msg):
        event_name = 'instant_status_resp'

        with allure.step("校验 当经度或纬度为0时，不管位置信息标识为有效还是无效，经纬度信息都不会保存到mongodb.vehicle_position"):
            original_position_in_mongodb = checker.mongodb.find('vehicle_position', {"_id": vid})[0]['location']

            position_status = random.choice([{'longitude':110.111111,'latitude':0},{'longitude':0,'latitude':35.333333}])
            publish_msg(event_name,
                        sample_point={
                            "position_status": position_status
                        })

            new_position_in_mongodb = checker.mongodb.find('vehicle_position', {"_id": vid})[0]['location']

            assert_equal(original_position_in_mongodb, new_position_in_mongodb)

        with allure.step("校验 当经度或纬度为null时，不管位置信息标识为有效还是无效，经纬度信息都不会保存到mongodb.vehicle_position"):
            original_position_in_mongodb = checker.mongodb.find('vehicle_position', {"_id": vid})[0]['location']

            clear_field = random.choice(['sample_point.position_status.longitude','sample_point.position_status.latitude'])
            publish_msg(event_name, clear_fields=[clear_field])

            new_position_in_mongodb = checker.mongodb.find('vehicle_position', {"_id": vid})[0]['location']

            assert_equal(original_position_in_mongodb, new_position_in_mongodb)

