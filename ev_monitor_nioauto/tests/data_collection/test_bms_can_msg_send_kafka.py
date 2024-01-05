""" 
@author:dun.yuan
@time: 2020/12/2 7:01 下午
@contact: dun.yuan@nio.com
@description: data collection server bms can msg解析后发送kafka消息,遍历showdoc所列的can信号，以及用不同的事件类型来上报
         data collection版本1.0.2563.51d18c7，在上报bms can信号后，会在往下游推送的消息里加入nio battery id字段（该字段一般在充电或行程开始的时候会上报，
         存在status_btry_packs表nio_encoding字段）
@showdoc：http://showdoc.nevint.com/index.php?s=/datacollection&page_id=28372
"""
import allure
import json
import pytest
from utils.assertions import assert_equal

cans = {
    172: "BMS_VCU_AC",
    173: "BMS_VCU_AD",
    174: "BMS_VCU_AE",
    625: "BMS_VCU_271",
    626: "BMS_VCU_272",
    628: "BMS_CGW_274"
}


@pytest.mark.test
class TestBMSCANMSGSendKafka(object):
    # 构造带can_id=172,173,174,625,626,628的信号并上报消息
    def test_report_bms_msg_with_alarm(self, vid, kafka, publish_msg, checker, cmdopt):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['bms_msg'])
        can_data = []
        for key in cans:
            can_data.append({'msg_id': key,
                             'value': 'ffffffffffffffff'})
        nextev_message, alarm_signal_update = publish_msg('alarm_signal_update_event', sample_points={
            'can_msg': {
                'can_data': can_data
            }
        })

        msg = None
        expect_msg = {
            'vehicle_id': vid,
            'sample_ts': alarm_signal_update['sample_ts'],
            'can': [{
                "canName": "BMS_VCU_AE",
                "canId": 174,
                "canValue": {
                    "BMSHvConectorError": 3
                }},
                {
                    "canName": "BMS_CGW_274",
                    "canId": 628,
                    "canValue": {
                        "ISO_Performance_Index": 3,
                        "BCV_Voltage_Performance_Index": 3,
                        "BCV_Current_Com_Index": 3,
                        "CSC_Com_Index": 3,
                        "CSC_Circuitry_Index": 3,
                        "CTM_Performance_Index": 3,
                        "CVT_Performance_Index": 3
                    }
                }]
        }
        for data in kafka['comn'].consume(kafka['topics']['bms_msg'], timeout=10):
            msg = json.loads(data.decode())
            if vid == msg['vehicle_id']:
                btry = checker.mysql.fetch_one('status_btry_packs', where_model={'id': vid})
                if 'marcopolo' not in cmdopt:
                    expect_msg['nio_battery_id'] = btry['nio_encoding']
                expect_msg['bid'] = btry['bid']
                assert_equal(msg, expect_msg)
                return
        assert False

    @pytest.mark.skip("转发sample_ts为空")
    def test_report_bms_msg_with_instant(self, vid, kafka, publish_msg, checker, cmdopt):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['bms_msg'])
        can_data = []
        for key in cans:
            can_data.append({'msg_id': key,
                             'value': 'ffffffffffffffff'})
        nextev_message, obj = publish_msg('instant_status_resp', sample_point={
            'can_msg': {
                'can_data': can_data
            }
        })

        msg = None
        expect_msg = {
            'vehicle_id': vid,
            'sample_ts': obj['sample_point']['sample_ts'],
            'can': [{
                "canName": "BMS_VCU_AE",
                "canId": 174,
                "canValue": {
                    "BMSHvConectorError": 3
                }},
                {
                    "canName": "BMS_CGW_274",
                    "canId": 628,
                    "canValue": {
                        "ISO_Performance_Index": 3,
                        "BCV_Voltage_Performance_Index": 3,
                        "BCV_Current_Com_Index": 3,
                        "CSC_Com_Index": 3,
                        "CSC_Circuitry_Index": 3,
                        "CTM_Performance_Index": 3,
                        "CVT_Performance_Index": 3
                    }
                }]
        }
        for data in kafka['comn'].consume(kafka['topics']['bms_msg'], timeout=10):
            msg = json.loads(data.decode())
            if vid == msg['vehicle_id']:
                btry = checker.mysql.fetch_one('status_btry_packs', where_model={'id': vid})
                if 'marcopolo' not in cmdopt:
                    expect_msg['nio_battery_id'] = btry['nio_encoding']
                expect_msg['bid'] = btry['bid']
                assert_equal(msg, expect_msg)
                return
        assert False

    @pytest.mark.parametrize('event_name', ['periodical_charge_update', 'periodical_journey_update'])
    def test_report_bms_msg_with_periodical_update(self, publish_msg_by_kafka, kafka, vid, event_name, cmdopt, checker):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['bms_msg'])

        with allure.step('上报携带can为bms信号的事件：' + event_name):
            can_data = []
            for key in cans:
                can_data.append({'msg_id': key,
                                 'value': 'ffffffffffffffff'})
            nextev_message, obj = publish_msg_by_kafka(event_name,
                                                       sample_points=[{'can_msg': {'can_data': can_data}}])
        msg = None
        expect_msg = {
            'vehicle_id': vid,
            'sample_ts': obj['sample_points'][0]['sample_ts'],
            'can': [{
                "canName": "BMS_VCU_AE",
                "canId": 174,
                "canValue": {
                    "BMSHvConectorError": 3
                }},
                {
                    "canName": "BMS_CGW_274",
                    "canId": 628,
                    "canValue": {
                        "ISO_Performance_Index": 3,
                        "BCV_Voltage_Performance_Index": 3,
                        "BCV_Current_Com_Index": 3,
                        "CSC_Com_Index": 3,
                        "CSC_Circuitry_Index": 3,
                        "CTM_Performance_Index": 3,
                        "CVT_Performance_Index": 3
                    }
                }]
        }
        for data in kafka['comn'].consume(kafka['topics']['bms_msg'], timeout=10):
            msg = json.loads(data.decode())
            if vid == msg['vehicle_id']:
                btry = checker.mysql.fetch_one('status_btry_packs', where_model={'id': vid})
                if 'marcopolo' not in cmdopt:
                    assert 'nio_battery_id' in msg
                    expect_msg['nio_battery_id'] = btry['nio_encoding']
                expect_msg['bid'] = btry['bid']
                assert_equal(msg, expect_msg)
                return
        assert False

    def test_report_bms_msg_with_lv_event(self, vid, kafka, publish_msg, cmdopt, checker):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['bms_msg'])
        can_data = []
        for key in cans:
            can_data.append({'msg_id': key,
                             'value': 'ffffffffffffffff'})

        # 上报携带bms can消息的lv_event信号
        nextev_message, obj = publish_msg('lv_batt_charging_event', can_msg={
            'can_data': can_data
        })

        msg = None
        expect_msg = {
            'vehicle_id': vid,
            'sample_ts': obj['sample_ts'],
            'can': [{
                "canName": "BMS_VCU_AE",
                "canId": 174,
                "canValue": {
                    "BMSHvConectorError": 3
                }},
                {
                    "canName": "BMS_CGW_274",
                    "canId": 628,
                    "canValue": {
                        "ISO_Performance_Index": 3,
                        "BCV_Voltage_Performance_Index": 3,
                        "BCV_Current_Com_Index": 3,
                        "CSC_Com_Index": 3,
                        "CSC_Circuitry_Index": 3,
                        "CTM_Performance_Index": 3,
                        "CVT_Performance_Index": 3
                    }
                }]
        }
        for data in kafka['comn'].consume(kafka['topics']['bms_msg'], timeout=10):
            msg = json.loads(data.decode())
            if vid == msg['vehicle_id']:
                btry = checker.mysql.fetch_one('status_btry_packs', where_model={'id': vid})
                if 'marcopolo' not in cmdopt:
                    expect_msg['nio_battery_id'] = btry['nio_encoding']
                expect_msg['bid'] = btry['bid']
                assert_equal(msg, expect_msg)
                return
        assert False

    @pytest.mark.parametrize('event_name', ['periodical_charge_update', 'periodical_journey_update'])
    def test_report_bms_msg_with_periodical_update_filtered(self, publish_msg_by_kafka, kafka, vid, event_name):
        can_data = []
        for key in cans:
            can_data.append({'msg_id': key,
                             'value': b'11111111111111'})

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
                                                                           'can_data': can_data
                                                                       },
                                                                       'evm_flag': False}])
        msg = None
        for data in kafka['comn'].consume(kafka['topics']['bms_msg'], timeout=10):
            print(data.decode())
            msg = json.loads(data.decode())
            if vid == msg['vehicle_id']:
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
                                                                           'can_data': can_data
                                                                       },
                                                                       'evm_flag': False}])
        for data in kafka['comn'].consume(kafka['topics']['bms_msg'], timeout=10):
            print(data.decode())
            msg = json.loads(data.decode())
            if vid == msg['vehicle_id']:
                assert False
        assert True
