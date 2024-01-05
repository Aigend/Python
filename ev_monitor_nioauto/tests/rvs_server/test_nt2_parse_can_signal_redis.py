""" 
@author:dun.yuan
@time: 2022/3/28 3:05 PM
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import random
import allure
import pytest
from utils.time_parse import timestamp_to_utc_strtime

can_ids = [537, 590, 623, 80, 617]


class TestNT2ParseCanSignal(object):
    @pytest.fixture(scope='class', autouse=True)
    def get_vid(self, vid, checker, request):
        def fin():
            checker.vid = vid

        request.addfinalizer(fin)

    @pytest.mark.parametrize('event_name', ['periodical_charge_update', 'periodical_journey_update', 'instant_status_resp'])
    def test_nt2_parse_can_periodical_update(self, env, publish_msg_by_kafka, vid, event_name, checker, redis_key_front):
        vid = env['vehicles']['et7_can_signal']['vehicle_id']
        vin = env['vehicles']['et7_can_signal']['vin']
        checker.vid = vid
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

        keys = ['SocStatus']
        # 清除redis 缓存
        # 增加staging环境支持
        remote_vehicle_key_front = redis_key_front['remote_vehicle']
        # 支持马克波罗服务测试
        key_front = f'{remote_vehicle_key_front}:vehicle_status:{vid}'
        for key in keys:
            checker.redis.delete(f'{key_front}:{key}')

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
                oo = obj['sample_point']
                sample_ts = obj['sample_point']['sample_ts']
            else:
                clear_fields = ['sample_points[0].can_msg', 'sample_points[0].tyre_status', 'sample_points[0].occupant_status', 'sample_points[0].alarm_signal']
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
                oo = obj['sample_points'][0]
                sample_ts = obj['sample_points'][0]['sample_ts']

        with allure.step('查询redis status_soc对应字段验证can signal解析结果'):
            keys = ['SocStatus']
            oo['charging_info'] = {'charger_type': 0 if flag == 1 else 7,  # charger_type的值从can ID:80 信号名：VCUWakeUpMod中获取
                                   'estimate_chrg_time': 0 if flag == 1 else 4095  # estimate_chrg_time的值从can ID:617 信号名：BMSEstimateChrgTime中获取
                                  }
            oo['soc_status']['battery_pack_cap'] = 0 if flag == 1 else 15  # battery_pack_cap的值从can ID:623 信号名：BMSBatteryPackCap中获取
            oo['soc_status']['chrg_req'] = 0 if flag == 1 else 7  # 充电状态 chrg_disp_lamp_req的值从can ID:537 信号名：VCUChrgDispLampReq中获取
            oo['soc_status']['charging_current'] = -2000 if flag == 1 else 4553.5  # 电流从can ID:590 信号名：VCUChrgDispCrrt中获取
            oo['soc_status']['charging_voltage'] = 0.0 if flag == 1 else 1023.5  # 电压从can ID:590 信号名：VCUChrgDispVolt中获取
            oo['soc_status']['charging_power'] = -500.0 if flag == 1 else 523.5  # 功率从can ID:590 信号名：VCUChrgPwr中获取

            checker.check_redis(oo, keys, clear_none=True, sample_ts=sample_ts)

