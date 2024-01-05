#!/usr/bin/env python
# coding=utf-8

"""
:file: test_periodical_charge_update_mongodb.py
:author: zhiqiang.zhu
:Date: Created on 2017/1/12 下午8:01
:Description: 周期性充电消息上报，包含position_status数据，driving_data数据，vehicle_status数据，occupant_status数据，soc_status数据，
:alarm数据，driving_motor数据，extremum数据。
"""
import random
import allure
from utils.assertions import assert_equal


class TestChargeUpdateMsg(object):
    def test_periodical_charge_update(self, checker, publish_msg):
        # 构造并上报消息
        event_name = 'periodical_charge_update'
        nextev_message, obj = publish_msg(event_name)

        # 校验
        collections = ['vehicle_position']
        checker.check_mongodb_collections(obj['sample_points'][0], collections,
                                          event_name=event_name,
                                          sample_ts=obj['sample_points'][0]['sample_ts'])

    def test_invalid_position_status(self, vid, checker, publish_msg):
        event_name = 'periodical_charge_update'

        with allure.step("校验 当经度或纬度为0时，不管位置信息标识为有效还是无效，经纬度信息都不会保存到mongodb.vehicle_position"):
            original_position_in_mongodb = checker.mongodb.find('vehicle_position', {"_id": vid})[0]['location']

            position_status = random.choice([{'longitude': 110.111111, 'latitude': 0}, {'longitude': 0, 'latitude': 35.333333}])
            publish_msg(event_name,
                        sample_points=[{
                            "position_status": position_status
                        }])

            new_position_in_mongodb = checker.mongodb.find('vehicle_position', {"_id": vid})[0]['location']

            assert_equal(original_position_in_mongodb, new_position_in_mongodb)

        with allure.step("校验 当经度或纬度为null时，不管位置信息标识为有效还是无效，经纬度信息都不会保存到mongodb.vehicle_position"):
            original_position_in_mongodb = checker.mongodb.find('vehicle_position', {"_id": vid})[0]['location']

            clear_field = random.choice(['sample_points[0].position_status.longitude', 'sample_points[0].position_status.latitude'])
            publish_msg(event_name, clear_fields=[clear_field])

            new_position_in_mongodb = checker.mongodb.find('vehicle_position', {"_id": vid})[0]['location']

            assert_equal(original_position_in_mongodb, new_position_in_mongodb)

    def test_periodical_charge_update_can_msg(self,vid, mongodb, checker, publish_msg):
        """
        1、can_msg只存Cassandra，
        2、msg_id 为623的can也会存到mongodb
            来自于PE的需求，查电池容量
            https://confluence.nioint.com/pages/viewpage.action?pageId=177346139
        3、data_report的接口 /api/1/in/data/vehicle/can_msg 可以解析can信号
        4、不是所有can都会上报：https://confluence.nioint.com/display/CVS/Vehicle+Data+Collection

        该功能上线后，新的解析规则解析1216的msg_id时会报错，
        原因是该msg_id为5位，但新的解析规则是按照8位进行解析的，
        目前回滚到都使用dbc 7.4做解析
        """
        with allure.step('mongodb更新msg_id为623的信号，且如果CGW上报上来的vehl_type_dbc为ES8_7.5.4/ES6_3.0.4，TSP会使用dbc 7.5.4/dbc 3.0.4 去解析'):
            event_name = 'periodical_charge_update'
            nextev_message, obj = publish_msg(event_name, sample_points=[
                {
                    'can_msg': {
                        'can_data': [
                            {
                                'msg_id': 623,
                                'value': '0002140623101102'
                            }
                        ]
                    }
                }
            ])
            collections = ['can_msg']
            checker.check_mongodb_collections(obj['sample_points'][0], collections,
                                              event_name=event_name,
                                              sample_ts=obj['sample_points'][0]['sample_ts'])

        with allure.step('CGW上报上来的vehl_type_dbc为空（针对BL240之前），TSP会和现在一样使用dbc 7.4去解析'):
            event_name = 'periodical_charge_update'
            nextev_message, obj = publish_msg(event_name, sample_points=[
                {
                    'can_msg': {
                        'can_data': [
                            {
                                'msg_id': 623,
                                'value': '0002140623101102'
                            }
                        ]
                    }
                }
            ], clear_fields=['sample_points[0].vehicle_status.vehl_type_dbc'])

            # 校验
            collections = ['can_msg']
            checker.check_mongodb_collections(obj['sample_points'][0], collections,
                                              event_name=event_name,
                                              sample_ts=obj['sample_points'][0]['sample_ts'])

        with allure.step('如果vehl_type_dbc和上述都不符合，会使用dbc 3.0.4 去解析'):
            event_name = 'periodical_charge_update'
            nextev_message, obj = publish_msg(event_name, sample_points=[
                {
                    'vehicle_status': {'vehl_type_dbc': 'aaaa'},
                    'can_msg': {
                        'can_data': [
                            {
                                'msg_id': 623,
                                'value': '0002140623101102'
                            }
                        ]
                    }
                }
            ])

            # 校验
            collections = ['can_msg']
            checker.check_mongodb_collections(obj['sample_points'][0], collections,
                                              event_name=event_name,
                                              sample_ts=obj['sample_points'][0]['sample_ts'])
