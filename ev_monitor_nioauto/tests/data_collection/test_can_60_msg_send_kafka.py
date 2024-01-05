""" 
@author:dun.yuan
@time: 2022/3/4 3:51 PM
@contact: dun.yuan@nio.com
@description: 在data_collection_server中，将上报消息中气囊can消息解析后发送到can_60 topic
@showdoc：http://showdoc.nevint.com/index.php?s=/datacollection&page_id=33217
"""
import allure
import json
import pytest
from utils.assertions import assert_equal


class TestCan60SendKafka(object):
    # 构造带can_id=60的信号并上报消息
    @pytest.mark.parametrize('event_name', ['periodical_charge_update', 'periodical_journey_update'])
    def test_report_can60_msg_with_periodical_update(self, publish_msg_by_kafka, kafka, vid, event_name):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['can_60'])

        with allure.step('上报携带canid=60消息的事件：' + event_name):
            nextev_message, obj = publish_msg_by_kafka(event_name,
                                                       sample_points=[{
                                                           'can_msg': {
                                                               'can_data': [
                                                                   {
                                                                       'msg_id': 60,
                                                                       'value': b'\xff\xff\xff\xff'
                                                                   }
                                                               ]
                                                           }}])
        msg = None
        expect_msg = {
            'vehicle_id': vid,
            'sample_ts': obj['sample_points'][0]['sample_ts'],
            'type': event_name,
            'can': [{
                'can_id': 60,
                'can_value': {'CrashDetd': 1}
            }]
        }
        for data in kafka['comn'].consume(kafka['topics']['can_60'], timeout=10):
            msg = json.loads(data.decode())
            if vid == msg['vehicle_id']:
                msg.pop('process_id')
                assert_equal(msg, expect_msg)
                return
        assert False

    def test_report_can60_msg_with_alarm(self, publish_msg_by_kafka, kafka, vid):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['can_60'])

        with allure.step('上报携带canid=60消息的事件：'):
            nextev_message, obj = publish_msg_by_kafka('alarm_signal_update_event',
                                                       sample_points={
                                                           'can_msg': {
                                                               'can_data': [
                                                                   {
                                                                       'msg_id': 60,
                                                                       'value': b'\xff\xff\xff\xff'
                                                                   }
                                                               ]
                                                           }})
        msg = None
        expect_msg = {
            'vehicle_id': vid,
            'sample_ts': obj['sample_ts'],
            'type': 'alarm_signal_update_event',
            'can': [{
                'can_id': 60,
                'can_value': {'CrashDetd': 1}
            }]
        }
        for data in kafka['comn'].consume(kafka['topics']['can_60'], timeout=10):
            msg = json.loads(data.decode())
            if vid == msg['vehicle_id']:
                assert_equal(msg, expect_msg)
                return
        assert False

    def test_report_can60_msg_with_instant(self, publish_msg_by_kafka, kafka, vid):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['can_60'])

        with allure.step('上报携带canid=60消息的事件：'):
            nextev_message, obj = publish_msg_by_kafka('instant_status_resp',
                                                       sample_point={
                                                           'can_msg': {
                                                               'can_data': [
                                                                   {
                                                                       'msg_id': 60,
                                                                       'value': b'\xff\xff\xff\xff'
                                                                   }
                                                               ]
                                                           }})
        msg = None
        expect_msg = {
            'vehicle_id': vid,
            'sample_ts': obj['sample_point']['sample_ts'],
            'type': 'instant_status_resp',
            'can': [{
                'can_id': 60,
                'can_value': {'CrashDetd': 1}
            }]
        }
        for data in kafka['comn'].consume(kafka['topics']['can_60'], timeout=10):
            msg = json.loads(data.decode())
            if vid == msg['vehicle_id']:
                assert_equal(msg, expect_msg)
                return
        assert False

    def test_report_can60_msg_with_lv(self, publish_msg_by_kafka, kafka, vid):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['can_60'])

        with allure.step('上报携带canid=60消息的事件：'):
            nextev_message, obj = publish_msg_by_kafka('lv_batt_charging_event',
                                                       can_msg={
                                                           'can_data': [
                                                               {
                                                                   'msg_id': 60,
                                                                   'value': b'\xff\xff\xff\xff'
                                                               }]})
        msg = None
        expect_msg = {
            'vehicle_id': vid,
            'sample_ts': obj['sample_ts'],
            'type': 'lv_batt_charging_event',
            'can': [{
                'can_id': 60,
                'can_value': {'CrashDetd': 1}
            }]
        }
        for data in kafka['comn'].consume(kafka['topics']['can_60'], timeout=10):
            msg = json.loads(data.decode())
            if vid == msg['vehicle_id']:
                assert_equal(msg, expect_msg)
                return
        assert False

    @pytest.mark.parametrize('event_name', ['periodical_charge_update', 'periodical_journey_update'])
    def test_report_can60_msg_with_periodical_update_filtered(self, publish_msg_by_kafka, kafka, vid, event_name):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['can_60'])

        # 只有2个update事件会过滤wti，instant和alarm事件不会过滤
        with allure.step(
                '过滤evm_flag =false&&alarm_signal只有这个CAM_FC_03:LKSTakeoverReq信号 && vehicle_status.vehl_state = 1'):
            signal_all = [
                {"name": "CAM_FC_03:LKSTakeoverReq", "value": 1, "alarm_level": 4, "wti_code": "WTI-158"},
            ]
            nextev_message, obj = publish_msg_by_kafka(event_name,
                                                       sample_points=[{'alarm_signal': {'signal_int': signal_all},
                                                                       'vehicle_status': {'vehl_state': 1},
                                                                       'can_msg': {
                                                                           'can_data': [
                                                                               {
                                                                                   'msg_id': 60,
                                                                                   'value': '00000000'
                                                                               }
                                                                           ]
                                                                       },
                                                                       'evm_flag': False}])
        msg = None
        for data in kafka['comn'].consume(kafka['topics']['can_60'], timeout=10):
            print(data.decode())
            msg = json.loads(data.decode())
            if vid == msg['vehicle_id'] and msg['can'][0]['can_id'] == 60:
                assert False
        assert True

        with allure.step('过滤evm_flag =false&&alarm_signal只有这个VCU_CGW_219:VCUChgLineSts信号 && 充电状态中即chrg_state=1'):
            signal_all = [
                {"name": "VCU_CGW_219:VCUChgLineSts", "value": 1, "alarm_level": 4, "wti_code": "WTI-43"},
            ]
            nextev_message, obj = publish_msg_by_kafka(event_name,
                                                       sample_points=[{'alarm_signal': {'signal_int': signal_all},
                                                                       'soc_status': {'chrg_state': 1},
                                                                       'can_msg': {
                                                                           'can_data': [
                                                                               {
                                                                                   'msg_id': 60,
                                                                                   'value': '00000000'
                                                                               }
                                                                           ]
                                                                       },
                                                                       'evm_flag': False}])
        for data in kafka['comn'].consume(kafka['topics']['can_60'], timeout=10):
            print(data.decode())
            msg = json.loads(data.decode())
            if vid == msg['vehicle_id'] and msg['can'][0]['can_id'] == 60:
                assert False
        assert True
