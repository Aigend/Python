#!/usr/bin/env python
# coding=utf-8

"""
:file: test_charge_start_event_mysql.py
:author: zhiqiang.zhu
:Date: Created on 2016/11/11
:Description: 充电开始事件，包含电池数据
"""
import random
import allure

from utils.assertions import assert_equal


class TestChargeStartMsg(object):
    def test_charge_start_event(self, publish_msg, checker):
        # 构造并上报消息
        event_name = 'charge_start_event'
        nextev_message, obj = publish_msg(event_name)

        # 校验
        collections = ['vehicle_position']
        checker.check_mongodb_collections(obj, collections, event_name=event_name, sample_ts=obj['sample_ts'])

    def test_invalid_position_status(self, vid,  publish_msg, checker):
        event_name = 'charge_start_event'

        with allure.step("校验 当经度或纬度为0时，不管位置信息标识为有效还是无效，经纬度信息都不会保存到mongodb.vehicle_position"):
            original_position_in_mongodb = checker.mongodb.find('vehicle_position', {"_id": vid})[0]['location']

            position_status = random.choice([{'longitude':110.111111,'latitude':0},{'longitude':0,'latitude':35.333333}])
            publish_msg(event_name, position_status=position_status)

            new_position_in_mongodb = checker.mongodb.find('vehicle_position', {"_id": vid})[0]['location']

            assert_equal(original_position_in_mongodb, new_position_in_mongodb)

        with allure.step("校验 当经度或纬度为null时，不管位置信息标识为有效还是无效，经纬度信息都不会保存到mongodb.vehicle_position"):
            original_position_in_mongodb = checker.mongodb.find('vehicle_position', {"_id": vid})[0]['location']

            clear_field = random.choice(['position_status.longitude','position_status.latitude'])
            publish_msg(event_name, clear_fields=[clear_field])

            new_position_in_mongodb = checker.mongodb.find('vehicle_position', {"_id": vid})[0]['location']

            assert_equal(original_position_in_mongodb, new_position_in_mongodb)



