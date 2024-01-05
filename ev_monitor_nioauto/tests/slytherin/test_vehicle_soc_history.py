#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2020/07/16 11:59
@contact: hongzhen.bi@nio.com
@description: 处理充电开始，充电中，充电结束事件，将数据存入vehicle_soc_history
"""
import json
import time

import allure
import pytest

from utils.assertions import assert_equal
from utils.httptool import request
from utils.logger import logger
from utils.time_parse import timestamp_to_utc_strtime
from utils.coordTransform import gcj02_to_wgs84
from utils.http_client import TSPRequest as hreq


class TestVehiSocHis(object):
    def test_vehilce_soc_history_region(self, env, checker, publish_msg_by_kafka):
        """
        http://venus.nioint.com/#/detailWorkflow/wf-20211101171107-tB
        slytherin版本1.0.172.1bdca2b之后，充电结束时，调gis接口用充电结束上报的经纬度来获取区域位置信息，填充vehicle_soc_history表中的area code字段
        gis接口：http://showdoc.nevint.com/index.php?s=/sas&page_id=13065
        :param env:
        :param checker:
        :param publish_msg_by_kafka:
        :return:
        """
        vid = env['vehicles']['vehicle_history_2']['vehicle_id']
        vin = env['vehicles']['vehicle_history_2']['vin']
        charge_id = str(int(time.time()))
        # 需要修改
        # 上报充电开始
        start_time = int(time.time() * 1000)
        publish_msg_by_kafka('charge_start_event', vid=vid, vin=vin, protobuf_v=18, sample_ts=start_time, charge_id=charge_id)
        # 上报充电update
        publish_msg_by_kafka('periodical_charge_update', vid=vid, vin=vin, protobuf_v=18, charge_id=charge_id)
        # 上报充电结束
        end_time = int(time.time() * 1000)
        nextev_message, charge_end_obj = publish_msg_by_kafka('charge_end_event', vid=vid, vin=vin, protobuf_v=18, sample_ts=end_time, charge_id=charge_id)
        with allure.step("从vehicle_soc_history表中查询充电记录"):
            vehicle_soc_history = checker.mysql.fetch_one('vehicle_soc_history',
                                                          {"vehicle_id": vid, "event_id": charge_id},
                                                          suffix=' and latitude is not NULL')

        with allure.step("调用gis接口，用经纬度来查询区域信息"):
            inputs = {
                "host": env['host']['gis_in'],
                "method": "GET",
                "path": "/v2/in/map/local/rgeo",
                "params": {
                    'app_id': 10001,
                    'location': f"{charge_end_obj['position_status']['longitude']},{charge_end_obj['position_status']['latitude']}",
                    "sign": ''
                }
            }
            region_data = hreq.request(env, inputs)
            logger.info("request status is {}".format(region_data["result_code"]))
            assert_equal(vehicle_soc_history['area_code'], region_data['data']['area_code'])

    def test_vehicle_soc_history(self, env, vid, checker, publish_msg_by_kafka):
        """
        http://venus.nioint.com/#/detailWorkflow/wf-20211101171107-tB
        slytherin版本1.0.172.1bdca2b之后，充电结束时，调gis接口用充电结束上报的经纬度来获取区域位置信息，填充vehicle_soc_history表中的area code字段
        如果充电结束未上报经纬度或经纬度非法，则调用data report接口来替代。
        :param env:
        :param vid:
        :param checker:
        :param publish_msg_by_kafka:
        :return:
        """
        charge_id = str(int(time.time()))
        # 需要修改
        # 上报充电开始
        start_time = int(time.time() * 1000)
        publish_msg_by_kafka('charge_start_event', sample_ts=start_time, charge_id=charge_id, position_status={'longitude': 0,
                                                                                                               'latitude': 0})
        # 上报充电update
        publish_msg_by_kafka('periodical_charge_update', charge_id=charge_id, sample_points=[{'position_status': {'longitude': 0,
                                                                                                                  'latitude': 0}}])
        # 上报充电结束
        end_time = int(time.time() * 1000)
        publish_msg_by_kafka('charge_end_event', sample_ts=end_time, charge_id=charge_id, position_status={'longitude': 0,
                                                                                                           'latitude': 0})
        time.sleep(5)
        with allure.step("从vehicle_soc_history表中查询充电记录"):
            vehicle_soc_history = checker.mysql.fetch_one('vehicle_soc_history',
                                                          {"vehicle_id": vid, "event_id": charge_id},
                                                          suffix=' and latitude is not NULL')

        with allure.step("若充电开始/结束位置无效且update数据无效则调用data_report接口补充位置数据"):
            # 校验调用接口补充开始位置数据
            inputs = {
                "host": env['host']['tsp_in'],
                "method": "GET",
                "path": f"/api/1/in/data/vehicle/{vid}/journey/track/newest",
                "params": {
                    'app_id': 10001,
                    'inquire_time': start_time // 1000,
                    "hash_type": "md5",
                    "sign": ''
                },
                "timeout": 5.0
            }
            start_data = hreq.request(env, inputs)
            logger.info("request status is {}".format(start_data["result_code"]))
            assert_equal(vehicle_soc_history['longitude'], start_data['data']['track'][0]['longitude'])
            assert_equal(vehicle_soc_history['latitude'], start_data['data']['track'][0]['latitude'])

        with allure.step("调用gis接口，用经纬度来查询区域信息"):
            inputs = {
                "host": env['host']['gis_in'],
                "method": "GET",
                "path": "/v2/in/map/local/rgeo",
                "params": {
                    'app_id': 10001,
                    'location': f"{vehicle_soc_history['longitude']},{vehicle_soc_history['latitude']}",
                    "sign": ''
                },
            }
            region_data = hreq.request(env, inputs)
            logger.info("request status is {}".format(region_data["result_code"]))
            assert_equal(vehicle_soc_history['area_code'], region_data['data']['area_code'])

    @pytest.mark.marcopolo_skip
    def test_charge_pile(self, env, vid, publish_msg_by_kafka, checker):
        # 马克波罗服务需要跳过@pytest.mark.skip('marcopolo gis')
        """
        充电结束上报成功，会以充电结束时的经纬度通过gis拿到最多10条（若有数据）充电桩数据存入vehicle_soc_history
        搜索半径为200米，没有数据返回则该字段为空
        接口文档：http://showdoc.nevint.com/index.php?s=/sas&page_id=3373
        """
        longitude_gcj02 = 116.465014
        latitude_gcj02 = 40.020800
        longitude, latitude = gcj02_to_wgs84(longitude_gcj02, latitude_gcj02)
        # 上报充电结束事件
        charge_id = time.strftime("%Y%m%d%M%S", time.localtime())
        publish_msg_by_kafka('charge_end_event', charge_id=charge_id, position_status={'longitude': longitude, 'latitude': latitude})

        with allure.step("调用gis接口，验证charge_pile字段存储正确"):
            inputs = {
                "host": env['host']['gis_in'],
                "method": "GET",
                "path": "/v1/in/resource/power/around",
                "params": {
                    'app_id': 10001,
                    'distance': 200,
                    'latitude': latitude_gcj02,
                    'longitude': longitude_gcj02,
                    'user_id': env['vehicles']['normal']['account_id'],
                    'cs_opening_mode': 'all_time',  # 包含在营业时间和不在营业时间的桩群
                    'resource_types': 'CS',  # CS代表充电桩
                    'with_merge': False,
                    'limit': 10,
                    'attributes': "name,id,address,location",
                    "hash_type": "md5",
                    "sign": ''
                },
                "timeout": 5.0
            }
            result = hreq.request(env, inputs)
            logger.info("request status is {}".format(result["result_code"]))
            time.sleep(5)
            charge_end_mysql = checker.mysql.fetch('vehicle_soc_history',
                                                   {"vehicle_id": vid},
                                                   order_by='update_time desc limit 1')[0]
            charge_pile = json.loads(charge_end_mysql['charge_pile'])
            if result['data']:
                for itme in result['data']:
                    location = itme.pop('location').split(',')
                    itme['longitude'] = float(location[0])
                    itme['latitude'] = float(location[1])
            assert_equal(charge_pile, result['data'])

    @pytest.mark.marcopolo_skip
    def test_charge_pile_with_invalid_charge_end(self, env, cmdopt, vid, publish_msg_by_kafka, checker):
        # 马克波罗服务需要跳过@pytest.mark.skip('marcopolo gis')
        """
        充电结束上报成功，但经纬度为无效数据，会以最后一条charge_update的非零经纬度（不论是否有效）补充并且通过gis拿到最多10条充电桩数据
        """
        longitude_gcj02 = 116.465014
        latitude_gcj02 = 40.020800
        longitude, latitude = gcj02_to_wgs84(longitude_gcj02, latitude_gcj02)

        charge_id = str(int(time.time()))
        # 上报充电开始
        publish_msg_by_kafka('charge_start_event', charge_id=charge_id, position_status={'longitude': 0, 'latitude': 0})
        # 上报充电update
        publish_msg_by_kafka('periodical_charge_update', charge_id=charge_id,
                             sample_points=[
                                 {
                                     'position_status':
                                         {'longitude': longitude,
                                          'latitude': latitude}
                                 }
                             ])
        # 上报充电结束
        publish_msg_by_kafka('charge_end_event', charge_id=charge_id, position_status={'longitude': 0, 'latitude': 0})

        with allure.step("调用gis接口，验证charge_pile字段存储正确"):
            inputs = {
                "host": env['host']['gis_in'],
                "method": "GET",
                "path": "/v1/in/resource/power/around",
                "params": {
                    'app_id': 10001,
                    'distance': 200,
                    'latitude': latitude_gcj02,
                    'longitude': longitude_gcj02,
                    'user_id': env['vehicles']['normal']['account_id'],
                    'cs_opening_mode': 'all_time',  # 包含在营业时间和不在营业时间的桩群
                    'resource_types': 'CS',  # CS代表充电桩
                    'with_merge': False,
                    'limit': 10,
                    'attributes': "name,id,address,location",
                    "hash_type": "md5",
                    "sign": ''
                },
                "timeout": 5.0
            }
            result = hreq.request(env, inputs)
            # params = {
            #     'app_id': 10001,
            #     'distance': 200,
            #     'latitude': latitude_gcj02,
            #     'longitude': longitude_gcj02,
            #     'user_id': env['vehicles']['normal']['account_id'],
            #     'cs_opening_mode': 'all_time',  # 包含在营业时间和不在营业时间的桩群
            #     'resource_types': 'CS',  # CS代表充电桩
            #     'with_merge': False,
            #     'limit': 10,
            #     'attributes': "name,id,address,location",
            #     "hash_type": "md5"
            # }
            # cmdopt = 'staging' if cmdopt == 'stg' else cmdopt
            # # 马克波罗服务修改地址
            # host_gis_in = env['host']['gis_in']
            # result = request('GET', url=f"{host_gis_in}/v1/in/resource/power/around", params=params, timeout=5.0).json()
            logger.info("request status is {}".format(result["result_code"]))

            charge_end_mysql = checker.mysql.fetch('vehicle_soc_history',
                                                   {"vehicle_id": vid},
                                                   order_by='update_time desc')[0]
            charge_pile = json.loads(charge_end_mysql['charge_pile'])
            if result['data']:
                for itme in result['data']:
                    location = itme.pop('location').split(',')
                    itme['longitude'] = float(location[0])
                    itme['latitude'] = float(location[1])
            assert_equal(charge_pile, result['data'])
