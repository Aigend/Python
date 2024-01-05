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
import time
import allure
import pytest
from nio_messages import wti
from utils.assertions import assert_equal

index_names = ['WTI-BMS-2', 'WTI-BMS-4', 'WTI-EP-15', 'WTI-EP-17', 'WTI-EP-2', 'WTI-BC-6', 'WTI-BMS-3', 'WTI-BSD-1',
               'WTI-FCTA-1', 'WTI-FCTA-2', 'WTI-SA-1', 'WTI-BMS-8', 'WTI-CT-1','WTI-CT-2','WTI-CT-3','WTI-PA-15',
               'WTI-TPMS-28', 'WTI-TPMS-27', 'WTI-TPMS-26', 'WTI-TPMS-25', 'WTI-SCM-1', 'WTI-VSTS-7', 'WTI-VSTS-8',
               'WTI-SB-1', 'WTI-LGHT-65', 'WTI-LGHT-66', 'WTI-ADAS-11','WTI-SA-7','WTI-SA-8','WTI-SA-9','WTI-SA-10',
               'WTI-PBRK-7','WTI-PBRK-8','WTI-PBRK-12','WTI-PBRK-13','WTI-PBRK-14']


@pytest.mark.marcopolo_skip
class TestAlarmSignalUpdateMSG(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, publish_msg_by_kafka):
        # 清空wti
        publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []}, sleep_time=4)

    @pytest.mark.marcopolo_skip
    def test_alarm_signal_update_to_kafka(self, vid, vin, prepare, kafka, publish_msg_by_kafka, checker):
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

    @pytest.mark.marcopolo_skip
    def test_alarm_signal_update_to_artemis(self, vid, vin, prepare, kafka, publish_msg_by_kafka, checker):
        """
        alarm_signal_update_event中, WTI推送topic中增加胎压的状态 http://showdoc.nevint.com/index.php?s=/11&page_id=22907
        供Artemis消费
        :param vid:
        :param vin:
        :param prepare:
        :param kafka:
        :param publish_msg_by_kafka:
        :param checker:
        :return:
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

        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['wti_data'])
        # 构造并上报消息
        nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': signal_int},
                                                   sleep_time=2)

        # 校验kafka
        kafka_msg = None
        is_found = False
        for data in kafka['comn'].consume(kafka['topics']['wti_data'], timeout=10):
            kafka_msg = json.loads(str(data, encoding='utf-8'))
            if kafka_msg['sample_time'] == obj['sample_ts'] and vid == kafka_msg['vehicle_id']:
                is_found = True
                break
        with allure.step('校验 {}'.format(kafka['topics']['wti_data'])):
            assert_equal(is_found, True)
            assert kafka_msg['type'] == 1
            wti_mysql = checker.mysql.fetch_one('status_wti_alarm',
                                                where_model={'id': vid, 'wti_code': s['wti_code']},
                                                fields=['wti_code', 'alarm_id', 'can_sn as sn'],
                                                order_by=' can_sn desc')
            assert_equal(kafka_msg['wti_info'][0], wti_mysql)
            assert kafka_msg['wti_entity']['soc'] == obj['sample_points']['soc_status']['soc']
            assert kafka_msg['wti_entity']['chrg_sts'] == obj['sample_points']['soc_status']['chrg_state']
            assert kafka_msg['wti_entity']['vehl_sts'] == obj['sample_points']['vehicle_status']['vehl_state']
            assert kafka_msg['wti_entity']['tyre_status']['front_left_wheel_press'] == round(obj['sample_points']['tyre_status']['frnt_le_whl_press'], 3)
            assert kafka_msg['wti_entity']['tyre_status']['front_left_wheel_temp'] == round(obj['sample_points']['tyre_status']['frnt_le_whl_temp'], 3)
            assert kafka_msg['wti_entity']['tyre_status']['front_right_wheel_press'] == round(obj['sample_points']['tyre_status']['frnt_ri_whl_press'], 3)
            assert kafka_msg['wti_entity']['tyre_status']['front_right_wheel_temp'] == round(obj['sample_points']['tyre_status']['frnt_ri_whl_temp'], 3)
            assert kafka_msg['wti_entity']['tyre_status']['rear_left_wheel_press'] == round(obj['sample_points']['tyre_status']['re_le_whl_press'], 3)
            assert kafka_msg['wti_entity']['tyre_status']['rear_left_wheel_temp'] == round(obj['sample_points']['tyre_status']['re_le_whl_temp'], 3)
            assert kafka_msg['wti_entity']['tyre_status']['rear_right_wheel_press'] == round(obj['sample_points']['tyre_status']['re_ri_whl_press'], 3)
            assert kafka_msg['wti_entity']['tyre_status']['rear_right_wheel_temp'] == round(obj['sample_points']['tyre_status']['re_ri_whl_temp'], 3)

        # 清空wti
        nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': []}, sleep_time=4)

        is_found = False
        for data in kafka['comn'].consume(kafka['topics']['wti_data'], timeout=10):
            kafka_msg = json.loads(str(data, encoding='utf-8'))
            if kafka_msg['sample_time'] == obj['sample_ts'] and vid == kafka_msg['vehicle_id']:
                is_found = True
                break
        with allure.step('校验 {}'.format(kafka['topics']['wti_data'])):
            assert_equal(is_found, True)
            assert kafka_msg['type'] == 0
            wti_mysql = checker.mysql.fetch_one('status_wti_alarm',
                                                where_model={'id': vid, 'wti_code': s['wti_code']},
                                                fields=['wti_code', 'alarm_id', 'can_sn as sn'],
                                                order_by=' can_sn desc')
            assert_equal(kafka_msg['wti_info'][0], wti_mysql)
            assert 'wti_entity' not in kafka_msg

    def test_ntester(self, publish_msg_by_kafka, kafka, vid):
        """
        ntester取alarm事件或update事件所带的ntester,如果vehicle_status没有带ntester字段则默认为false。
        如果vehicle_status整个都没有上报则取redis或mysql的值.优先级：小于10min的redis remote_vehicle_test:vehicle_status:{vid}:ExteriorStatus --> mysql status_vehicle

        """
        with allure.step('校验wti_can_signal kafka中包含正确的 ntester信息'):

            signal_int = [{'name': 'TpmsFrntLeWhlPressSts', 'value': 2, 'alarm_level': 2, 'wti_code': 'WTI-TPMS-17',
                           'description': '左前轮胎压力低'}, ]

            # clear_fields = ['sample_points.vehicle_status']
            ntester = True
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_int},
                                                       sample_points={'vehicle_status': {'ntester': ntester}},
                                                       # clear_fields=clear_fields,
                                                       sleep_time=2)
            #
            kafka_msg = None
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['wti_can_signal'], timeout=10):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if kafka_msg['sample_time'] == obj['sample_ts'] and vid == kafka_msg['vehicle_id']:
                    is_found = True
                    break
            with allure.step('校验 {}'.format(kafka['topics']['wti_can_signal'])):
                assert_equal(is_found, True)
                assert_equal(kafka_msg['vehicle_status']['ntester'], ntester)

    @pytest.mark.marcopolo_skip
    @pytest.mark.test
    @pytest.mark.parametrize("status", [5, 10], ids=['repair start', 'repair end'])
    def test_repair(self, env, kafka, redis, status, publish_msg_by_kafka):
        # TODO 马克波罗不支持需跳过
        with allure.step("校验当有维修工单时，status=5/10代表维修开始/结束,同时kafka会推送redis中所记录的维修状态"):
            # redis: get remote_vehicle_test:vehicle_status:{vid}:SpecialStatus

            vid = env['vehicles']['vehicle_for_repair']['vehicle_id']
            vin = env['vehicles']['vehicle_for_repair']['vin']
            # 清空wti
            publish_msg_by_kafka('alarm_signal_update_event', vid=vid, vin=vin, alarm_signal={'signal_int': []},
                                 sleep_time=4)
            # 维修工单推送
            ts = int(time.time())
            '''
             按照artemis showdoc（http: // showdoc.nevint.com / index.php?s = / 222 & page_id = 10010），来生成维修工单的状态消息去推送
            '''
            vehicle_repair_order = json.dumps({
                "order_status_name": "维修开始" if status == 5 else "维修结束",
                "booking_order_no": "BSHHB00020180720001113", "ro_type": "20201002", "business_type": "21201001",
                "order_status_code": str(status), "update_at": ts, "ro_no": "BSHHB00020180720001113",
                "update_by": "用户代表",
                "vehicle_id": vid, "vin": vin,
                "order_type": "101210034", "timestamp": ts,
            })

            kafka['do'].produce(kafka['topics']['repair'], vehicle_repair_order)
            time.sleep(2)

            # 上报wti
            signal_int = [{'name': 'TpmsFrntLeWhlPressSts', 'value': 2, 'alarm_level': 2, 'wti_code': 'WTI-TPMS-17',
                           'description': '左前轮胎压力低'}, ]
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       alarm_signal={'signal_int': signal_int},
                                                       sample_points={'vehicle_status': {'ntester': False}},
                                                       vid=vid, vin=vin,
                                                       sleep_time=2)

            # kafka 校验
            kafka_msg = None
            is_found = False
            repaired_in_order = 1 if status == 5 else 0
            for data in kafka['comn'].consume(kafka['topics']['wti_can_signal'], timeout=10):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if kafka_msg['sample_time'] == obj['sample_ts'] and vid == kafka_msg['vehicle_id']:
                    is_found = True
                    break
            with allure.step('校验 {}'.format(kafka['topics']['wti_can_signal'])):
                assert_equal(is_found, True)
                assert_equal(kafka_msg['vehicle_status']['repair'], repaired_in_order)

    def test_alarm_signal_update_by_index(self, vid, vin, publish_msg_by_kafka, checker, prepare, kafka):
        signal_name = random.choice(index_names)
        # here we want to traversal all wti report with index
        s = list(filter(lambda x: x['name'] == signal_name, wti.SIGNAL))

        # wti_enabled=0仍旧会向wti_can_signal推送
        # is_wti_enabled = checker.mysql.fetch('const_wti',
        #                                      where_model={"wti_code": s[0]['wti_code']},
        #                                      fields=['wti_enabled'])[0]['wti_enabled']

        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['wti_can_signal'])

        nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event', alarm_signal={'signal_int': s},
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
