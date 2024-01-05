""" 
@author:dun.yuan
@time: 2022/3/25 11:46 PM
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import random
import allure
import pytest
from utils.time_parse import timestamp_to_utc_strtime

can_ids = [537, 590, 623, 701, 923, 80, 617, 336, 268]


class TestNT2ParseCanSignal(object):
    @pytest.mark.parametrize('event_name', ['periodical_charge_update', 'periodical_journey_update', 'instant_status_resp'])
    def test_nt2_parse_can_periodical_update(self, env, publish_msg_by_kafka, event_name, checker):
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

        with allure.step('模拟ET7上报携带can signal的周期事件, nt2平台某些字段不再上报故构造上报消息时清除'):
            if event_name == 'instant_status_resp':
                clear_fields = ['sample_point.can_msg', 'sample_point.tyre_status', 'sample_point.occupant_status', 'sample_point.charging_info']
                _, obj = publish_msg_by_kafka(event_name, platform_type=1, protobuf_v=18, vid=vid, vin=vin,
                                              config_version='ET7_1.0.0',
                                              signallib_version=random.choice([
                                                  'BL00.07.00_DA_01', 'BL00.07.00_DA_02', 'BL00.07.00_DA_03'
                                              ]),
                                              sample_point={'can_signal': {"signal_info": signals}},
                                              clear_fields=clear_fields
                                              )
                sample_ts = obj['sample_point']['sample_ts']
            else:
                clear_fields = ['sample_points[0].can_msg', 'sample_points[0].tyre_status', 'sample_points[0].occupant_status']
                if event_name == 'periodical_charge_update':
                    clear_fields.append('sample_points[0].charging_info')
                _, obj = publish_msg_by_kafka(event_name, platform_type=1, protobuf_v=18, vid=vid, vin=vin,
                                              config_version='ET7_1.0.0',
                                              signallib_version=random.choice([
                                                  'BL00.07.00_DA_01', 'BL00.07.00_DA_02', 'BL00.07.00_DA_03'
                                              ]),
                                              sample_points=[{'can_signal': {"signal_info": signals}}],
                                              clear_fields=clear_fields
                                              )
                sample_ts = obj['sample_points'][0]['sample_ts']

        with allure.step('查询mysql status_soc对应字段验证can signal解析结果'):
            soc_mysql = checker.mysql.fetch_one('status_soc', {'id': vid, "sample_time": timestamp_to_utc_strtime(sample_ts)})
            assert soc_mysql['charger_type'] == (0 if flag == 1 else 7)  # charger_type的值从can ID:80 信号名：VCUWakeUpMod中获取
            assert soc_mysql['estimate_chrg_time'] == (0 if flag == 1 else 4095)  # estimate_chrg_time的值从can ID:617 信号名：BMSEstimateChrgTime中获取
            assert soc_mysql['battery_pack_cap'] == (0 if flag == 1 else 15)  # battery_pack_cap的值从can ID:623 信号名：BMSBatteryPackCap中获取
            assert soc_mysql['chrg_disp_lamp_req'] == (0 if flag == 1 else 7)  # 充电状态 chrg_disp_lamp_req的值从can ID:537 信号名：VCUChrgDispLampReq中获取
            assert soc_mysql['chrg_disp_crrt'] == (-2000 if flag == 1 else 4553.5)  # 电流从can ID:590 信号名：VCUChrgDispCrrt中获取
            assert soc_mysql['chrg_disp_volt'] == (0.0 if flag == 1 else 1023.5)  # 电压从can ID:590 信号名：VCUChrgDispVolt中获取
            assert soc_mysql['chrg_pwr'] == (-500.0 if flag == 1 else 523.5)  # 功率从can ID:590 信号名：VCUChrgPwr中获取

        with allure.step('查询mysql status_tyre对应字段验证can signal解析结果'):
            # 胎压，轮胎温度
            # canID:923 信号：TpmsFrntLeWhlPress，TpmsFrntRiWhlPress，TpmsReLeWhlPress，TpmsReRiWhlPress，TpmsFrntLeWhlTemp，TpmsFrntRiWhlTemp，TpmsReLeWhlTemp，TpmsReRiWhlTemp
            tyre_mysql = checker.mysql.fetch_one('status_tyre', {'id': vid, "sample_time": timestamp_to_utc_strtime(sample_ts)})
            assert tyre_mysql['frnt_le_whl_press'] == 0 if flag == 1 else 350.115
            assert tyre_mysql['frnt_ri_whl_press'] == 0 if flag == 1 else 350.115
            assert tyre_mysql['re_le_whl_press'] == 0 if flag == 1 else 350.115
            assert tyre_mysql['re_ri_whl_press'] == 0 if flag == 1 else 350.115
            assert tyre_mysql['re_ri_whl_temp'] == -50 if flag == 1 else 205
            assert tyre_mysql['re_le_whl_temp'] == -50 if flag == 1 else 205
            assert tyre_mysql['frnt_le_whl_temp'] == -50 if flag == 1 else 205
            assert tyre_mysql['frnt_ri_whl_temp'] == -50 if flag == 1 else 205

        with allure.step('查询mysql status_occupant对应字段验证can signal解析结果'):
            # 乘客信息
            # canID: 701 信号：SeatOccpFrntLeSts，SeatOccptFrntRiSts
            occupant_mysql = checker.mysql.fetch_one('status_occupant', {'id': vid,
                                                                         "sample_time": timestamp_to_utc_strtime(sample_ts)})
            assert occupant_mysql['fr_le_seat'] == 0 if flag == 1 else 3
            assert occupant_mysql['fr_ri_seat'] == 0 if flag == 1 else 1

        with allure.step('查询mysql status_vehicle表vehl_mode字段验证can signal解析结果'):
            # 乘客信息
            # canID: 268 信号：VehMode
            occupant_mysql = checker.mysql.fetch_one('status_vehicle', {'id': vid,
                                                                         "sample_time": timestamp_to_utc_strtime(sample_ts)})
            assert occupant_mysql['vehl_mode'] == 0 if flag == 1 else 15

        with allure.step("校验mongo can_msg,电池信息上报10分钟之内在mongo查询，超过10分钟查询mysql"):
            can_msg_in_mongo = checker.mongodb.find("can_msg", {"_id": f"{vid}_623"})[0]
            assert can_msg_in_mongo['timestamp'] == sample_ts
            assert can_msg_in_mongo['value']['BMSBatteryPackCap'] == 0 if flag == 1 else 15
