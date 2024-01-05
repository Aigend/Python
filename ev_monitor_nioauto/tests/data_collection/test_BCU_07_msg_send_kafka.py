""" 
@author:dun.yuan
@time: 2020/11/9 4:11 下午
@contact: dun.yuan@nio.com
@description: data collection server BCU_07解析后发送kafka消息, 用showdoc里所列的支持上报事件类型来测试
@showdoc：http://showdoc.nevint.com/index.php?s=/datacollection&page_id=27975
"""
import allure
import json
import pytest


class TestBCU07MSGSendKafka(object):
    # 构造带can_id=94的信号并上报消息

    def test_report_bcu07_msg_with_alarm(self, vid, kafka, publish_msg):
        # 重置offset
        kafka['cvs'].set_offset_to_end(kafka['topics']['bcu_07'])

        # 上报携带canid=94消息的alarm信号
        nextev_message, alarm_signal_update = publish_msg('alarm_signal_update_event', sample_points={
            'can_msg': {
                'can_data': [
                    {
                        'msg_id': 94,
                        'value': b'00000000000000'
                    }
                ]
            }
        })

        msg = None
        for data in kafka['cvs'].consume(kafka['topics']['bcu_07'], timeout=10):
            print(data.decode())
            msg = json.loads(data.decode())
            if vid == msg['vehicle_id']:
                assert msg['type'] == 'alarm_signal_update_event'
                assert msg['can'][0]['can_id'] == 94
                return
        assert False

    @pytest.mark.parametrize('event_name', ['periodical_charge_update', 'periodical_journey_update'])
    def test_report_bcu07_msg_with_periodical_update(self, publish_msg_by_kafka, kafka, vid, event_name):
        # 重置offset
        kafka['cvs'].set_offset_to_end(kafka['topics']['bcu_07'])

        with allure.step(
                '上报携带canid=94消息的事件：'+event_name):
            nextev_message, obj = publish_msg_by_kafka(event_name,
                                                       sample_points=[{
                                                                       'can_msg': {
                                                                           'can_data': [
                                                                               {
                                                                                   'msg_id': 94,
                                                                                   'value': '00000000000000'
                                                                               }
                                                                           ]
                                                                       }}])
        msg = None
        for data in kafka['cvs'].consume(kafka['topics']['bcu_07'], timeout=10):
            print(data.decode())
            msg = json.loads(data.decode())
            if vid == msg['vehicle_id']:
                assert msg['type'] == event_name
                assert msg['can'][0]['can_id'] == 94
                return
        assert False

    def test_report_bcu07_msg_with_lv_event(self, vid, kafka, publish_msg):
        # 重置offset
        kafka['cvs'].set_offset_to_end(kafka['topics']['bcu_07'])

        # 上报携带canid=94消息的lv_event信号
        nextev_message, alarm_signal_update = publish_msg('lv_batt_charging_event', can_msg={
                'can_data': [
                    {
                        'msg_id': 94,
                        'value': b'00000000000000'
                    }
                ]
            })

        msg = None
        for data in kafka['cvs'].consume(kafka['topics']['bcu_07'], timeout=10):
            print(data.decode())
            msg = json.loads(data.decode())
            if vid == msg['vehicle_id']:
                assert msg['type'] == 'lv_batt_charging_event'
                assert msg['can'][0]['can_id'] == 94
                return
        assert False

    @pytest.mark.parametrize('event_name', ['periodical_charge_update', 'periodical_journey_update'])
    def test_report_bcu07_msg_with_periodical_update_filtered(self, publish_msg_by_kafka, kafka, vid, event_name):
        # 重置offset
        kafka['cvs'].set_offset_to_end(kafka['topics']['bcu_07'])

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
                                                                                   'msg_id': 94,
                                                                                   'value': '00000000000000'
                                                                               }
                                                                           ]
                                                                       },
                                                                       'evm_flag': False}])
        msg = None
        for data in kafka['cvs'].consume(kafka['topics']['bcu_07'], timeout=10):
            print(data.decode())
            msg = json.loads(data.decode())
            if vid == msg['vehicle_id'] and msg['can'][0]['can_id'] == 94:
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
                                                                                   'msg_id': 94,
                                                                                   'value': '00000000000000'
                                                                               }
                                                                           ]
                                                                       },
                                                                       'evm_flag': False}])
        for data in kafka['cvs'].consume(kafka['topics']['bcu_07'], timeout=10):
            print(data.decode())
            msg = json.loads(data.decode())
            if vid == msg['vehicle_id'] and msg['can'][0]['can_id'] == 94:
                assert False
        assert True
