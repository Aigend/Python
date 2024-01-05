#!/usr/bin/env python
# coding=utf-8

"""
Prod环境自动注册EVM上报的车辆


cases:
        验证当vehicle_profile中不存在的vid车辆上报start/end事件会同时新插入到vehicle_profile表里
        验证插入kafka的数据只包含vehicleId／vin／iccid三者中的一个时，vehicle_profile不会记录数据
        验证插入kafka的数据只包含vehicleId和vin时，vehicle_profile插入一条数据，补全vehicle_id和vin，iccId为空
        验证插入kafka的数据包含上一条的vehicleId／vin，并带着iccId，vehicle_profile之前的数据补全iccId
        验证插入kafka的数据包含vehicleId／vin／iccId时，vehicle_profile插入一条数据，补全vehicle_id／vin／iccId
        验证插入kafka的数据包含的vehicleId／vin和上一条相同，但iccId不同时，vehicle_profile之前数据不会更新
        验证如果从红龙(RD管理证书的服务)获取vin-vid映射关系失败，则认为不可以注册,存 notice illegal vehicle表
        验证上报消息包含车机平台数据，会记录在vehicle_profile的平台字段
"""
import time

import pytest
import allure
import json
from utils.assertions import assert_equal


class TestAutoRegister(object):
    @pytest.fixture(scope="function", autouse=False)
    def set_iccid_null(self, checker, env):
        vin = env['vehicles']['has_not_iccid']['vin']
        vid = env['vehicles']['has_not_iccid']['vehicle_id']
        with allure.step('在vehicle_profile表中更新某条车辆纪录，将iccid设置为null'):
            checker.mysql.update('vehicle_profile',
                                 where_model={'id': vid},
                                 fields_with_data={
                                     'iccid': None
                                 })

        # Sleep 6 mins to wait data collection picking the mysql new iccid value
        time.sleep(60 * 6)
        return {"vin": vin, "vid": vid}

    @pytest.mark.longtime
    @pytest.mark.skip('longtime')
    def test_iccid(self, checker, publish_msg_by_kafka, prepare, api, set_iccid_null):
        """
        校验mysql的vehicle_porfile表中iccid为空时，上报的数据会填补iccid的值，但如果iccid已经有值，上报的数据不会更新iccid的值
        """
        vin = set_iccid_null['vin']
        vid = set_iccid_null['vid']
        event_name = 'charge_start_event'

        with allure.step('第一次上报，校验vehicle_profile表的iccid会更新'):
            mileage = prepare['original_mileage'] + 1
            nextev_message, first_obj = publish_msg_by_kafka(event_name,
                                                             vin=vin,
                                                             vid=vid,
                                                             vehicle_status={"mileage": mileage},
                                                             )
            first_iccid_myql = checker.mysql.fetch('vehicle_profile',
                                                   {"id": vid},
                                                   fields=['iccid']
                                                   )[0]['iccid']
            assert_equal(first_iccid_myql, first_obj['icc_id'])

        with allure.step('第二次上报，校验vehicle_profile表的iccid不再更新'):
            mileage = prepare['original_mileage'] + 2
            nextev_message, second_obj = publish_msg_by_kafka(event_name,
                                                              vin=vin,
                                                              vid=vid,
                                                              icc_id='III' + vin,
                                                              vehicle_status={"mileage": mileage},
                                                              )
            second_iccid_mysql = checker.mysql.fetch('vehicle_profile',
                                                     {"id": vid},
                                                     fields=['iccid']
                                                     )[0]['iccid']
            assert second_iccid_mysql != second_obj['icc_id']
            assert_equal(first_iccid_myql, second_iccid_mysql)

    @pytest.mark.skip('manual')
    def test_other(self):
        """
        验证插入kafka的数据只包含vehicleId／vin／iccid三者中的一个时，vehicle_profile不会记录数据
        验证插入kafka的数据只包含vehicleId和vin时，vehicle_profile插入一条数据，补全vehicle_id和vin，iccId为空
        验证插入kafka的数据包含vehicleId／vin／iccId时，vehicle_profile插入一条数据，补全vehicle_id／vin／iccId
        """
        pass

    @pytest.mark.skip('manual')
    def test_update_vehicle_profile(self):
        # 校验当vehicle_profile中不存在的vid车辆上报start/end事件会同时新插入到vehicle_profile表里
        """
        必须要有noticeType字段，类似于{"noticeType":"NonExistVehicle","timestamp":1565033982920,"staticInfo":{"vehicleId":"866c718a4b934275ab22d974637041b3","vin":"EVMzhuzhiqiang001","iccId":"ICCEVMzhuzhiqiang001"}}
        该字段在message数据包里没有，数据库里也没有
        :return:
        """
        pass

    @pytest.mark.test
    def test_sync_platform_to_vehicle_profile(self, publish_msg_by_kafka, checker):
        with allure.step("选择vehicle_profile的车辆测试"):
            vehicle = checker.mysql.fetch_one('vehicle_profile', {'is_activated': 0, 'vin like': 'SQETEST%'})
            checker.mysql.delete('vehicle_profile', {'id': vehicle['id']})

        with allure.step("构造并上报消息"):
            _, obj = publish_msg_by_kafka('charge_start_event', platform_type=1, vid=vehicle['id'],
                                          vin=vehicle['vin'])

        with allure.step('校验mysql存储车辆信息及平台'):
            vehicle_new = checker.mysql.fetch_one('vehicle_profile', {'id': vehicle['id']})
            assert vehicle_new['id'] == vehicle['id']
            assert vehicle_new['vin'] == vehicle['vin']
            assert vehicle_new['iccid'] == f'ICC{vehicle["vin"]}'
            assert vehicle_new['platform'] == 'NT2.0'
