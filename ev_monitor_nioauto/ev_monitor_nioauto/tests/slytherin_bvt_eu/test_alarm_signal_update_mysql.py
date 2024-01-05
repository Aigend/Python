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
               'WTI-FCTA-1', 'WTI-FCTA-2', 'WTI-SA-1', 'WTI-BMS-8',
               'WTI-TPMS-28', 'WTI-TPMS-27', 'WTI-TPMS-26', 'WTI-TPMS-25', 'WTI-SCM-1']


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

        nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': signal_int})

        # 校验
        tables = ['status_wti_alarm']
        checker.check_mysql_tables(obj, tables, event_name='alarm_signal_update_event', sample_ts=obj['sample_ts'],
                                   extra=signal_int)
