#!/usr/bin/env python
# coding=utf-8

"""
:file: test_periodical_charge_update_kafka.py
:author: zhiqiang.zhu
:Date: Created on 2017/1/12 下午8:01
:Description: 周期性充电消息存储到kafka的swc-tsp-data_collection-test-vehicle_data供其他系统消费
"""
import allure

from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestChargeUpdateMsg(object):
    def test_periodical_charge_update(self, vid, cmdopt, kafka, publish_msg_by_kafka):
        """
        vehicle_data kafka 只发送未解析的can msg，不再发送解析后的can msg。
        未解析的 msg_id 为原 msg_id 取负数，value为hexstring，即表示十六进制的字符串
        """
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, obj = publish_msg_by_kafka('periodical_charge_update')

        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=60):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == obj['sample_points'][0]['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            msg.pop('params') if msg else None
            nextev_obj = parse_nextev_message(nextev_message)
            nextev_obj.pop('params')
            assert_equal(msg, nextev_obj)

    def test_some_wti_not_save(self, publish_msg_by_kafka, kafka, vid):
        # 只有2个update事件会过滤wti，instant和alarm事件不会过滤
        event_name = 'periodical_charge_update'
        with allure.step('过滤evm_flag =false&&alarm_signal只有这个CAM_FC_03:LKSTakeoverReq信号 && vehicle_status.vehl_state = 1'):

            signal_all = [
                {"name": "CAM_FC_03:LKSTakeoverReq", "value": 1, "alarm_level": 4, "wti_code": "WTI-158"},
            ]
            nextev_message, obj = publish_msg_by_kafka(event_name,
                                                       sample_points=[{'alarm_signal': {'signal_int': signal_all},
                                                                       'vehicle_status': {'vehl_state': 1},
                                                                       'evm_flag': False}])

            msg = None
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=10):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == obj['sample_points'][0]['sample_ts'] and vid == msg['params']['account_id']:
                    is_found = True
                    break

            with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):

                assert_equal(is_found, False)

        with allure.step('过滤evm_flag =false&&alarm_signal只有这个VCU_CGW_219:VCUChgLineSts信号 && 充电状态中即chrg_state=1'):
            signal_all = [
                {"name": "VCU_CGW_219:VCUChgLineSts", "value": 1, "alarm_level": 4, "wti_code": "WTI-43"},
            ]
            nextev_message, obj = publish_msg_by_kafka(event_name,
                                                       sample_points=[{'alarm_signal': {'signal_int': signal_all},
                                                                       'soc_status': {'chrg_state': 1},
                                                                       'evm_flag': False}])
            msg = None
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=10):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == obj['sample_points'][0]['sample_ts'] and vid == msg['params']['account_id']:
                    is_found = True
                    break

            with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):

                assert_equal(is_found, False)
