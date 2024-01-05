""" 
@author:dun.yuan
@time: 2022/3/29 2:46 PM
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import random
import allure
import pytest
import time
from data.lat_long import LAT_LONG


class TestParseNPFromCan(object):
    @pytest.fixture(scope='class', autouse=True)
    def get_vid(self, vid, checker, request):
        def fin():
            checker.vid = vid

        request.addfinalizer(fin)

    def test_parse_np_from_can_nt2(self, env, publish_msg_by_kafka, checker):
        """
        NT2 DA_NAD_Sts：获取acc/np/nop状态

        对应can336应发的值：
        0000000006000000，DA_NAD_Sts：6
        0000000007000000，DA_NAD_Sts：7
        0000000008000000，DA_NAD_Sts：8
        0000000009000000，DA_NAD_Sts：9

        NT2.0 DA_NAD_Sts
        9 "state 31 (DA / NOP active)" nop 3
        8 "state 23 (DA / NP active (long.only))"
        7 "state 22 (DA / NP active (long/lat))" np 2
        6 "state 21 (DA / ACC active)" acc 1
        none 0
        """
        vid = env['vehicles']['et7_can_signal']['vehicle_id']
        vin = env['vehicles']['et7_can_signal']['vin']
        checker.vid = vid
        with allure.step('模拟ET7上报携带id 336的can signal的周期事件, nt2平台某些字段不再上报故构造上报消息时清除'):
            n = random.choice([5, 6, 7, 8, 9])
            dic = {5: 0, 6: 1, 7: 2, 8: 2, 9: 3}
            signals = []
            for ii in [336, 80, 617]:
                signal = {'id': ii, 'data_info': []}
                for i in range(2):
                    if i == 0:
                        signal['data_info'].append({'ts_offset': i, 'data': '0000000000000000'})
                    else:
                        signal['data_info'].append({'ts_offset': i, 'data': f'000000000{n}000000'})
                signals.append(signal)
            _, obj = publish_msg_by_kafka('periodical_journey_update', platform_type=1, protobuf_v=18, vid=vid, vin=vin,
                                          config_version='ET7_1.0.0',
                                          signallib_version=random.choice([
                                              'BL00.07.00_DA_01', 'BL00.07.00_DA_02', 'BL00.07.00_DA_03'
                                          ]),
                                          sample_points=[{'can_signal': {"signal_info": signals}}],
                                          clear_fields=['sample_points[0].can_msg',
                                                        # 'sample_points[0].charging_info',
                                                        'sample_points[0].tyre_status',
                                                        'sample_points[0].occupant_status'])

        with allure.step('验证Cassandra driving_data存储'):
            tables = {
                'driving_data': ['dump_enrgy',
                                 'mileage',
                                 'position',
                                 'posng_valid_type',
                                 'soc',
                                 'speed',
                                 'nio_pilot_sts',
                                 'trip_odometer',
                                 'realtime_power_consumption',
                                 'process_id',
                                 'sample_ts']
            }
            obj['sample_points'][0]['nio_pilot_sts'] = dic[n]
            obj['sample_points'][0]['version'] = obj['version']
            checker.check_cassandra_tables(obj['sample_points'][0], tables,
                                           event_name='periodical_journey_update',
                                           sample_ts=obj['sample_points'][0]['sample_ts'])

    def test_parse_np_from_can_nt1(self, env, publish_msg_by_kafka, checker):
        """
        NT1:
        CAM_FC_03 552 ACCNPSts This signal shows the status of the ACC/L2-Pilot system
        CAM_FC_04 548 NOPSts NOP main status

        对应CAN 552应发值：
        00E0000000000000，AccNpSts 7
        00C0000000000000, AccNpSts 6
        00A0000000000000, AccNpSts 5
        0060000000000000, AccNpSts 3

        对应CAN 548应发值：
        000000E000000000，NOPSts 7
        0000006000000000，NOPSts 3

        NOP_Sts 3 -> nop 3
        NOP_Sts != 3 & AccNpSts = 5, 6 -> np 2
        NOP_Sts != 3 & AccNpSts = 3 -> acc 1
        none 0
        """
        vid = env['vehicles']['vehicle_history_2']['vehicle_id']
        vin = env['vehicles']['vehicle_history_2']['vin']
        checker.vid = vid
        with allure.step('模拟NT1平台上报携带id 336的can msg的周期事件, can_signal上报消息时清除'):
            m = random.choice(['E', 'C', 'A', '6'])
            n = random.choice(['E', '6'])
            can_msgs = {'can_data': [
                {
                    'msg_id': 552,
                    'value': f'00{m}0000000000000'
                },
                {
                    'msg_id': 548,
                    'value': f'000000{n}000000000'
                }
            ]}
            _, obj = publish_msg_by_kafka('periodical_journey_update', protobuf_v=18, vid=vid, vin=vin,
                                          sample_points=[{'can_msg': can_msgs}],
                                          clear_fields=['sample_points[0].can_signal'])

        with allure.step('验证Cassandra driving_data存储'):
            tables = {
                'driving_data': ['dump_enrgy',
                                 'mileage',
                                 'position',
                                 'posng_valid_type',
                                 'soc',
                                 'speed',
                                 'nio_pilot_sts',
                                 'trip_odometer',
                                 'realtime_power_consumption',
                                 'process_id',
                                 'sample_ts']
            }
            if n == '6':
                obj['sample_points'][0]['nio_pilot_sts'] = 3
            elif m == 'C' or m == 'A':
                obj['sample_points'][0]['nio_pilot_sts'] = 2
            elif m == '6':
                obj['sample_points'][0]['nio_pilot_sts'] = 1
            else:
                obj['sample_points'][0]['nio_pilot_sts'] = 0
            obj['sample_points'][0]['version'] = obj['version']
            checker.check_cassandra_tables(obj['sample_points'][0], tables,
                                           event_name='periodical_journey_update',
                                           sample_ts=obj['sample_points'][0]['sample_ts'])

    @pytest.mark.test  # 定期上报用于验证data statistics服务np统计是否正确
    def test_parse_np_from_can_nt2_one_trip(self, env, publish_msg_by_kafka, checker):
        vid = env['vehicles']['et7_can_signal']['vehicle_id']
        vin = env['vehicles']['et7_can_signal']['vin']
        checker.vid = vid
        with allure.step('上报行程开始事件'):
            start_ts = int(time.time()) * 1000
            journey_id = str(start_ts // 1000)
            soc = 98  # -
            dump_enrgy = 70  # -
            remaining_range = 500  # -
            mileage = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])[0]['mileage']
            po_s = {"latitude": LAT_LONG[0]['latitude'], "longitude": LAT_LONG[0]['longitude'], "posng_valid_type": 0}
            publish_msg_by_kafka('trip_start_event', protobuf_v=18,
                                 vid=vid, vin=vin,
                                 sample_ts=start_ts,
                                 position_status=po_s,
                                 soc_status={"remaining_range": remaining_range, 'soc': soc, 'dump_enrgy': dump_enrgy},
                                 vehicle_status={"mileage": mileage, "soc": soc},
                                 trip_status={'trip_id': journey_id, 'trip_odometer': 0},
                                 )
        with allure.step('模拟ET7上报携带id 336的can signal的周期事件, nt2平台某些字段不再上报故构造上报消息时清除'):
            n = random.choice([5, 6, 7, 8, 9])
            dic = {5: 0, 6: 1, 7: 2, 8: 2, 9: 3}
            signals = []
            for ii in [336, 80, 617]:
                signal = {'id': ii, 'data_info': []}
                for i in range(2):
                    if i == 0:
                        signal['data_info'].append({'ts_offset': i, 'data': '0000000000000000'})
                    else:
                        signal['data_info'].append({'ts_offset': i, 'data': f'000000000{n}000000'})
                signals.append(signal)
            _, obj = publish_msg_by_kafka('periodical_journey_update', platform_type=1, protobuf_v=18, vid=vid, vin=vin,
                                          config_version='ET7_1.0.0',
                                          signallib_version=random.choice([
                                              'BL00.07.00_DA_01', 'BL00.07.00_DA_02', 'BL00.07.00_DA_03'
                                          ]),
                                          journey_id=journey_id,
                                          sample_points=[{'can_signal': {"signal_info": signals},
                                                          "vehicle_status": {"speed": 100, "mileage": mileage + 1,
                                                                             "soc": soc},
                                                          'trip_status': {'trip_id': journey_id, 'trip_odometer': 10.1},
                                                          'position_status': po_s
                                                          }],
                                          clear_fields=['sample_points[0].can_msg',
                                                        # 'sample_points[0].charging_info',
                                                        'sample_points[0].tyre_status',
                                                        'sample_points[0].occupant_status'])
        with allure.step('模拟ET7上报携带id 336的can signal的周期事件, nt2平台某些字段不再上报故构造上报消息时清除'):
            n = random.choice([5, 6, 7, 8, 9])
            dic = {5: 0, 6: 1, 7: 2, 8: 2, 9: 3}
            signals = []
            for ii in [336, 80, 617]:
                signal = {'id': ii, 'data_info': []}
                for i in range(2):
                    if i == 0:
                        signal['data_info'].append({'ts_offset': i, 'data': '0000000000000000'})
                    else:
                        signal['data_info'].append({'ts_offset': i, 'data': f'000000000{n}000000'})
                signals.append(signal)
            _, obj = publish_msg_by_kafka('periodical_journey_update', platform_type=1, protobuf_v=18, vid=vid, vin=vin,
                                          config_version='ET7_1.0.0',
                                          signallib_version=random.choice([
                                              'BL00.07.00_DA_01', 'BL00.07.00_DA_02', 'BL00.07.00_DA_03'
                                          ]),
                                          journey_id=journey_id,
                                          sample_points=[{# 'can_signal': {"signal_info": signals},
                                                          "vehicle_status": {"speed": 100, "mileage": mileage + 3,
                                                                             "soc": soc - 1},
                                                          'trip_status': {'trip_id': journey_id, 'trip_odometer': 11.2},
                                                          'position_status': po_s
                                                          }],
                                          clear_fields=['sample_points[0].can_msg',
                                                        # 'sample_points[0].charging_info',
                                                        'sample_points[0].tyre_status',
                                                        'sample_points[0].occupant_status'])
        with allure.step('模拟ET7上报携带id 336的can signal的周期事件, nt2平台某些字段不再上报故构造上报消息时清除'):
            n = random.choice([5, 6, 7, 8, 9])
            dic = {5: 0, 6: 1, 7: 2, 8: 2, 9: 3}
            signals = []
            for ii in [336, 80, 617]:
                signal = {'id': ii, 'data_info': []}
                for i in range(2):
                    if i == 0:
                        signal['data_info'].append({'ts_offset': i, 'data': '0000000000000000'})
                    else:
                        signal['data_info'].append({'ts_offset': i, 'data': f'000000000{n}000000'})
                signals.append(signal)
            _, obj = publish_msg_by_kafka('periodical_journey_update', platform_type=1, protobuf_v=18, vid=vid, vin=vin,
                                          config_version='ET7_1.0.0',
                                          signallib_version=random.choice([
                                              'BL00.07.00_DA_01', 'BL00.07.00_DA_02', 'BL00.07.00_DA_03'
                                          ]),
                                          journey_id=journey_id,
                                          sample_points=[{'can_signal': {"signal_info": signals},
                                                          "vehicle_status": {"speed": 100, "mileage": mileage + 3,
                                                                             "soc": soc - 1},
                                                          'trip_status': {'trip_id': journey_id, 'trip_odometer': 11.2},
                                                          'position_status': po_s
                                                          }],
                                          clear_fields=['sample_points[0].can_msg',
                                                        # 'sample_points[0].charging_info',
                                                        'sample_points[0].tyre_status',
                                                        'sample_points[0].occupant_status'])
        with allure.step('模拟ET7上报携带id 336的can signal的周期事件, nt2平台某些字段不再上报故构造上报消息时清除'):
            n = random.choice([5, 6, 7, 8, 9])
            dic = {5: 0, 6: 1, 7: 2, 8: 2, 9: 3}
            signals = []
            for ii in [336, 80, 617]:
                signal = {'id': ii, 'data_info': []}
                for i in range(2):
                    if i == 0:
                        signal['data_info'].append({'ts_offset': i, 'data': '0000000000000000'})
                    else:
                        signal['data_info'].append({'ts_offset': i, 'data': f'000000000{n}000000'})
                signals.append(signal)
            _, obj = publish_msg_by_kafka('periodical_journey_update', platform_type=1, protobuf_v=18, vid=vid, vin=vin,
                                          config_version='ET7_1.0.0',
                                          signallib_version=random.choice([
                                              'BL00.07.00_DA_01', 'BL00.07.00_DA_02', 'BL00.07.00_DA_03'
                                          ]),
                                          journey_id=journey_id,
                                          sample_points=[{#'can_signal': {"signal_info": signals},
                                                          "vehicle_status": {"speed": 100, "mileage": mileage + 3,
                                                                             "soc": soc - 1},
                                                          'trip_status': {'trip_id': journey_id, 'trip_odometer': 11.2},
                                                          'position_status': po_s
                                                          }],
                                          clear_fields=['sample_points[0].can_msg',
                                                        # 'sample_points[0].charging_info',
                                                        'sample_points[0].tyre_status',
                                                        'sample_points[0].occupant_status'])
        with allure.step('模拟ET7上报携带id 336的can signal的周期事件, nt2平台某些字段不再上报故构造上报消息时清除'):
            n = random.choice([5, 6, 7, 8, 9])
            dic = {5: 0, 6: 1, 7: 2, 8: 2, 9: 3}
            signals = []
            for ii in [336, 80, 617]:
                signal = {'id': ii, 'data_info': []}
                for i in range(2):
                    if i == 0:
                        signal['data_info'].append({'ts_offset': i, 'data': '0000000000000000'})
                    else:
                        signal['data_info'].append({'ts_offset': i, 'data': f'000000000{n}000000'})
                signals.append(signal)
            _, obj = publish_msg_by_kafka('periodical_journey_update', platform_type=1, protobuf_v=18, vid=vid, vin=vin,
                                          config_version='ET7_1.0.0',
                                          signallib_version=random.choice([
                                              'BL00.07.00_DA_01', 'BL00.07.00_DA_02', 'BL00.07.00_DA_03'
                                          ]),
                                          journey_id=journey_id,
                                          sample_points=[{'can_signal': {"signal_info": signals},
                                                          "vehicle_status": {"speed": 100, "mileage": mileage + 6,
                                                                             "soc": soc - 2},
                                                          'trip_status': {'trip_id': journey_id, 'trip_odometer': 12.3},
                                                          'position_status': po_s
                                                          }],
                                          clear_fields=['sample_points[0].can_msg',
                                                        # 'sample_points[0].charging_info',
                                                        'sample_points[0].tyre_status',
                                                        'sample_points[0].occupant_status'])

        with allure.step('上报行程结束'):
            publish_msg_by_kafka('trip_end_event', protobuf_v=18,
                                 vid=vid, vin=vin,
                                 position_status=po_s,
                                 soc_status={
                                     "remaining_range": remaining_range - 2,
                                     'soc': soc - 2,
                                     'dump_enrgy': dump_enrgy - 2},
                                 vehicle_status={"mileage": mileage + 2,
                                                 "soc": soc - 2},
                                 trip_status={'trip_id': journey_id, 'trip_odometer': 15.5}
                                 )
