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
            checker.check_mysql_tables(charge_end_obj, tables, event_name='charge_end_event')

