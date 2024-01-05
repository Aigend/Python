""" 
@author:dun.yuan
@time: 2022/4/11 11:11 AM
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure
import json
import pytest
import random
from utils.assertions import assert_equal

can_ids = [94, 174, 628]


class TestCanSIGNALForwardKafka(object):
    @pytest.mark.parametrize('event_name',
                             ['instant_status_resp', 'periodical_charge_update', 'periodical_journey_update'])
    def test_report_can_signal_with_event(self, env, publish_msg_by_kafka, event_name, checker, kafka, cmdopt):
        # 重置offset
        kafka['cvs'].set_offset_to_end(kafka['topics']['bcu_07'])
        kafka['comn'].set_offset_to_end(kafka['topics']['bms_msg'])
        kafka['comn'].set_offset_to_end(kafka['topics']['can_60'])

        with allure.step('模拟ET7上报携带can signals的事件'):
            vid = env['vehicles']['et7_can_signal']['vehicle_id']
            vin = env['vehicles']['et7_can_signal']['vin']
            signals = []
            flag = random.choice([0, 1])
            for ii in can_ids:
                signal = {'id': ii, 'data_info': []}
                for i in range(2):
                    if i == flag:
                        signal['data_info'].append({'ts_offset': i, 'data': '0000000000000000'})
                    else:
                        signal['data_info'].append({'ts_offset': i, 'data': 'ffffffffffffffff'})
                signals.append(signal)

            if event_name == 'instant_status_resp':
                clear_fields = ['sample_point.can_msg', 'sample_point.alarm_signal']
                _, obj = publish_msg_by_kafka(event_name, platform_type=1, protobuf_v=18, vid=vid, vin=vin,
                                              config_version='ET7_1.0.0', sleep_time=30 if 'stg' in cmdopt else 2,
                                              signallib_version=random.choice([
                                                  'BL00.07.00_DA_01', 'BL00.07.00_DA_02', 'BL00.07.00_DA_03'
                                              ]),
                                              sample_point={'can_signal': {"signal_info": signals}},
                                              clear_fields=clear_fields
                                              )
                sample_ts = obj['sample_point']['can_signal']['sample_ts']
            else:
                clear_fields = ['sample_points[0].can_msg', 'sample_points[0].alarm_signal']
                _, obj = publish_msg_by_kafka(event_name, platform_type=1, protobuf_v=18, vid=vid, vin=vin,
                                              config_version='ET7_1.0.0',
                                              signallib_version=random.choice([
                                                  'BL00.07.00_DA_01', 'BL00.07.00_DA_02', 'BL00.07.00_DA_03'
                                              ]),
                                              sample_points=[{'can_signal': {"signal_info": signals}}],
                                              clear_fields=clear_fields
                                              )
                sample_ts = obj['sample_points'][0]['can_signal']['sample_ts']

        with allure.step('验证can_id 94的信号正确转发至bcu_07 topic'):
            expect_msg = {'vehicle_id': vid,
                          'sample_ts': sample_ts,
                          'type': event_name}
            expect_msg0 = {
                'can': [{
                    "can_id": 94,
                    "can_value": {
                        "ABAActv": 0, "ABAAvl": 0, "ABPActv": 0, "ABPAvl": 0, "ABSActv": 0, "ARPActv": 0,
                        "ARPCfgSts": 0, "AVHCfgSts": 0, "AVHSts": 0, "AWBActv": 0, "AWBAvl": 0, "AutoBrkgActv": 0,
                        "AutoBrkgAvl": 0, "BCU_EPBReq": 0, "BDWActv": 0, "BTCS": 0, "BascBrkActv": 0, "BascBrkSts": 0,
                        "BrakeDiscTem": 0, "CBCActv": 0, "CBCDeactv": 0, "CDPActv": 0, "CDPAvail": 0, "DTCActv": 0,
                        "DTCAvl": 0, "DWTActv": 0, "DWTBDeactv": 0, "EBAActv": 0, "EBAAvl": 0, "EBDActv": 0,
                        "EBPActv": 0, "HBAActv": 0, "HBADeactv": 0, "HBBActv": 0, "HBCActv": 0, "HDCSts": 0,
                        "HHCActv": 0, "HHCAvail": 0, "HPSAtv": 0, "HPSAvl": 0, "HRBActv": 0, "PFAEna": 0,
                        "PSP_Pressure_Status": 0, "RBCAtv": 0, "RBCAvl": 0, "SCMActv": 0, "SCMAvl": 0, "TCSActv": 0,
                        "TCSDeactv": 0, "TSCCfgSts": 0, "TSCSts": 0, "VCA": 0, "VDCActv": 0, "VDCDeactv": 0,
                        "VehBrkPedlMod": 0, "VehicleStability": 0
                    }
                }]
            }
            expect_msg1 = {
                'can': [{
                    "can_id": 94,
                    "can_value": {
                        "ABAActv": 1, "ABAAvl": 1, "ABPActv": 1, "ABPAvl": 1, "ABSActv": 1, "ARPActv": 1,
                        "ARPCfgSts": 1, "AVHCfgSts": 1, "AVHSts": 3, "AWBActv": 1, "AWBAvl": 1, "AutoBrkgActv": 1,
                        "AutoBrkgAvl": 1, "BCU_EPBReq": 3, "BDWActv": 1, "BTCS": 1, "BascBrkActv": 1, "BascBrkSts": 3,
                        "BrakeDiscTem": 1, "CBCActv": 1, "CBCDeactv": 1, "CDPActv": 1, "CDPAvail": 1, "DTCActv": 1,
                        "DTCAvl": 1, "DWTActv": 1, "DWTBDeactv": 1, "EBAActv": 1, "EBAAvl": 1, "EBDActv": 1,
                        "EBPActv": 1, "HBAActv": 1, "HBADeactv": 1, "HBBActv": 1, "HBCActv": 1, "HDCSts": 3,
                        "HHCActv": 1, "HHCAvail": 1, "HPSAtv": 1, "HPSAvl": 1, "HRBActv": 1, "PFAEna": 1,
                        "PSP_Pressure_Status": 1, "RBCAtv": 1, "RBCAvl": 1, "SCMActv": 1, "SCMAvl": 1, "TCSActv": 1,
                        "TCSDeactv": 1, "TSCCfgSts": 1, "TSCSts": 3, "VCA": 1, "VDCActv": 1, "VDCDeactv": 1,
                        "VehBrkPedlMod": 7, "VehicleStability": 3
                    }
                }]
            }
            expect_msg0.update(expect_msg)
            expect_msg1.update(expect_msg)
            i = 0
            for data in kafka['cvs'].consume(kafka['topics']['bcu_07'], timeout=10):
                msg = json.loads(data.decode())
                if 'process_id' in msg:
                    del(msg['process_id'])
                if vid == msg['vehicle_id'] and sample_ts == msg['sample_ts']:
                    i += 1
                    if flag == 0:
                        assert_equal(msg, expect_msg0)
                    else:
                        assert_equal(msg, expect_msg1)
                elif vid == msg['vehicle_id'] and sample_ts + 1 == msg['sample_ts']:
                    i += 1
                    if flag == 0:
                        expect_msg1['sample_ts'] += 1
                        assert_equal(msg, expect_msg1)
                    else:
                        expect_msg0['sample_ts'] += 1
                        assert_equal(msg, expect_msg0)
            assert i == 2

        with allure.step('验证can_id 174 628的信号正确转发至bms_msg topic'):
            expect_msg0 = {
                'vehicle_id': vid,
                'sample_ts': sample_ts,
                'can': [{
                    "canName": "BMS_VCU_AE",
                    "canId": 174,
                    "canValue": {
                        "BMSHvConectorError": 0
                    }},
                    {
                        "canName": "BMS_CGW_274",
                        "canId": 628,
                        "canValue": {
                            "ISO_Performance_Index": 0,
                            "BCV_Voltage_Performance_Index": 0,
                            "BCV_Current_Com_Index": 0,
                            "CSC_Com_Index": 0,
                            "CSC_Circuitry_Index": 0,
                            "CTM_Performance_Index": 0,
                            "CVT_Performance_Index": 0
                        }
                    }]
            }
            expect_msg1 = {
                'vehicle_id': vid,
                'sample_ts': sample_ts,
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
            btry = checker.mysql.fetch_one('status_btry_packs', where_model={'id': vid})
            if 'marcopolo' not in cmdopt:
                expect_msg0['nio_battery_id'] = btry['nio_encoding']
                expect_msg1['nio_battery_id'] = btry['nio_encoding']
            expect_msg0['bid'] = btry['bid']
            expect_msg1['bid'] = btry['bid']
            i = 0
            for data in kafka['comn'].consume(kafka['topics']['bms_msg'], timeout=10):
                msg = json.loads(data.decode())
                print(msg)
                if vid == msg['vehicle_id'] and sample_ts == msg['sample_ts']:
                    i += 1
                    if flag == 0:
                        assert_equal(msg, expect_msg0)
                    else:
                        assert_equal(msg, expect_msg1)
                elif vid == msg['vehicle_id'] and sample_ts + 1 == msg['sample_ts']:
                    i += 1
                    if flag == 0:
                        expect_msg1['sample_ts'] += 1
                        assert_equal(msg, expect_msg1)
                    else:
                        expect_msg0['sample_ts'] += 1
                        assert_equal(msg, expect_msg0)
            assert i == 2

        with allure.step('验证上报事件携带can signal就会转发vehicle_status中的urgt_prw_shtdwn替代can_id 60信号'):
            expect_msg = {
                'vehicle_id': vid,
                'sample_ts': sample_ts,
                'type': event_name,
                'can': [{
                    'can_id': 60,
                    'can_value': {'CrashDetd': obj['sample_point']['vehicle_status']['urgt_prw_shtdwn']
                                  if 'instant' in event_name else obj['sample_points'][0]['vehicle_status']['urgt_prw_shtdwn']}
                }]
            }
            for data in kafka['comn'].consume(kafka['topics']['can_60'], timeout=10):
                msg = json.loads(data.decode())
                if vid == msg['vehicle_id'] and sample_ts == msg['sample_ts']:
                    assert_equal(msg, expect_msg)

    @pytest.mark.parametrize('event_name', ['periodical_charge_update', 'periodical_journey_update'])
    def test_report_bms_msg_with_periodical_update_filtered(self, env, publish_msg_by_kafka, event_name, checker,
                                                            kafka):
        # 重置offset
        kafka['cvs'].set_offset_to_end(kafka['topics']['bcu_07'])
        kafka['comn'].set_offset_to_end(kafka['topics']['bms_msg'])
        kafka['comn'].set_offset_to_end(kafka['topics']['can_60'])

        with allure.step(
                '过滤evm_flag =false&&alarm_signal只有这个CAM_FC_03:LKSTakeoverReq信号 && vehicle_status.vehl_state = 1'):
            vid = env['vehicles']['et7_can_signal']['vehicle_id']
            vin = env['vehicles']['et7_can_signal']['vin']
            signals = []
            flag = random.choice([0, 1])
            for ii in can_ids:
                signal = {'id': ii, 'data_info': []}
                for i in range(2):
                    if i == flag:
                        signal['data_info'].append({'ts_offset': i, 'data': '0000000000000000'})
                    else:
                        signal['data_info'].append({'ts_offset': i, 'data': 'ffffffffffffffff'})
                signals.append(signal)
            signal_all = [{"name": "CAM_FC_03:LKSTakeoverReq", "value": 1, "alarm_level": 4, "wti_code": "WTI-158"}]
            clear_fields = ['sample_points[0].can_msg']
            _, obj = publish_msg_by_kafka(event_name, platform_type=1, protobuf_v=18, vid=vid, vin=vin,
                                          config_version='ET7_1.0.0',
                                          signallib_version=random.choice([
                                              'BL00.07.00_DA_01', 'BL00.07.00_DA_02', 'BL00.07.00_DA_03'
                                          ]),
                                          sample_points=[{'can_signal': {"signal_info": signals},
                                                          'alarm_signal': {'signal_int': signal_all},
                                                          'vehicle_status': {'vehl_state': 1},
                                                          'evm_flag': False}],
                                          clear_fields=clear_fields
                                          )
            sample_ts = obj['sample_points'][0]['can_signal']['sample_ts']

        with allure.step('验证can id 94没有转发至bcu 07 topic'):
            for data in kafka['cvs'].consume(kafka['topics']['bms_msg'], timeout=10):
                msg = json.loads(data.decode())
                if vid == msg['vehicle_id'] and sample_ts == msg['sample_ts']:
                    assert False
            assert True

        with allure.step('验证can id 174 628没有转发至bms_msg topic'):
            for data in kafka['comn'].consume(kafka['topics']['bcu_07'], timeout=10):
                msg = json.loads(data.decode())
                if vid == msg['vehicle_id'] and sample_ts == msg['sample_ts']:
                    assert False
            assert True

        with allure.step('验证CrashDetd没有转发至can_60 topic'):
            for data in kafka['comn'].consume(kafka['topics']['can_60'], timeout=10):
                msg = json.loads(data.decode())
                if vid == msg['vehicle_id'] and sample_ts == msg['sample_ts']:
                    assert False
            assert True

    @pytest.mark.skip("corner case, 无需每日定期执行")
    @pytest.mark.parametrize('event_name', ['periodical_charge_update', 'periodical_journey_update'])
    def test_report_can_signal_with_event_2_points(self, env, publish_msg_by_kafka, event_name, checker, kafka, cmdopt):
        # 重置offset
        kafka['cvs'].set_offset_to_end(kafka['topics']['bcu_07'])
        kafka['comn'].set_offset_to_end(kafka['topics']['bms_msg'])
        kafka['comn'].set_offset_to_end(kafka['topics']['can_60'])

        with allure.step('模拟ET7上报携带can signals的事件'):
            vid = env['vehicles']['et7_can_signal']['vehicle_id']
            vin = env['vehicles']['et7_can_signal']['vin']
            signals = []
            flag = random.choice([0, 1])
            for ii in can_ids:
                signal = {'id': ii, 'data_info': []}
                for i in range(2):
                    if i == flag:
                        signal['data_info'].append({'ts_offset': i, 'data': '0000000000000000'})
                    else:
                        signal['data_info'].append({'ts_offset': i, 'data': 'ffffffffffffffff'})
                signals.append(signal)

            clear_fields = ['sample_points[0].can_msg', 'sample_points[0].alarm_signal',
                            'sample_points[1].can_msg', 'sample_points[1].alarm_signal']
            _, obj = publish_msg_by_kafka(event_name, platform_type=1, protobuf_v=18, vid=vid, vin=vin,
                                          config_version='ET7_1.0.0',
                                          signallib_version=random.choice([
                                              'BL00.07.00_DA_01', 'BL00.07.00_DA_02', 'BL00.07.00_DA_03'
                                          ]),
                                          sample_points=[{'can_signal': {"signal_info": signals}},
                                                         {'can_signal': {"signal_info": signals}}],
                                          clear_fields=clear_fields
                                          )

        with allure.step('验证can_id 94的信号正确转发至bcu_07 topic'):
            i = 0
            for data in kafka['cvs'].consume(kafka['topics']['bcu_07'], timeout=10):
                msg = json.loads(data.decode())
                if vid == msg['vehicle_id']:
                    i += 1
            assert i == 4

        with allure.step('验证can_id 174 628的信号正确转发至bms_msg topic'):
            i = 0
            for data in kafka['comn'].consume(kafka['topics']['bms_msg'], timeout=10):
                msg = json.loads(data.decode())
                print(msg)
                if vid == msg['vehicle_id']:
                    i += 1
            assert i == 4

        with allure.step('验证上报事件携带can signal就会转发vehicle_status中的urgt_prw_shtdwn替代can_id 60信号'):
            i = 0
            for data in kafka['comn'].consume(kafka['topics']['can_60'], timeout=10):
                msg = json.loads(data.decode())
                print(msg)
                if vid == msg['vehicle_id']:
                    i += 1
            assert i == 2
