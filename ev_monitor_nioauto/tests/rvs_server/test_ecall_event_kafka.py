#!/usr/bin/env python
# coding=utf-8

"""
:Description: ecall事件上报校验
"""
import json
import random
import time
import allure
import pytest

from utils.assertions import assert_equal
from utils import message_formator

# TODO 马克波罗服务暂不支持，先跳过
@pytest.mark.marcopolo_skip
class TestEcallEventMsg(object):
    def test_ecall_event_kafka(self, vid, kafka, publish_msg_by_kafka, cmdopt):
        # rvs版本933.1.0.1595.c8c49c4之后，ecall事件上报除转发kafka外，还通过调hermes接口/api/1/in/hermes/ecall/register
        # 主动将ecall上报事件通知到hermes，可在本case执行完毕后，在kibana查询log验证。

        kafka['comn'].set_offset_to_end(kafka['topics']['ecall'])
        kafka['comn'].set_offset_to_end(kafka['topics']['ecall_ad'])
        # 构造并上报消息
        nextev_message, obj = publish_msg_by_kafka('ecall_event', reason_code='airbag_pump_trigger',
                                                   status={'alarm_signal': {'signal_int': [{'name': 'TpmsFrntLeWhlTempSts', 'value': 1, 'alarm_level': 2, 'wti_code': 'WTI-TPMS-21', 'description': '左前轮胎温度过高'}]}})

        # 校验
        kafka_msg = None
        is_found = False
        for data in kafka['comn'].consume(kafka['topics']['ecall'], timeout=20):
            kafka_msg = json.loads(str(data, encoding='utf-8'))
            if vid == kafka_msg['vehicle_id'] and kafka_msg['sample_time'] == obj['sample_ts']//1000:
                is_found = True
                break

        with allure.step('校验数据推送到了swc-cvs-tsp-{0}-80001-ecall'.format(cmdopt)):
            assert_equal(True, is_found)
            formator = message_formator.MessageFormator(vid, sample_ts=obj['sample_ts'])

            ecall_status = obj['status']
            event_id = obj['event_id'] // 1000
            reason_code = obj['reason_code']
            alarm_signal = obj['status']['alarm_signal']
            window_in_mysql = None
            door_in_mysql = None
            ecall_event_in_message = formator.to_mysql_ecall_event(ecall_status=ecall_status,
                                                                   event_id=event_id,
                                                                   reason_code=reason_code,
                                                                   alarm_signal=alarm_signal,
                                                                   window_mysql=window_in_mysql,
                                                                   door_mysql=door_in_mysql
                                                                   )


            # sorted the tyre_alarm list
            kafka_msg['ecall_data']['tyre_alarm'] = sorted(kafka_msg['ecall_data']['tyre_alarm'], key=lambda k: k['wti_code'])
            ecall_event_in_message['ecall_data']['tyre_alarm'] = sorted(ecall_event_in_message['ecall_data']['tyre_alarm'], key=lambda k: k['wti_code'])

            ecall_event_in_message['sample_time'] = obj['sample_ts']//1000
            assert_equal(kafka_msg, ecall_event_in_message)

        with allure.step('校验数据推送到了swc-cvs-tsp-{0}-80001-ecall-ad'.format(cmdopt)):
            # http://showdoc.nevint.com/index.php?s=/11&page_id=33558
            # 气囊弹出 ecall同时会转发到swc-cvs-tsp-${env}-80001-ecall-ad
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['ecall_ad'], timeout=20):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if vid == kafka_msg['vehicle_id']:
                    is_found = True
                    ecall_event_in_message.pop('reason_code')
                    ecall_event_in_message.pop('channel')
                    ecall_event_in_message.pop('vehicle_identity')
                    ecall_event_in_message['data'] = ecall_event_in_message.pop('ecall_data')
                    assert_equal(kafka_msg, ecall_event_in_message)
                    break
            assert is_found

    def test_window_status_rule_kafka(self, env, kafka, publish_msg_by_kafka, cmdopt, mysql):
        with allure.step('校验ES6遵循新的车窗状态映射规则'):
            kafka['comn'].set_offset_to_end(kafka['topics']['ecall'])
            vin = env['vehicles']['v_ES6']['vin']
            vid = env['vehicles']['v_ES6']['vehicle_id']
            status = {
                "window_status": {
                    "sun_roof_positions": {
                        "sun_roof_posn": random.choice([random.randint(0, 102), 127])
                    }
                }
            }
            # 构造并上报消息
            nextev_message, obj = publish_msg_by_kafka('ecall_event', vin=vin, vid=vid, status=status)

            # 校验
            kafka_msg = None
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['ecall'], timeout=20):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if vid == kafka_msg['vehicle_id'] and kafka_msg['sample_time'] == obj['sample_ts']//1000:
                    is_found = True
                    break

            with allure.step('校验数据推送到了swc-cvs-tsp-{0}-80001-ecall'.format(cmdopt)):
                assert_equal(True, is_found)
                formator = message_formator.MessageFormator(vid, sample_ts=obj['sample_ts'])

                ecall_status = obj['status']
                event_id = obj['event_id'] // 1000
                reason_code = obj['reason_code']
                alarm_signal = obj['status']['alarm_signal']
                window_in_mysql = None
                door_in_mysql = None
                vehicle_model = mysql['rvs'].fetch('vehicle_profile', {"id": vid}, fields=['model_type', 'model_type_year'])[0]
                model_type = vehicle_model['model_type']
                model_type_year = vehicle_model['model_type_year']
                ecall_event_in_message = formator.to_mysql_ecall_event(ecall_status=ecall_status,
                                                                       event_id=event_id,
                                                                       reason_code=reason_code,
                                                                       alarm_signal=alarm_signal,
                                                                       window_mysql=window_in_mysql,
                                                                       door_mysql=door_in_mysql,
                                                                       model_type=model_type,
                                                                       model_type_year=model_type_year
                                                                       )


                # sorted the tyre_alarm list
                kafka_msg['ecall_data']['tyre_alarm'] = sorted(kafka_msg['ecall_data']['tyre_alarm'], key=lambda k: k['wti_code'])
                ecall_event_in_message['ecall_data']['tyre_alarm'] = sorted(ecall_event_in_message['ecall_data']['tyre_alarm'], key=lambda k: k['wti_code'])

                ecall_event_in_message['sample_time'] = obj['sample_ts']//1000
                assert_equal(kafka_msg, ecall_event_in_message)

        with allure.step('校验新款ES8遵循新的车窗状态映射规则'):
            vin = env['vehicles']['v_new_ES8']['vin']
            vid = env['vehicles']['v_new_ES8']['vehicle_id']
            status = {
                "window_status": {
                    "sun_roof_positions": {
                        "sun_roof_posn": random.choice([random.randint(0, 102), 127])
                    }
                }
            }
            # 构造并上报消息
            # nextev_message, obj = publish_msg_by_kafka('ecall_event',sample_ts=prepare['sample_ts'])
            nextev_message, obj = publish_msg_by_kafka('ecall_event', vin=vin, vid=vid, status=status)

            # 校验
            kafka_msg = None
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['ecall'], timeout=20):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if vid == kafka_msg['vehicle_id'] and kafka_msg['sample_time'] == obj['sample_ts'] // 1000:
                    is_found = True
                    break

            with allure.step('校验数据推送到了swc-cvs-tsp-{0}-80001-ecall'.format(cmdopt)):
                    assert_equal(True, is_found)
                    formator = message_formator.MessageFormator(vid, sample_ts=obj['sample_ts'])

                    ecall_status = obj['status']
                    event_id = obj['event_id'] // 1000
                    reason_code = obj['reason_code']
                    alarm_signal = obj['status']['alarm_signal']
                    window_in_mysql = None
                    door_in_mysql = None
                    vehicle_model = mysql['rvs'].fetch('vehicle_profile', {"id": vid}, fields=['model_type', 'model_type_year'])[0]
                    model_type = vehicle_model['model_type']
                    model_type_year = vehicle_model['model_type_year']
                    ecall_event_in_message = formator.to_mysql_ecall_event(ecall_status=ecall_status,
                                                                           event_id=event_id,
                                                                           reason_code=reason_code,
                                                                           alarm_signal=alarm_signal,
                                                                           window_mysql=window_in_mysql,
                                                                           door_mysql=door_in_mysql,
                                                                           model_type=model_type,
                                                                           model_type_year=model_type_year
                                                                           )

                    # sorted the tyre_alarm list
                    kafka_msg['ecall_data']['tyre_alarm'] = sorted(kafka_msg['ecall_data']['tyre_alarm'], key=lambda k: k['wti_code'])
                    ecall_event_in_message['ecall_data']['tyre_alarm'] = sorted(ecall_event_in_message['ecall_data']['tyre_alarm'], key=lambda k: k['wti_code'])

                    ecall_event_in_message['sample_time'] = obj['sample_ts'] // 1000
                    assert_equal(kafka_msg, ecall_event_in_message)

        with allure.step('校验ecall事件中不包含天窗状态'):
            '''
            http://venus.nioint.com/#/detailWorkflow/wf-20220413172931-Yi
            '''
            time.sleep(62)
            vin = env['vehicles']['v_new_ES8']['vin']
            vid = env['vehicles']['v_new_ES8']['vehicle_id']
            # 构造并上报消息
            nextev_message, obj = publish_msg_by_kafka('ecall_event', vin=vin, vid=vid,
                                                       clear_fields=['status.window_status.sun_roof_positions.sun_roof_posn'])

            # 校验
            kafka_msg = None
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['ecall'], timeout=20):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if vid == kafka_msg['vehicle_id'] and kafka_msg['sample_time'] == obj['sample_ts'] // 1000:
                    is_found = True
                    break

            with allure.step('校验数据推送到了swc-cvs-tsp-{0}-80001-ecall'.format(cmdopt)):
                assert_equal(True, is_found)
                assert 'sun_roof_posn' not in kafka_msg

    def test_interval_is_one_min(self, vid, kafka, publish_msg_by_kafka, cmdopt):
        """
        校验第一次上报与第二次上报的间隔在一分钟以内时，上报数据被忽略，不推送到kafka, event_id 代表时间戳（秒计）为判定依据
        交替不同的result reason时，也有一分钟限制。
        urgt_prw_shtdwn从0变为1时，也有一分钟的限制。

        注意，当上报的event_id不以当前时间来取值时（例如取的是昨天的某两个时间点，之间相差一直有1秒），rvs认为它是补发数据，此时没有一分钟的限制。该两条数据都会落库。
        此时kafka的推送也没有一分钟限制
        """
        kafka['comn'].set_offset_to_end(kafka['topics']['ecall'])
        sample_ts = round(time.time() * 1000)

        with allure.step('第一次上报，验证推送到了kafka'):
            nextev_message, obj = publish_msg_by_kafka('ecall_event', sample_ts=sample_ts, event_id=sample_ts)
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['ecall'], timeout=2 if cmdopt == 'test' else 30):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if vid == kafka_msg['vehicle_id'] and kafka_msg['sample_time'] == obj['sample_ts'] // 1000:
                    is_found = True
                    break
                elif kafka_msg['sample_time'] * 1000 > obj['sample_ts'] + 10000:
                    break
            assert is_found is True

        with allure.step('第二次上报，距离第一次的时间小于一分钟，验证数据没有推送到kafka'):
            # 第二次上报比第一次间隔3秒
            sample_ts = sample_ts + 3*1000
            nextev_message, obj = publish_msg_by_kafka('ecall_event', sample_ts=sample_ts, event_id=sample_ts)
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['ecall'], timeout=2 if cmdopt == 'test' else 30):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                if vid == kafka_msg['vehicle_id'] and kafka_msg['sample_time'] == obj['sample_ts'] // 1000:
                    is_found = True
                    break
                elif kafka_msg['sample_time'] * 1000 > obj['sample_ts'] + 10000:
                    break
            assert is_found is False
