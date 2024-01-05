#!/usr/bin/env python
# coding=utf-8

"""
:file: test_custom_alarm_event_mysql.py
:author: liliu
:Description: 信号报警，包含国标报警和自定义报警的校验
"""
import json
import random
import time
import allure
from datetime import datetime

import pytest

from nio_messages import wti
from utils.assertions import assert_equal
from utils.time_parse import timestamp_to_utc_strtime, now_utc_strtime, now_time_sec

index_names = ['WTI-BMS-2', 'WTI-BMS-4', 'WTI-EP-15', 'WTI-EP-17', 'WTI-EP-2', 'WTI-BC-6', 'WTI-BMS-3', 'WTI-BSD-1',
               'WTI-FCTA-1', 'WTI-FCTA-2', 'WTI-SA-1', 'WTI-BMS-8', 'WTI-CT-1','WTI-CT-2','WTI-CT-3','WTI-PA-15',
               'WTI-TPMS-28', 'WTI-TPMS-27', 'WTI-TPMS-26', 'WTI-TPMS-25', 'WTI-SCM-1', 'WTI-VSTS-7', 'WTI-VSTS-8',
               'WTI-SB-1', 'WTI-LGHT-65', 'WTI-LGHT-66', 'WTI-ADAS-11','WTI-SA-7','WTI-SA-8','WTI-SA-9','WTI-SA-10',
               'WTI-PBRK-7','WTI-PBRK-8','WTI-PBRK-12','WTI-PBRK-13','WTI-PBRK-14']


class TestAlarmSignalUpdateMSG(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, publish_msg_by_kafka):
        # 清空wti
        publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []}, sleep_time=4)

    def test_alarm_signal_update(self, vid, vin, prepare, publish_msg_by_kafka, checker):

        # here we want to choose alarm which is wti_enabled
        signal_int = []
        while True:
            s = random.choice(wti.SIGNAL)
            # 带note标记的都是比较特殊的wti，此处随机选一个的时候不选它
            if 'note' in s:
                continue
            is_wti_enabled = checker.mysql.fetch('const_wti',
                                                 where_model={"wti_code": s['wti_code']},
                                                 fields=['wti_enabled'])[0]['wti_enabled']
            if is_wti_enabled == 0:
                continue

            signal_int.append(s)
            break

        nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': signal_int},
                                                   sleep_time=2)

        # 校验
        tables = ['status_wti_alarm', 'history_wti_alarm']
        checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                   extra=signal_int)

    def test_history_wti_alarm_endtime_will_update(self, vid, vin, prepare, checker, publish_msg_by_kafka):
        publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []}, sleep_time=2)
        with allure.step("校验 上报两次alarm_signal事件时，history_wti_alarm中会更新第一次报，且不再在第二次继续上报的wti对应条目的end_time"):
            # 例如第一次的为（wti_1,wti_2）,第二次的为（wti_1,wti_3）
            # 则history_wti_alarm表中wti_2对应的条目的end_time会更新,但是wti_1不会更新，因为第二次继续报了wti_1

            # 准备数据
            first_sn = str(round(time.time() * 1000))
            first_alarm_signal = [
                {'sn': first_sn, 'name': 'ABSFailLampReq', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-BC-1',
                 "alarm_id": vin + '-' + first_sn + '-BC-1-WTI'}
            ]

            time.sleep(2)

            second_sn = str(round(time.time() * 1000))
            second_alarm_signal = [
                {'sn': first_sn, 'name': 'EBDFailLampReq', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-BC-4',
                 "alarm_id": vin + '-' + second_sn + '-BC-4-WTI'}
            ]

            # 第一次上报，检查history_wti_alarm中wti的start_time为上报的sn值，end_time为null
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': first_alarm_signal}, sleep_time=2)

            old_wti_in_mysql = checker.mysql.fetch('history_wti_alarm',
                                                   {"vehicle_id": vid,
                                                    'alarm_id': first_alarm_signal[0]['alarm_id']},
                                                   fields=['start_time', 'end_time'])[0]

            start_time = timestamp_to_utc_strtime(first_alarm_signal[0]['sn'])

            assert_equal(start_time, old_wti_in_mysql['start_time'])
            assert_equal(None, old_wti_in_mysql['end_time'])

            # 第二次上报，检查history_wti_alarm中第一次那条的wti的start_time保持不变为第一次上报的sn值，end_time值依据第二次上报的sample_ts进行更新
            time.sleep(2)
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': second_alarm_signal})
            new_wti_in_mysql = checker.mysql.fetch('history_wti_alarm',
                                                   {"vehicle_id": vid,
                                                    'alarm_id': first_alarm_signal[0]['alarm_id']},
                                                   fields=['start_time', 'end_time'])[0]

            end_time = timestamp_to_utc_strtime(obj['sample_ts'])
            assert_equal(start_time, new_wti_in_mysql['start_time'])
            assert_equal(end_time, new_wti_in_mysql['end_time'])

    def test_alarm_level_will_update(self, vin, vid, prepare, publish_msg_by_kafka, checker):
        """
        校验 上报两次alarm_signal时，status_wti_alarm 中会更新第一次报，且不再在第二次继续上报的wti对应条目的alarm_level为0
        例如第一次的为（wti_1,wti_2）,第二次的为（wti_1,wti_3）
        则status_wti_alarm表中wti_2对应的条目的alarm_level会更新为0,表示该条alarm结束了。
        并且wti_2除alarm_level与update_time之外的记录仍为第一次的数值，不会更新为第二次的数值。
        wti_1的所有数据则始终是第一次上报的值

        """
        with allure.step("校验上报两次alarm_signal时，status_wti_alarm 中会更新第一次报，且不再在第二次继续上报的wti对应条目的alarm_level为0"):
            # 准备数据
            first_sn = str(round(time.time() * 1000))
            first_alarm_signal = [
                {'sn': first_sn, 'name': 'VCUHVILError', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-EP-15',
                 "alarm_id": vin + '-' + first_sn + '-EP-15-WTI'}
            ]

            time.sleep(2)
            second_sn = str(round(time.time() * 1000))
            second_alarm_signal = [
                {'sn': first_sn, 'name': 'VCUImdStopDriving', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-EP-16',
                 "alarm_id": vin + '-' + second_sn + '-EP-16-WTI'}
            ]
            # 第一次上报，检查status_wti_alarm中wti的alarm_level为上报的level值
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': first_alarm_signal}, sleep_time=2)

            status_wti_alarm_mysql_first = \
                checker.mysql.fetch('status_wti_alarm', {"id": vid, 'wti_code': first_alarm_signal[0]['wti_code']})[0]
            assert_equal(status_wti_alarm_mysql_first['alarm_level'], first_alarm_signal[0]['alarm_level'])

            # 第二次上报，检查status_wti_alarm中第一次那条的wti的alarm_level值为0，表示该alarm已经终止
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': second_alarm_signal}, sleep_time=2)
            status_wti_alarm_mysql_second = \
                checker.mysql.fetch('status_wti_alarm', {"id": vid, 'wti_code': first_alarm_signal[0]['wti_code']})[0]
            assert_equal(status_wti_alarm_mysql_second['alarm_level'], 0)

    @pytest.mark.test
    def test_wti_enabled(self, vid, prepare, checker, publish_msg_by_kafka):
        with allure.step('校验 上报的alarm_signal必须在const_wti表中wti_enabled=1，数据才写入status_wti_alarm,history_wti_alarm 表'):
            alarm_signal = [
                {'name': 'TpmsSts', 'value': 2, 'alarm_level': 2, 'wti_code': 'WTI-TPMS-4'}
            ]
            wti_code = alarm_signal[0]['wti_code']
            # 预先校验上报的alarm在const_wti表中wti_enabled=0
            is_wti_enabled = \
                checker.mysql.fetch('const_wti', where_model={"wti_code": wti_code}, fields=['wti_enabled'])[0][
                    'wti_enabled']
            assert is_wti_enabled == 0

            # 上报
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': alarm_signal}, sleep_time=2)

            # 校验
            status_wti_alarm_mysql = checker.mysql.fetch('status_wti_alarm', {"id": vid, 'wti_code': wti_code}, retry_num=5)
            history_wti_alarm_mysql = checker.mysql.fetch('history_wti_alarm',
                                                          {'vehicle_id': vid, 'wti_code': wti_code}, retry_num=5)
            assert_equal(len(status_wti_alarm_mysql), 0)
            assert_equal(len(history_wti_alarm_mysql), 0)

    def test_wti_mutual_exclude(self, prepare, publish_msg_by_kafka, checker):
        with allure.step('校验  互斥的 wti'):
            signal_all = [
                random.choice([
                    {'name': 'Textinfo', 'value': 4, 'alarm_level': 2, 'wti_code': 'WTI-ADAS-1',
                     'note': 'WTI-ADAS-1,WTI-NP-5，WTI-NP-7，WTI-NP-9互斥'},
                    {'name': 'Textinfo', 'value': 5, 'alarm_level': 2, 'wti_code': 'WTI-NP-5',
                     'note': 'WTI-ADAS-1,WTI-NP-5，WTI-NP-7, WTI-NP-9互斥'},
                    {'name': 'Textinfo', 'value': 7, 'alarm_level': 2, 'wti_code': 'WTI-NP-7',
                     'note': 'WTI-ADAS-1,WTI-NP-5，WTI-NP-7, WTI-NP-9互斥'},
                    {'name': 'Textinfo', 'value': 9, 'alarm_level': 4, 'wti_code': 'WTI-NP-9',
                     'note': 'WTI-ADAS-1,WTI-NP-5，WTI-NP-7, WTI-NP-9互斥'},
                ]),
                random.choice([
                    {'name': 'BMSIsolationLvl', 'value': 3, 'alarm_level': 1, 'wti_code': 'WTI-BMS-4',
                     'note': '互斥 WTI-BMS-4, WTI-BMS-3, WTI-BMS-5'},
                    {'name': 'BMSIsolationLvl', 'value': 2, 'alarm_level': 2, 'wti_code': 'WTI-BMS-3',
                     'note': '互斥 WTI-BMS-4, WTI-BMS-3, WTI-BMS-5'},
                    {'name': 'BMSIsolationLvl', 'value': 4, 'alarm_level': 2, 'wti_code': 'WTI-BMS-5',
                     'note': '互斥 WTI-BMS-4, WTI-BMS-3, WTI-BMS-5'}
                ]),
                random.choice([
                    {'name': 'BMSCellVoltageOverUnder', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-EVM-4',
                     'note': '互斥 WTI-EVM-4,WTI-EVM-5'},
                    {'name': 'BMSCellVoltageOverUnder', 'value': 2, 'alarm_level': 1, 'wti_code': 'WTI-EVM-5',
                     'note': '互斥 WTI-EVM-4,WTI-EVM-5'},
                ]
                ),
                random.choice([
                    {'name': 'BMSFaultLvl', 'value': [2, 3], 'alarm_level': 2, 'wti_code': 'WTI-BMS-1',
                     'note': '互斥 WTI-BMS-1, WTI-BMS-2'},
                    {'name': 'BMSFaultLvl', 'value': [4, 5], 'alarm_level': 1, 'wti_code': 'WTI-BMS-2',
                     'note': '互斥 WTI-BMS-1, WTI-BMS-2'},
                ]),
                random.choice([
                    {'name': 'LvlAdjLampReq', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-SSPC-4',
                     'note': '互斥 WTI-SSPC-4, WTI-SSPC-5'},
                    {'name': 'LvlAdjLampReq', 'value': 2, 'alarm_level': 2, 'wti_code': 'WTI-SSPC-5',
                     'note': '互斥 WTI-SSPC-4, WTI-SSPC-5'},
                ]),
                random.choice([
                    {'name': 'BMSSOCOverUnder', 'value': 2, 'alarm_level': 1, 'wti_code': 'WTI-EVM-6',
                     'note': '互斥 WTI-EVM-3, WTI-EVM-6'},
                    {'name': 'BMSSOCOverUnder', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-EVM-3',
                     'note': '互斥 WTI-EVM-3, WTI-EVM-6'},
                ]),
                random.choice([
                    {'name': 'VCUChrgDispLampReq', 'value': 3, 'alarm_level': 2, 'wti_code': 'WTI-CHRG-3',
                     'note': '互斥 WTI-CHRG-3, WTI-CHRG-8'},
                    {'name': 'VCUChrgDispLampReq', 'value': 7, 'alarm_level': 4, 'wti_code': 'WTI-CHRG-8',
                     'note': '互斥 WTI-CHRG-3, WTI-CHRG-8'},
                ]),
                random.choice([
                    {'name': 'TpmsFrntLeWhlPressSts', 'value': 2, 'alarm_level': 2, 'wti_code': 'WTI-TPMS-17',
                     'description': '左前轮胎压力低', 'note': '互斥 WTI-TPMS-17,WTI-TPMS-25'},
                    {'name': 'WTI-TPMS-25', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-TPMS-25',
                     'description': '左前轮胎压力过高', 'note': '互斥 WTI-TPMS-17,WTI-TPMS-25'},
                ]),
                random.choice([
                    {'name': 'TpmsFrntRiWhlPressSts', 'value': 2, 'alarm_level': 2, 'wti_code': 'WTI-TPMS-18',
                     'description': '右前轮胎压力低', 'note': '互斥 WTI-TPMS-18,WTI-TPMS-26'},
                    {'name': 'WTI-TPMS-26', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-TPMS-26',
                     'description': '右前轮胎压力过高', 'note': '互斥 WTI-TPMS-18,WTI-TPMS-26'},
                #     TpmsFrntRiWhlPressSts
                ]),
                random.choice([
                    {'name': 'TpmsReLeWhlPressSts', 'value': 2, 'alarm_level': 2, 'wti_code': 'WTI-TPMS-19',
                     'description': '左后轮胎压力低', 'note': '互斥 WTI-TPMS-19,WTI-TPMS-27'},
                    {'name': 'WTI-TPMS-27', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-TPMS-27',
                     'description': '左后轮胎压力过高', 'note': '互斥 WTI-TPMS-19,WTI-TPMS-27'},
                #     TpmsReLeWhlPressSts
                ]),
                random.choice([
                    {'name': 'TpmsReRiWhlPressSts', 'value': 2, 'alarm_level': 2, 'wti_code': 'WTI-TPMS-20',
                     'description': '右后轮胎压力低', 'note': '互斥 WTI-TPMS-20,WTI-TPMS-28'},
                    {'name': 'WTI-TPMS-28', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-TPMS-28',
                     'description': '右后轮胎压力过高', 'note': '互斥 WTI-TPMS-20,WTI-TPMS-28'},
                ]),

            ]

            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_all}, sleep_time=5)
            time.sleep(10)
            tables = ['status_wti_alarm', 'history_wti_alarm']
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_all)

    def test_wti_special(self, vin, vid, prepare, publish_msg_by_kafka, checker):
        # TODO WTI-VSTS-1 WTI-VSTS-2还没做校验，目前还没有讨论出该怎么上报。待后续添加case
        with allure.step('校验 WTI-EP-4 and WTI-EP-8 时会触发WTI-EP-11'):
            signal_all = [
                {'name': 'PEUFFltSts', 'value': 3, 'alarm_level': 2, 'wti_code': 'WTI-EP-4',
                 'note': 'WTI-EP-4 and WTI-EP-8 时会触发WTI-EP-11'},
                {'name': 'PEURFltSts', 'value': 3, 'alarm_level': 2, 'wti_code': 'WTI-EP-8',
                 'note': 'WTI-EP-4 and WTI-EP-8 时会触发WTI-EP-11'},
                {'name': 'PEUFFltSts,PEURFltSts', 'value': 3, 'alarm_level': 2, 'wti_code': 'WTI-EP-11',
                 'note': 'WTI-EP-4 and WTI-EP-8 时会触发WTI-EP-11'},
            ]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_all})
            tables = ['status_wti_alarm', 'history_wti_alarm']
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_all)

        with allure.step('校验 WTI-EP-5 and WTI-EP-9 时会触发WTI-EP-12'):
            publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []})
            signal_all = [
                {'name': 'PEUFFltSts', 'value': [4, 5], 'alarm_level': 2, 'wti_code': 'WTI-EP-5',
                 'note': 'WTI-EP-5 and WTI-EP-9 时会触发WTI-EP-12'},
                {'name': 'PEURFltSts', 'value': [4, 5], 'alarm_level': 2, 'wti_code': 'WTI-EP-9',
                 'note': 'WTI-EP-5 and WTI-EP-9 时会触发WTI-EP-12'},
                {'name': 'PEUFFltSts,PEURFltSts', 'value': [4, 5], 'alarm_level': 1, 'wti_code': 'WTI-EP-12',
                 'note': 'WTI-EP-5 and WTI-EP-9 时会触发WTI-EP-12'},
            ]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_all})
            tables = ['status_wti_alarm', 'history_wti_alarm']
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_all)

        with allure.step('校验WTI-BC-4 and WTI-VSTB-2 时会触发WTI-BC-5'):
            publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []})
            signal_all = [
                {'name': 'EBDFailLampReq', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-BC-4',
                 'note': 'WTI-BC-4 and WTI-VSTB-2 时会触发WTI-BC-5'},
                {'name': 'VDCTCSFailLampReq', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-VSTB-2',
                 'note': 'WTI-BC-4 and WTI-VSTB-2 时会触发WTI-BC-5'},
                {'name': 'EBDFailLampReq,VDCTCSFailLampReq', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-BC-5',
                 'note': 'WTI-BC-4 and WTI-VSTB-2 时会触发WTI-BC-5'},
            ]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_all})
            tables = ['status_wti_alarm', 'history_wti_alarm']
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_all)

        with allure.step('校验 WTI-CHRG-5 name为ACChrgrOverT或DCChrgrOverT都可以'):
            publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []}, sleep_time=2)
            signal_all = [
                {'name': 'ACChrgrOverT', 'value': 1, 'alarm_level': 4, 'wti_code': 'WTI-CHRG-5',
                 'note': 'ACChrgrOverT=1 or DCChrgrOverT=1'},
                {'name': 'DCChrgrOverT', 'value': 1, 'alarm_level': 4, 'wti_code': 'WTI-CHRG-5',
                 'note': 'ACChrgrOverT=1 or DCChrgrOverT=1'},
            ]
            signal_special = [random.choice(signal_all)]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_special}, sleep_time=2)
            tables = ['status_wti_alarm', 'history_wti_alarm']
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_special)

        with allure.step('校验WTI-PA-16 name为ACChrgrOverT或DCChrgrOverT都可以触发，或者WTI-PA-17 and WTI-PA-18 时会触发WTI-PA-16'):
            publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []})
            signal_all = [
                random.choice([
                    {'name': 'UpaSysDi', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-PA-16',
                     'note': 'UpaSysDi=1 or UpaSysSrv=1 or (WTI-PA-17 and WTI-PA-18)'},
                    {'name': 'UpaSysSrv', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-PA-16',
                     'note': 'UpaSysDi=1 or UpaSysSrv=1 or (WTI-PA-17 and WTI-PA-18)'},
                ])
            ]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_all})
            tables = ['status_wti_alarm', 'history_wti_alarm']
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_all)

            publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []})
            signal_all = [
                {'name': 'FrntSnsrFltSt', 'value': [1, 2], 'alarm_level': 2, 'wti_code': 'WTI-PA-17',
                 'note': 'WTI-PA-17 and WTI-PA-18 时会触发WTI-PA-16'},
                {'name': 'ReSnsrFltSt', 'value': [1, 2], 'alarm_level': 2, 'wti_code': 'WTI-PA-18',
                 'note': 'WTI-PA-17 and WTI-PA-18 时会触发WTI-PA-16'},
                {
                    'name': 'UpaSysDi=1 or UpaSysSrv=1 or ((FrntSnsrFltSt=1 or FrntSnsrFltSt=2) and (ReSnsrDltSt=1 or ReSnsrFltSt=2))',
                    'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-PA-16',
                    'note': 'UpaSysDi=1 or UpaSysSrv=1 or (WTI-PA-17 and WTI-PA-18)'},
            ]

            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_all})
            tables = ['status_wti_alarm', 'history_wti_alarm']
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_all)

        with allure.step('WTI-PS-5 rvs_server不处理'):
            signal_int = [
                {'name': 'PassAirbgInhbnLampReq', 'value': 2, 'alarm_level': 4, 'wti_code': 'WTI-PS-5',
                 'note': 'rvs server 不处理'}
            ]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_int})
            sn = obj['alarm_signal']['signal_int'][0]['sn']
            # 校验
            alarm_id = '{}-{}-{}-WTI'.format(vin, sn, signal_int[0]['wti_code'][4:])
            history_wti = checker.mysql.fetch('history_wti_alarm', {"vehicle_id": vid, 'alarm_id': alarm_id}, retry_num=5)
            assert_equal(len(history_wti), 0)

    def test_wti_more_special(self, vid, publish_msg_by_kafka, checker, prepare):
        with allure.step('校验 ProtoBufVersion>=16时，BMSDCChargeCurrentOverUnder=1只会触发WTI-BMS-10'):
            publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []}, sleep_time=2)
            old_evm_20_mysql = checker.mysql.fetch('status_wti_alarm', {"id": vid, 'wti_code in': ['WTI-EVM-20']})[0]

            signal_all = [
                {'name': 'BMSDCChargeCurrentOverUnder', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-BMS-10',
                 'note': 'ProtoBufVersion>=16且BMSDCChargeCurrentOverUnder=1，只生成WTI-BMS-10，ProtoBufVersion<16且BMSDCChargeCurrentOverUnder=1，生成WTI-BMS-10和WTI-EVM-20'},

            ]
            sample_ts = round(time.time() * 1000)
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event', sample_ts=sample_ts,
                                                       alarm_signal={'signal_int': signal_all})
            tables = ['status_wti_alarm', 'history_wti_alarm']
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_all)

            new_evm_20_mysql = checker.mysql.fetch('status_wti_alarm', {"id": vid, 'wti_code in': ['WTI-EVM-20']})[0]
            assert_equal(old_evm_20_mysql, new_evm_20_mysql)

        with allure.step('校验 ProtoBufVersion<16时，BMSDCChargeCurrentOverUnder=1会触发WTI-BMS-10和WTI-EVM0-20'):
            publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []}, sleep_time=2)
            signal_all = [
                {'name': 'BMSDCChargeCurrentOverUnder', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-BMS-10',
                 'note': 'ProtoBufVersion>=16且BMSDCChargeCurrentOverUnder=1，只生成WTI-BMS-10，ProtoBufVersion<16且BMSDCChargeCurrentOverUnder=1，生成WTI-BMS-10和WTI-EVM-20'},
                {'name': 'BMSDCChargeCurrentOverUnder and ProtoBufVersion<16', 'value': 1, 'alarm_level': 1,
                 'wti_code': 'WTI-EVM-20',
                 'note': 'ProtoBufVersion>=16且BMSDCChargeCurrentOverUnder=1，只生成WTI-BMS-10，ProtoBufVersion<16且BMSDCChargeCurrentOverUnder=1，生成WTI-BMS-10和WTI-EVM-20'},

            ]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_all}, protobuf_v=15)
            tables = ['status_wti_alarm', 'history_wti_alarm']
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_all)

        with allure.step('校验 ProtoBufVersion<16时，BMSCellVoltageOverUnder=1只触发WTI-EVM-4'):
            publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []})
            old_evm_20_mysql = checker.mysql.fetch('status_wti_alarm', {"id": vid, 'wti_code in': ['WTI-EVM-20']})[0]
            signal_all = [
                {'name': 'BMSCellVoltageOverUnder', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-EVM-4',
                 'note': '互斥 WTI-EVM-4,WTI-EVM-5; ProtoBufVersion>=16且BMSCellVoltageOverUnder=1，生成WTI-EVM-4和WTI-EVM-20，ProtoBufVersion<16且BMSCellVoltageOverUnder=1，只生成WTI-EVM-4'}

            ]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_all}, protobuf_v=15)
            tables = ['status_wti_alarm', 'history_wti_alarm']
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_all)
            new_evm_20_mysql = checker.mysql.fetch('status_wti_alarm', {"id": vid, 'wti_code in': ['WTI-EVM-20']})[0]
            assert_equal(old_evm_20_mysql, new_evm_20_mysql)

        with allure.step('校验 ProtoBufVersion>=16时，BMSCellVoltageOverUnder=1触发WTI-EVM-4和WTI-EVM-20'):
            publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []})
            signal_all = [
                {'name': 'BMSCellVoltageOverUnder', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-EVM-4',
                 'note': '互斥 WTI-EVM-4,WTI-EVM-5; ProtoBufVersion>=16且BMSCellVoltageOverUnder=1，生成WTI-EVM-4和WTI-EVM-20，ProtoBufVersion<16且BMSCellVoltageOverUnder=1，只生成WTI-EVM-4'},
                {'name': 'BMSCellVoltageOverUnder and ProtoBufVersion>=16', 'value': 1, 'alarm_level': 1,
                 'wti_code': 'WTI-EVM-20',
                 'note': '互斥 WTI-EVM-4,WTI-EVM-5; ProtoBufVersion>=16且BMSCellVoltageOverUnder=1，生成WTI-EVM-4和WTI-EVM-20，ProtoBufVersion<16且BMSCellVoltageOverUnder=1，只生成WTI-EVM-4'}

            ]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_all})
            tables = ['status_wti_alarm', 'history_wti_alarm']
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_all)

    def test_wti_normal(self, publish_msg_by_kafka, checker, prepare):
        # 等待数据完全清空
        time.sleep(10)

        with allure.step('校验 所有普通wti，即不含note并且wti_enabled的wti'):
            wti_not_enabled = [item['wti_code'] for item in
                               checker.mysql.fetch('const_wti', where_model={"wti_enabled": 0}, fields=['wti_code'])]
            signal_all = list()
            for item in wti.SIGNAL:
                if item['wti_code'] not in wti_not_enabled:
                    if 'note' in item:
                        continue
                    if isinstance(item['value'], int):
                        signal_all.append(item)
                    elif isinstance(item['value'], list):
                        item['value'] = random.choice(item['value'])
                        signal_all.append(item)

            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_all}, sleep_time=14)
            time.sleep(5)
            tables = ['status_wti_alarm', 'history_wti_alarm']

            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_all)

    @pytest.mark.skip('manual')
    def test_WTI_PS_1(self, publish_msg_by_kafka, checker, prepare):
        """
        WTI-PS-1 的报警会有版本控制，版本大于等于 Bl220(ES8 F140="V0001541 BX", ES6 F140="V0058915 AB")才写入mysql数据库，
        版本信息会在redis记录 remote_vehicle_test:vehicle_status:{vid}:VersionModel

        逻辑为：若redis的 remote_vehicle_test:vehicle_status:{vid}:VersionModel 中为空，那么所有WTI事件都可以通过查询mysql中的status_did表，
               向该key插入车机版本信息，且其TTL为1小时。若非空，不会进行更新。
               而只有 WTI-PS-1 的报警事件会读取该key存储的车机版本号并校验，若小于Bl220，则该报警事件不会写入mysql。

        测试关键步骤：通过 pangu 平台的 EVM -> 车辆ECU-did工具 或 publish_msg_by_kafka('did_update_event'）
                    上报需要的CGW的车机版本，删除redis的remote_vehicle_test:vehicle_status:{vid}:VersionModel的key，
                    上报 WTI-PS-1 事件，车机版本大于等于 Bl220 才会写入mysql的 history_wti_alarm。

        注意：redis中该key的生存周期为1小时，通过did事件上报版本后，需手动删除该key存储的旧车机版本信息，或者等待该key1小时的自动清除
        """
        pass

    @pytest.mark.skip  # name包含ErrorMgmt的wti已不再支持
    def test_WTI_error_mgmt(self, publish_msg_by_kafka, checker, prepare):
        with allure.step('校验 error_mgmt的 wti'):
            signal_all = [
                random.choice([
                    {'name': 'BCU_09:ErrorMgmt', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-BC-12',
                     'note': 'name 值可以为BCU_09:ErrorMgmt 或 WTI-BC-12'},
                    {'name': 'WTI-BC-12', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-BC-12',
                     'note': 'name 值可以为BCU_09:ErrorMgmt 或 WTI-BC-12'},
                ]),
                random.choice([
                    {'name': 'BAU_02:ErrorMgmt', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-BC-13',
                     'note': 'name 值可以为BAU_02:ErrorMgmt 或 WTI-BC-13'},
                    {'name': 'WTI-BC-13', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-BC-13',
                     'note': 'name 值可以为BAU_02:ErrorMgmt 或 WTI-BC-13'},
                ]
                ),
                random.choice([
                    {'name': 'ACM_01:ErrorMgmt', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-PS-7',
                     'note': 'name 值可以为ACM_01:ErrorMgmt 或 WTI-PS-7'},
                    {'name': 'WTI-PS-7', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-PS-7',
                     'note': 'name 值可以为ACM_01:ErrorMgmt 或 WTI-PS-7'},
                ]),
                random.choice([
                    {'name': 'BCM_12:ErrorMgmt', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-TPMS-1',
                     'note': 'name 值可以为BCM_12:ErrorMgmt 或 WTI-TPMS-1'},
                    {'name': 'WTI-TPMS-1', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-TPMS-1',
                     'note': 'name 值可以为BCM_12:ErrorMgmt 或 WTI-TPMS-1'},
                ]),
                random.choice([
                    {'name': 'BCM_13:ErrorMgmt', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-TPMS-2',
                     'note': 'name 值可以为BCM_13:ErrorMgmt 或 WTI-TPMS-2'},
                    {'name': 'WTI-TPMS-2', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-TPMS-2',
                     'note': 'name 值可以为BCM_13:ErrorMgmt 或 WTI-TPMS-2'},
                ]),
                random.choice([
                    {'name': 'NM_CGW:ErrorMgmt', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-VSTS-3',
                     'note': 'name 值可以为NM_CGW:ErrorMgmt 或 WTI-VSTS-3'},
                    {'name': 'WTI-VSTS-3', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-VSTS-3',
                     'note': 'name 值可以为NM_CGW:ErrorMgmt 或 WTI-VSTS-3'},
                ]),
            ]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_all}, sleep_time=2)
            time.sleep(5)
            tables = ['status_wti_alarm', 'history_wti_alarm']
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_all)

    def test_name_is_wti_code(self, publish_msg_by_kafka, checker, prepare):
        with allure.step('校验name为wti_code的报警，会正常落库'):
            signal_all = [
                {'name': 'WTI-BC-4', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-BC-4',
                 'note': 'WTI-BC-4 and WTI-VSTB-2 时会触发WTI-BC-5, 其name值可以为EBDFailLampReq 或 WTI-BC-4'},
                {'name': 'WTI-BC-5', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-BC-5',
                 'note': 'WTI-BC-4 and WTI-VSTB-2 时会触发WTI-BC-5, 单独报WTI-BC-5也会落库'},
                {'name': 'WTI-EP-12', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-EP-12',
                 'note': 'WTI-EP-5 and WTI-EP-9 时会触发WTI-EP-12, 单独报WTI-EP-12也会落库'},
                {'name': 'WTI-EP-4', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-EP-4',
                 'note': 'WTI-EP-4 and WTI-EP-8 时会触发WTI-EP-11, 单独报WTI-EP-11也会落库, name为WTI-EP-4也会落库'},
                {'name': 'WTI-EP-11', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-EP-11',
                 'note': 'WTI-EP-4 and WTI-EP-8 时会触发WTI-EP-11, 单独报WTI-EP-11也会落库'},
                {'name': 'WTI-EP-5', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-EP-9',
                 'note': 'WTI-EP-5 and WTI-EP-9 时会触发WTI-EP-12, 单独报WTI-EP-12也会落库, name为WTI-EP-5也会落库'},
                {'name': 'WTI-EP-8', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-EP-8',
                 'note': 'WTI-EP-4 and WTI-EP-8 时会触发WTI-EP-11, 单独报WTI-EP-11也会落库, name为WTI-EP-8也会落库'},
                {'name': 'WTI-EP-9', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-EP-9',
                 'note': 'WTI-EP-5 and WTI-EP-9 时会触发WTI-EP-12, 单独报WTI-EP-12也会落库, name为WTI-EP-9也会落库'},
                {'name': 'WTI-PA-17', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-PA-17',
                 'note': 'WTI-PA-17 and WTI-PA-18 时会触发WTI-PA-16, 单独报WTI-PA-16也会落库, name为WTI-PA-17也会落库'},
                {'name': 'WTI-PA-18', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-PA-18',
                 'note': 'WTI-PA-17 and WTI-PA-18 时会触发WTI-PA-16, 单独报WTI-PA-16也会落库, name为WTI-PA-18也会落库'},
                {'name': 'WTI-PA-16', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-PA-16',
                 'note': 'WTI-PA-17 and WTI-PA-18 时会触发WTI-PA-16, 单独报WTI-PA-16也会落库'},
                {'name': 'WTI-VSTB-2', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-VSTB-2',
                 'note': 'WTI-BC-4 and WTI-VSTB-2 时会触发WTI-BC-5, 其name值可以为VDCTCSFailLampReq 或 WTI-VSTB-2'},
                {'name': 'WTI-VSTS-1', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-VSTS-1',
                 'note': '报CGWSwtPwrFailSts = 1 and VehState = 1( Driver Present)会触发WTI-VSTS-1, 单独报WTI-VSTS-1也会落库'},
                {'name': 'WTI-VSTS-2', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-VSTS-2',
                 'note': '报CGWSwtPwrFailSts = 1 and VehState= 2 (Driving)会触发WTI-VSTS-2, 单独报WTI-VSTS-2也会落库'},
                {'name': 'WTI-CHRG-5', 'value': 1, 'alarm_level': 4, 'wti_code': 'WTI-CHRG-5',
                 'note': 'ACChrgrOverT=1 or DCChrgrOverT=1 时会触发WTI-CHRG-5, 单独报WTI-CHRG-5也会落库'},
            ]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_all}, sleep_time=5)

            tables = ['status_wti_alarm', 'history_wti_alarm']
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_all)

    def test_wti_evm_11_and_12(self, vid, vin, publish_msg_by_kafka, checker, prepare):
        with allure.step('校验 name:WTI-EVM-11,value>136被解析为WTI-EVM-11'):
            signal_all = [
                {'name': 'WTI-EVM-11', 'value': [136, 138], 'alarm_level': 1, 'evm_alarm_level': 1,
                 'wti_code': 'WTI-EVM-11',
                 'note': 'name:WTI-EVM-11,value>136被解析为WTI-EVM-11; name:DCDCHotSpotTemp,value>120被解析为为WTI-EVM-12'},
            ]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_all}, sleep_time=2)

            tables = ['status_wti_alarm', 'history_wti_alarm']
            time.sleep(5)
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_all)

        with allure.step('校验 name:DCDCHotSpotTemp,value>120的报警会被解析为WTI-EVM-12'):
            signal_all = [
                {'name': 'DCDCHotSpotTemp', 'value': [121, 136], 'alarm_level': 1, 'evm_alarm_level': 1,
                 'wti_code': 'WTI-EVM-12',
                 'note': 'name:WTI-EVM-11,value>136被解析为WTI-EVM-11; name:DCDCHotSpotTemp,value>120被解析为为WTI-EVM-12'},
            ]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_all}, sleep_time=2)
            time.sleep(5)
            tables = ['status_wti_alarm', 'history_wti_alarm']
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_all)

    def test_wti_evm_13_and_14(self, vid, vin, publish_msg_by_kafka, checker, prepare):
        with allure.step('校验 name:WTI-EVM-13,value>90被解析为WTI-EVM-13'):
            signal_all = [
                {'name': 'WTI-EVM-13', 'value': [91, 96, 101], 'alarm_level': 1, 'evm_alarm_level': 1,
                 'wti_code': 'WTI-EVM-13',
                 'note': 'name:WTI-EVM-13,value>90被解析为WTI-EVM-13; name:DCDCCoolantTemp,value>95会被解析为WTI-EVM-14; name:DCDCCoolantTemp,90<value<=95不再被解析为报警'},
            ]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_all}, sleep_time=2)

            # 校验EVM-EVM-13会落库
            time.sleep(5)
            tables = ['status_wti_alarm', 'history_wti_alarm']
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_all)

            # 校验WTI-EVM-14不会出现
            time.sleep(5)
            status_wti_alarm_mysql = checker.mysql.fetch('status_wti_alarm', {"id": vid, 'wti_code': 'WTI-EVM-14'},
                                                         exclude_fields=['update_time'])[0]
            assert_equal(status_wti_alarm_mysql['alarm_level'], 0)

        with allure.step('校验 name:DCDCCoolantTemp,value>95会被解析为WTI-EVM-14'):
            signal_all = [
                {'name': 'DCDCCoolantTemp', 'value': [96, 101], 'alarm_level': 1, 'evm_alarm_level': 1,
                 'wti_code': 'WTI-EVM-14',
                 'note': 'name:WTI-EVM-13,value>90被解析为WTI-EVM-13; name:DCDCCoolantTemp,value>95会被解析为WTI-EVM-14; name:DCDCCoolantTemp,90<value<=95不再被解析为报警'},
            ]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_all}, sleep_time=2)
            time.sleep(5)
            tables = ['status_wti_alarm', 'history_wti_alarm']
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_all)

        with allure.step('校验 name:DCDCCoolantTemp,90<value<=95不再被解析为报警'):
            signal_all = [
                {'name': 'DCDCCoolantTemp', 'value': [91, 95], 'alarm_level': 1, 'evm_alarm_level': 1,
                 'wti_code': 'WTI-EVM-13',
                 'note': 'name:WTI-EVM-13,value>90被解析为WTI-EVM-13; name:DCDCCoolantTemp,value>95会被解析为WTI-EVM-14; name:DCDCCoolantTemp,90<value<=95不再被解析为报警'},
            ]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_all}, sleep_time=2)
            time.sleep(5)
            status_wti_alarm_mysql = checker.mysql.fetch('status_wti_alarm', {"id": vid, 'wti_code': 'WTI-EVM-13'},
                                                         exclude_fields=['update_time'])[0]
            assert_equal(status_wti_alarm_mysql['alarm_level'], 0)

    def test_end_time_is_sample_ts(self, vin, vid, publish_msg_by_kafka, checker):
        """
        验证故障结束时间从publish_ts改为 sample_ts
        """
        # here we want to choose alarm which is wti_enabled
        signal_int = []
        while True:
            s = random.choice(wti.SIGNAL)
            # 带note标记的都是比较特殊的wti，此处随机选一个的时候不选它
            if 'note' in s:
                continue
            is_wti_enabled = checker.mysql.fetch('const_wti',
                                                 where_model={"wti_code": s['wti_code']},
                                                 fields=['wti_enabled'])[0]['wti_enabled']
            if is_wti_enabled == 0:
                continue

            signal_int.append(s)
            break

        nextev_message, obj_start = publish_msg_by_kafka('alarm_signal_update_event',
                                                         alarm_signal={'signal_int': signal_int}, sleep_time=2)

        # 清除WTI
        nextev_message, obj_end = publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []},
                                                       sleep_time=2)
        with allure.step('校验故障结束时间为结束事件的sample_ts'):
            sn = obj_start['alarm_signal']['signal_int'][0]['sn']
            alarm_id = '{}-{}-{}-WTI'.format(vin, sn, signal_int[0]['wti_code'][4:])
            end_time = checker.mysql.fetch('history_wti_alarm', {"vehicle_id": vid, 'alarm_id': alarm_id},
                                           suffix=' and `end_time` is not NULL')[0]['end_time']
            assert_equal(end_time, timestamp_to_utc_strtime(obj_end['sample_ts']))

    def test_WTI_SA(self, publish_msg_by_kafka, checker, prepare):
        """
        cgw会在BL270改变wti信号名:EPSWarnLampReq -> EPS_WarnLampReq
        由于旧版本信号会同时存在，对WTI-SA-1、WTI-SA-2和WTI-SA-3做版本兼容，两种信号都支持（Slytherin本身并不会去校验车辆版本，监测到这两种信号直接落库）
        """
        with allure.step('校验EPSWarnLampReq、EPS_WarnLampReq，两种信号都可以正常落库'):
            signal_all = [
                {'name': 'EPSWarnLampReq', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-SA-1',
                 'note': '互斥 WTI-SA-1, WTI-SA-2, WTI-SA-3'},
                {'name': 'EPS_WarnLampReq', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-SA-1',
                 'note': '互斥 WTI-SA-1, WTI-SA-2, WTI-SA-3'},
                {'name': 'EPSWarnLampReq', 'value': 2, 'alarm_level': 1, 'wti_code': 'WTI-SA-2',
                 'note': '互斥 WTI-SA-1, WTI-SA-2, WTI-SA-3'},
                {'name': 'EPS_WarnLampReq', 'value': 2, 'alarm_level': 1, 'wti_code': 'WTI-SA-2',
                 'note': '互斥 WTI-SA-1, WTI-SA-2, WTI-SA-3'},
                {'name': 'EPSWarnLampReq', 'value': 3, 'alarm_level': 1, 'wti_code': 'WTI-SA-3',
                 'note': '互斥 WTI-SA-1, WTI-SA-2, WTI-SA-3'},
                {'name': 'EPS_WarnLampReq', 'value': 3, 'alarm_level': 1, 'wti_code': 'WTI-SA-3',
                 'note': '互斥 WTI-SA-1, WTI-SA-2, WTI-SA-3'},
                {'name': 'WTI-SA-3', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-SA-3',
                 'note': '互斥 WTI-SA-1, WTI-SA-2, WTI-SA-3'},
            ]
            signal_int = [random.choice(signal_all)]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_int}, sleep_time=2)
            time.sleep(5)
            tables = ['status_wti_alarm', 'history_wti_alarm']
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                       extra=signal_int)

    @pytest.mark.skip('manual')
    def test_history_battery_alarm(self, kafka, publish_msg_by_kafka):
        """
        * history_battery_alarm表用于记录电池故障信息

        * device_type 定义了如下几种电池来源
            0= invalid device, 1 = vehicle, 2 = power_swap, 3 = power_mobile  4 = power_energy_storage_station

            device_type=1 通过车机上报电池相关的wti触发。电池相关wti即const_wti.ecu=BMS

            device_type=2|3|4 这几种可以通过电池告警平台提供的接口来触发，然后告警平台推送到topic：swc-sas-bordercollie-test-battery-alarm被Slytherin消费落库

        * VMS将使用history_battery_alarm表数据。在 故障管理-电池故障 页面


        case:
        1. 上报存在的bid电池告警事件且device_type=2|3|4，history_battery_alarm表存储正常，detail_status更新数据,detail_status的数据来自于接口/trident/v1/in/bordercollie/battery_status。
            * detail_status字段数据来自电池历史状态信息接口，时间范围为trigger_time的前2后20秒，接口没有返回值时，detail_status置为空
                /trident/v1/in/bordercollie/battery_status
                http://showdoc.nevint.com/index.php?s=/96&page_id=9710 smart-vehicle

            * history_battery_alarm表 end_time为空。直到上报一条peoss_alarm_inactive

        2. 验证device_type=2|3|4时，多次上报active报警（即trigger_time不同，msg_type=peoss_alarm_active）时，表中会插入多条记录

        3. 验证device_type=2|3|4时，上报不存在的bid告警事件，history_battery_alarm表能插入数据，但detail_status字段数据为空

        4. 验证来自topic：swc-sas-bordercollie-test-battery-alarm 且device_type=vehicle的电池报警数据时，不存储到history_battery_alalrm表

        5. 验证车机上报const_wti.ecu=BMS的wti,会存储到history_battery_alarm表
            * alarm/journey_update/charge_update上报的wti都可以落库
            * 和device_type=2|3|4不同，同一wti不会多次插入表
            * 上报不同的wti时，会关闭前面未结束的wti

        6. 验证PE电池报警device_type为储能站（power_energy_storage_station）时，不存储位置数据

        7. 验证device_type=2|3|4，当上报一条inactive（即msg_type: peoss_alarm_inactive）告警时，close之前所有的同类故障



        """
        # device_type=2|3|4，kafka mock数据
        data = json.dumps(
            {
                "alarm_name": "BMSCellVoltageOverUnder",
                "alarm_value_str": 1,
                "nio_bid": "P0079340AA039180061300001B33152",
                "gb_bid": "",
                "trigger_time": 1594957883124,
                "trigger_type": 3,
                "longitude": 104.5083850087,
                "latitude": 29.8468341966,
                "msg_type": "peoss_alarm_active",
                "device_type": "power_mobile",
                "device_id": "PS-NIO-3b6e91a0-7fca77cb"
            }

        )
        kafka['comn_for_battery_alarm'].produce(kafka['topics']['battery_alarm'], data)

        # device_type=1, 车机上报数据
        signal_all = [
            {'name': 'BMSCellVoltageOverUnder', 'value': 1, 'alarm_level': 1, 'wti_code': 'WTI-EVM-4'},
        ]

        publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': signal_all}, sleep_time=2)

    def test_alarm_signal_update_by_index(self, vid, vin, publish_msg_by_kafka, checker, prepare):
        signal_name = random.choice(index_names)
        # here we want to traversal all wti report with index
        s = list(filter(lambda x: x['name'] == signal_name, wti.SIGNAL))

        is_wti_enabled = checker.mysql.fetch('const_wti',
                                             where_model={"wti_code": s[0]['wti_code']},
                                             fields=['wti_enabled'])[0]['wti_enabled']

        nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': s})
        tables = ['status_wti_alarm', 'history_wti_alarm']
        if is_wti_enabled == 0:
            for tt in tables:
                assert not checker.mysql.fetch('status_wti_alarm', where_model={"id": vid, 'wti_code': s[0]['wti_code']}, retry_num=5)
        else:
            checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'], extra=s)
