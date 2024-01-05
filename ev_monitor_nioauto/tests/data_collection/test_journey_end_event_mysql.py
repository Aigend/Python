#!/usr/bin/env python
# coding=utf-8

"""
:file: test_journey_end_event_mysql.py
:author: zhiqiang.zhu
:Date: Created on 2016/1/11
:Description: 行程开始事件，包含position数据。
"""
import random
import allure
import pytest
from utils.assertions import assert_equal


class TestJourneyEndMsg(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    def test_journey_end_event(self, vid, prepare, checker, publish_msg):
        # 构造并上报消息
        mileage = prepare['original_mileage'] + 1

        nextev_message, journey_end_obj = publish_msg('journey_end_event',
                                                      vehicle_status={"mileage": mileage}
                                                      )

        # 校验
        tables =['status_position','status_vehicle', 'status_soc']
        checker.check_mysql_tables(journey_end_obj, tables)

    def test_journey_end_event_mysql_dont_update_mileage(self, vid, checker, prepare, publish_msg):
        # 校验当传入mileage小于Mysql中的数值时，stataus_vehicle表中mileage字段不更新
        mileage = prepare['original_mileage'] -2
        nextev_message, journey_end_obj = publish_msg('journey_end_event',
                                                      vehicle_status={"mileage": mileage}
                                                      )

        mileage_in_mysql = checker.mysql.fetch('status_vehicle', {"id": vid},['mileage'])[0]
        with allure.step("校验当传入mileage小于DB中存的值，stataus_vehicle表中mileage字段不更新"):
            assert_equal(mileage_in_mysql['mileage'], prepare['original_mileage'])

    def test_posng_valid_type(self, vid, prepare, checker, publish_msg):
        with allure.step("校验 位置信息标为无效时，只要经纬度不为0或null，status_position仍会保存位置信息"):
            mileage = prepare['original_mileage'] + 1

            nextev_message, obj = publish_msg('journey_end_event',
                                              vehicle_status={
                                                  "mileage": mileage
                                              },
                                              position_status={
                                                  "posng_valid_type": random.choice([1, 2])
                                              }
                                              )

            tables = ['status_position', 'status_vehicle', 'status_soc']
            checker.check_mysql_tables(obj, tables)

    def test_latitude_longitude_is_zero(self, vid, prepare, checker, publish_msg):


        with allure.step("校验 当经度或纬度为0时，不管位置信息标识为有效还是无效，status_position都不会保存位置信息"):
            mileage = prepare['original_mileage'] + 1

            original_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]

            position_status = random.choice([{'longitude':110.111111,'latitude':0},{'longitude':0,'latitude':35.333333}])
            nextev_message, obj = publish_msg('journey_end_event',
                                              vehicle_status={
                                                  "mileage": mileage
                                              },
                                              position_status=position_status,
                                              )

            # Check other tables will update
            tables = ['status_vehicle', 'status_soc']
            checker.check_mysql_tables(obj, tables)

            # Check position won't update
            new_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            assert_equal(original_position_status_in_mysql, new_position_status_in_mysql)

    def test_latitude_longitude_is_null(self, vid, prepare, checker, publish_msg):
        with allure.step("校验 当经度或纬度为null时，不管位置信息标识为有效还是无效，status_position都不会保存位置信息"):
            mileage = prepare['original_mileage'] + 1

            original_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]

            clear_field = random.choice(['position_status.longitude','position_status.latitude'])
            nextev_message, obj = publish_msg('journey_end_event',
                                              vehicle_status={
                                                  "mileage": mileage
                                              },
                                              clear_fields=[clear_field]
                                              )

            # Check other tables will update
            tables = ['status_vehicle', 'status_soc']
            checker.check_mysql_tables(obj, tables)

            # Check position won't update
            new_position_status_in_mysql = checker.mysql.fetch('status_position', {"id": vid})[0]
            assert_equal(original_position_status_in_mysql, new_position_status_in_mysql)

