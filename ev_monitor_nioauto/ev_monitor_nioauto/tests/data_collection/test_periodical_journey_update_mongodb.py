#!/usr/bin/env python
# coding=utf-8

"""
:file: test_periodical_journey_update_mongodb.py
:author: zhiqiang.zhu
:Date: Created on 2017/1/12 下午8:01
:Description: 周期性充电消息上报，包含position_status数据，driving_data数据，vehicle_status数据，occupant_status数据，soc_status数据，
:alarm数据，driving_motor数据，extremum数据，btry_packs数据，hvac_status数据，signal_status数据，tyre_status数据。
"""
import random
import allure

from utils.assertions import assert_equal


class TestJouneyUpdateMsg(object):
    def test_periodical_journey_update(self, checker, publish_msg):
        # 构造并上报消息
        event_name = 'periodical_journey_update'
        nextev_message, obj = publish_msg(event_name)

        # 校验
        collections = ['vehicle_position']   # 停止更新mongoDB can_msg
        checker.check_mongodb_collections(obj['sample_points'][0], collections,
                                          event_name=event_name,
                                          sample_ts = obj['sample_points'][0]['sample_ts'])



    def test_invalid_position_status(self, vid, checker, publish_msg):
        event_name = 'periodical_journey_update'

        with allure.step("校验 当经度或纬度为0时，不管位置信息标识为有效还是无效，经纬度信息都不会保存到mongodb.vehicle_position"):
            original_position_in_mongodb = checker.mongodb.find('vehicle_position', {"_id": vid})[0]['location']

            position_status = random.choice([{'longitude':110.111111,'latitude':0},{'longitude':0,'latitude':35.333333}])
            publish_msg(event_name,
                        sample_points=[{
                            "position_status": position_status
                        }])

            new_position_in_mongodb = checker.mongodb.find('vehicle_position', {"_id": vid})[0]['location']

            assert_equal(original_position_in_mongodb, new_position_in_mongodb)

        with allure.step("校验 当经度或纬度为null时，不管位置信息标识为有效还是无效，经纬度信息都不会保存到mongodb.vehicle_position"):
            original_position_in_mongodb = checker.mongodb.find('vehicle_position', {"_id": vid})[0]['location']

            clear_field = random.choice(['sample_points[0].position_status.longitude','sample_points[0].position_status.latitude'])
            publish_msg(event_name, clear_fields=[clear_field])

            new_position_in_mongodb = checker.mongodb.find('vehicle_position', {"_id": vid})[0]['location']

            assert_equal(original_position_in_mongodb, new_position_in_mongodb)



