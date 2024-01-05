#!/usr/bin/env python
# coding=utf-8

"""
:file: test_charge_start_event_cassandra.py
:author: chunming.liu
:Date: Created on 2019/11/11
:Description: 充电开始事件，包含电池数据
"""
import datetime
import allure

from utils.assertions import assert_equal


class TestChargeStartMsg(object):
    def test_charge_start_event_cassandra(self, publish_msg, checker):
        # 构造并上报消息
        nextev_message, charge_start_obj = publish_msg('charge_start_event')

        # 校验
        tables = {
            'vehicle_data': ['vehicle_id',
                             'charging_info',
                             'soc_status',
                             'position_status',
                             'vehicle_status',
                             'btry_pak_info',
                             'icc_id',
                             'process_id as charge_id',
                             'sample_ts'],

            'driving_data': ['dump_enrgy',
                             'mileage',
                             'position',
                             'posng_valid_type',
                             'soc',
                             'speed',
                             'realtime_power_consumption',
                             'sample_ts']
        }
        checker.check_cassandra_tables(charge_start_obj, tables, event_name='charge_start_event')

    def test_process_id_is_null_dont_update_driving_data(self, env, publish_msg_by_kafka, checker):
        with allure.step("校验不传charge_id时，不更新Cassandra的driving_data表"):
            # 构造并上报消息
            nextev_message, charge_start_obj = publish_msg_by_kafka('charge_start_event', clear_fields=["charge_id"])

            # 校验
            sample_date = datetime.datetime.fromtimestamp(charge_start_obj["sample_ts"] / 1000.0).strftime('%Y-%m')
            event_in_cassandra = checker.cassandra.fetch('driving_data', where_model={'vehicle_id': env['vehicles']['normal']['vehicle_id'],
                                                                                      'sample_date': sample_date,
                                                                                      'sample_ts': charge_start_obj["sample_ts"]})
            assert_equal(len(event_in_cassandra), 0)
    
    def test_periodical_charge_update_without_trip_id(self, publish_msg, checker):
        """
        http://venus.nioint.com/#/detailWorkflow/wf-20210709142237-ir
        proto ver>=18时，无trip_id由journey_id替代
        :param publish_msg:
        :param checker:
        :return:
        """
        # 构造并上报消息
        nextev_message, charge_start_obj = publish_msg('charge_start_event', protobuf_v=18)

        # 校验
        tables = {
                  'driving_data': ['dump_enrgy',
                                   'mileage',
                                   'position',
                                   'posng_valid_type',
                                   'soc',
                                   'speed',
                                   'realtime_power_consumption',
                                   'process_id',
                                   'sample_ts']
                  }
        checker.check_cassandra_tables(charge_start_obj, tables, event_name='charge_start_event')
