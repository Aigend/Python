#!/usr/bin/env python
# coding=utf-8

"""
:file: test_charge_start_event_mysql.py
:author: chunming.liu
:Date: Created on 2019/1/11
:Description: 充电开始事件
"""
import allure
import time
import pytest


class TestChargeStartMsg(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        charge_id = time.strftime("%Y%m%d", time.localtime()) + '0001'
        # original_mileage_in_mysql = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])[0]['mileage']
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        original_mileage_in_mysql = sql_result[0]['mileage'] if sql_result else 0
        is_exist = checker.mysql.fetch('vehicle_soc_history',
                                       {"vehicle_id": vid, "event_type": 1, "event_id": charge_id}, ['charger_type'])
        original_charger_type_in_mysql = is_exist[0]['charger_type'] if is_exist else None
        return {'charge_id': charge_id, 'original_mileage': original_mileage_in_mysql, 'original_charger_type': original_charger_type_in_mysql}

    def test_charge_start_event(self, vid, prepare, publish_msg, checker):
        # 构造并上报消息
        # 问题排查标注
        mileage = prepare['original_mileage'] + 1
        # 同一个charge_id的充电开始事件，如果上报多次，charger_type为第一次上报的，保持不变
        if prepare['original_charger_type'] is not None:
            nextev_message, charge_start_obj = publish_msg('charge_start_event',
                                                           charge_id=prepare['charge_id'],
                                                           charging_info={"charger_type": prepare.get('original_charger_type')},
                                                           vehicle_status={"mileage": mileage})
        else:
            nextev_message, charge_start_obj = publish_msg('charge_start_event',
                                                           charge_id=prepare['charge_id'],
                                                           clear_fields= ['charging_info'],
                                                           vehicle_status={"mileage": mileage})

        with allure.step("校验充电开始事件存入vehicle_soc_history表"):
            tables = ['vehicle_soc_history']
            checker.check_mysql_tables(charge_start_obj, tables, event_name='charge_start_event')
