#!/usr/bin/env python
# coding=utf-8

"""
:file: test_custom_alarm_event_mysql.py
:author: liliu
:Description: 信号报警，包含国标报警和自定义报警的校验
当有alarm事件或者update事件时，如果alarm_signal有值，则往kafka里推，如果alarm_signal为空，则不推
http://showdoc.nevint.com/index.php?s=/11&page_id=9542

kafka里数据大致如下：
b'{"vehicle_status":{"repair":0,"nio_battery_id":"P0073713MK6AJR9FN1HDS7BOGLWIVUPT",
"latitude":36.64463761450727,"ntester":true,"longitude":93.87536520489121},
"vehicle_id":"4e18c0f0ab734805a802b845a02ad824","vin":"SQETEST0514819462",
"signals":[{"sn":"1572330954915","name":"TpmsFrntLeWhlPressSts","value":2}],
"sample_time":1572330954815}'

"""
import json
import random
import allure
import pytest

from nio_messages import wti
from utils.assertions import assert_equal

index_names = ['WTI-BMS-2', 'WTI-BMS-4', 'WTI-EP-15', 'WTI-EP-17', 'WTI-EP-2', 'WTI-BC-6', 'WTI-BMS-3', 'WTI-BSD-1',
               'WTI-FCTA-1', 'WTI-FCTA-2', 'WTI-SA-1', 'WTI-BMS-8',
               'WTI-TPMS-28', 'WTI-TPMS-27', 'WTI-TPMS-26', 'WTI-TPMS-25', 'WTI-SCM-1']


@pytest.mark.marcopolo_skip
class TestAlarmSignalUpdateMSG(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, publish_msg_by_kafka):
        # 清空wti
        publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []}, sleep_time=4)

    def test_alarm_signal_update_to_kafka(self, vid, vin, prepare, kafka, publish_msg_by_kafka, checker):
        # TODO 马克波罗不支持需跳过@pytest.mark.skip('marcopolo wti_can_signal topic')
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

        # 重置offset
        # TODO 需要申请topic权限，目前开发还未加，需要先增加
        kafka['comn'].set_offset_to_end(kafka['topics']['wti_can_signal'])
        # 构造并上报消息
        nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': signal_int},
                                                   sleep_time=2)

        # 校验kafka
        kafka_msg = None
        is_found = False
        for data in kafka['comn'].consume(kafka['topics']['wti_can_signal'], timeout=10):
            kafka_msg = json.loads(str(data, encoding='utf-8'))
            if kafka_msg['sample_time'] == obj['sample_ts'] and vid == kafka_msg['vehicle_id']:
                is_found = True
                break
        with allure.step('校验 {}'.format(kafka['topics']['wti_can_signal'])):
            assert_equal(is_found, True)
            checker.check_alarm_signal_kafka(obj, kafka_msg)
