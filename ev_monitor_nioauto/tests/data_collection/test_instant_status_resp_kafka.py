#!/usr/bin/env python
# coding=utf-8

"""
:file: test_instant_status_resp_kafka.py
:author: muhan.chen
:Date: Created on 2018/5/30 下午5:18
:Description: 上报车辆的全量数据
"""

import allure

from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


@allure.feature('上报车辆的全量事件')
class TestInstantStatusMsg(object):
    def test_instant_status_resp(self, vid, cmdopt, kafka, publish_msg_by_kafka):
        """
        vehicle_data kafka 只发送未解析的can msg，不再发送解析后的can msg。
        未解析的 msg_id 为原 msg_id 取负数，value为hexstring，即表示十六进制的字符串
        """
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, obj = publish_msg_by_kafka('instant_status_resp')
        publish_ts = obj['sample_point']['sample_ts'] + 2000
        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=60):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == publish_ts and vid == msg['params']['account_id']:
                break

        #新增bid字段，验证推送到大数据平台的消息里携带
        assert 'bid' in msg['params']['vehicle_status']['sample_point']['battery_package_info']['btry_pak_encoding'][0]
        msg['params']['vehicle_status']['sample_point']['battery_package_info']['btry_pak_encoding'][0].pop('bid')

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            # msg.pop('params') if msg else None
            nextev_obj = parse_nextev_message(nextev_message)
            msg['params'].pop('original_length')
            nextev_obj['params'].pop('original_length')
            msg['params']['vehicle_status']['sample_point'].pop('can_msg')
            nextev_obj['params']['vehicle_status']['sample_point'].pop('can_msg')
            if 'marcopolo' in cmdopt:
                nextev_obj['params']['vehicle_status']['sample_point']['position_status'].pop('latitude')
                nextev_obj['params']['vehicle_status']['sample_point']['position_status'].pop('longitude')
                nextev_obj['params']['vehicle_status']['sample_point']['battery_package_info']['btry_pak_encoding'][0].pop('re_encoding')
                nextev_obj['params']['vehicle_status']['sample_point']['battery_package_info']['btry_pak_encoding'][0]['nio_encoding'] =\
                    nextev_obj['params']['vehicle_status']['sample_point']['battery_package_info']['btry_pak_encoding'][0]['nio_encoding'][:27]
            assert_equal(msg, nextev_obj)
