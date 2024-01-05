#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2020/06/16 13:33
@contact: hongzhen.bi@nio.com
@description: 充电结束
"""
import allure
from utils.assertions import assert_equal
from utils.httptool import request
import time
import pytest

from utils.logger import logger
from utils.time_parse import timestamp_to_utc_strtime
from utils.http_client import TSPRequest as hreq


class TestChargeEndMsg(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    def test_charge_end_event(self, vid, prepare, publish_msg, checker):
        # 构造并上报消息
        mileage = prepare['original_mileage'] + 1

        # 同一个charge_id的充电结束事件，如果上报多次，经纬度为第一次上报的，保持不变
        nextev_message, charge_end_obj = publish_msg('charge_end_event',
                                                     vehicle_status={"mileage": mileage})

        time.sleep(3)
        with allure.step("校验充电结束事件存入vehicle_soc_history表"):
            tables = ['vehicle_soc_history']
            checker.check_mysql_tables(charge_end_obj, tables, event_name='charge_end_event', sample_ts=charge_end_obj['sample_ts'])

    def test_null_position_status(self, vid, env, prepare, publish_msg_by_kafka, mysql):
        """
        不包含position_status，延时5秒调用查询某时间点前最新路径信息接口补录对应位置数据
        /api/1/in/data/vehicle/brief_info（http://showdoc.nevint.com/index.php?s=/datareport&page_id=3950）
        """
        # 构造并上报消息
        mileage = prepare['original_mileage'] + 1
        charge_id = str(int(time.time()))
        nextev_message, charge_start_obj = publish_msg_by_kafka('charge_start_event',
                                                                charge_id=charge_id,
                                                                vehicle_status={"mileage": mileage})

        nextev_message, charge_end_obj = publish_msg_by_kafka('charge_end_event', sleep_time=5,
                                                              charge_id=charge_id,
                                                              vehicle_status={"mileage": mileage},
                                                              clear_fields=["position_status"])
        with allure.step("调用journey/track/newest接口查询最新经纬度"):
            inputs = {
                "host": env['host']['tsp_in'],
                "method": "GET",
                "path": f"/api/1/in/data/vehicle/{vid}/journey/track/newest",
                "params": {
                    'app_id': 10005,
                    'inquire_time': int(time.time()),
                    "hash_type": "md5",
                    "sign": ''
                },
                "timeout": 5.0
            }
            response = hreq.request(env, inputs)
            logger.info("request status is {}".format(response["result_code"]))
        with allure.step("校验vehicle_soc_history的经纬度"):
            end_time = timestamp_to_utc_strtime(charge_end_obj['sample_ts'])
            record = mysql['rvs'].fetch('vehicle_soc_history', {"vehicle_id": vid, "event_id": charge_id, "end_time": end_time})
            longitude = record[0]['longitude']
            latitude = record[0]['latitude']
            assert_equal(longitude, response['data']['track'][0]['longitude'])
            assert_equal(latitude, response['data']['track'][0]['latitude'])
