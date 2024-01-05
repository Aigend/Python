#!/usr/bin/env python
# coding=utf-8

"""
:file: test_periodical_charge_update_cassandra.py
:author: zhiqiang.zhu
:Date: Created on 2017/1/12 下午8:01
:Description: 周期性充电消息上报，包含position_status数据，driving_data数据，vehicle_status数据，occupant_status数据，soc_status数据，
:alarm数据，driving_motor数据，extremum数据。
"""
import datetime

import allure
import pytest


class TestChargeUpdateMsg(object):
    @pytest.mark.parametrize("reissue", [True, False], ids=['reissue is True', 'reissue if False'])
    def test_periodical_charge_update(self, publish_msg, reissue, checker):
        # 构造并上报消息
        nextev_message, charge_update_obj = publish_msg('periodical_charge_update',
                                                        reissue=reissue,
        )

        # 校验
        # 周期上报事件的alarm_signal存到cassandra里的alarm_data，alarm_data存到cassandra里的re_alarm_data里，
        tables ={'vehicle_data':['vehicle_id',
                                    'charging_info',
                                    'soc_status',
                                    'body_status',
                                    'position_status',
                                    'vehicle_status',
                                    'bms_status',
                                    'driving_data',
                                    'driving_motor_status',
                                    'extremum_data',
                                    'occupant_status',
                                    'hvac_status',
                                    'tyre_status',
                                    'can_msg',
                                    'can_signal',
                                    're_alarm_data',
                                    'alarm_data',
                                    'evm_flag',
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
        checker.check_cassandra_tables(charge_update_obj['sample_points'][0], tables,
                                       event_name='periodical_charge_update',
                                       sample_ts=charge_update_obj['sample_points'][0]['sample_ts'])

    def test_some_wti_not_save(self, publish_msg, cassandra, vid):
        # 只有2个update事件会过滤wti，instant和alarm事件不会过滤
        with allure.step('过滤evm_flag =false&&alarm_signal只有这个CAM_FC_03:LKSTakeoverReq信号 && vehicle_status.vehl_state = 1'):
            event_name='periodical_charge_update'

            signal_all = [
                {"name": "CAM_FC_03:LKSTakeoverReq", "value": 1, "alarm_level": 4, "wti_code": "WTI-158"},
            ]
            nextev_message, obj = publish_msg('periodical_charge_update',
                                              sample_points=[{'alarm_signal': {'signal_int': signal_all},
                                                              'vehicle_status': {'vehl_state': 1},
                                                              'evm_flag': False}])
            sample_date = datetime.datetime.fromtimestamp(obj['sample_points'][0]['sample_ts'] / 1000.0).strftime('%Y-%m')
            event_in_cassandra = cassandra['datacollection'].fetch('vehicle_data', where_model={'vehicle_id': vid,
                                                                                                'sample_date': sample_date,
                                                                                                'sample_ts': obj['sample_points'][0]['sample_ts'],
                                                                                                'msg_type': 'periodical_charge_update'
                                                                                                }, )

            # 校验
            assert len(event_in_cassandra) == 0

        with allure.step('过滤evm_flag =false&&alarm_signal只有这个VCU_CGW_219:VCUChgLineSts信号 && 充电状态中即chrg_state=1'):
            signal_all = [
                {"name": "VCU_CGW_219:VCUChgLineSts", "value": 1, "alarm_level": 4, "wti_code": "WTI-43"},
            ]
            nextev_message, obj = publish_msg(event_name,
                                              sample_points=[{'alarm_signal': {'signal_int': signal_all},
                                                              'soc_status': {'chrg_state': 1},
                                                              'evm_flag': False}])
            sample_date = datetime.datetime.fromtimestamp(obj['sample_points'][0]['sample_ts'] / 1000.0).strftime('%Y-%m')
            event_in_cassandra = cassandra['datacollection'].fetch('vehicle_data', where_model={'vehicle_id': vid,
                                                                                                'sample_date': sample_date,
                                                                                                'sample_ts': obj['sample_points'][0]['sample_ts'],
                                                                                                'msg_type': event_name
                                                                                                }, )

            assert len(event_in_cassandra) == 0

    def test_periodical_charge_update_without_trip_id(self, publish_msg, checker):
        """
        http://venus.nioint.com/#/detailWorkflow/wf-20210709142237-ir
        proto ver>=18时，无trip_id由journey_id替代
        :param publish_msg:
        :param checker:
        :return:
        """
        # 构造并上报消息
        nextev_message, charge_update_obj = publish_msg('periodical_charge_update', protobuf_v=18,
                                                        signallib_version='BL00.07.00_DA_01')

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
        charge_update_obj['sample_points'][0]['version'] = charge_update_obj['version']
        charge_update_obj['sample_points'][0]['process_id'] = charge_update_obj['charge_id']
        checker.check_cassandra_tables(charge_update_obj['sample_points'][0], tables,
                                       event_name='periodical_charge_update',
                                       sample_ts=charge_update_obj['sample_points'][0]['sample_ts'])



