#!/usr/bin/env python
# coding=utf-8


import ast
import json
import allure
import pytest

from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal
from utils.logger import logger


# 换电推送增加bid
# https://confluence.nioint.com/pages/viewpage.action?pageId=359236741
# http://showdoc.nevint.com/index.php?s=/11&page_id=11592
# 为验证换电推送的feature，在上报换电事件中，指定chg_subsys_encoding值为battery_trace_test.sys_battery_pack_entity表内存在的nio_encoding值，并验证向下游推送时携带bid字段
class TestPowerSwapEventMsg(object):
    def test_power_swap_start_event(self, vid, publish_msg, kafka, mysql, cmdopt, checker):
        kafka['comn'].set_offset_to_end(kafka['topics']['power_swap'])
        # 选取电池编码
        pack = mysql['battery_trace'].fetch_one('sys_battery_pack_entity', where_model={'status': 1},
                                                order_by='create_time desc')

        # 构造并上报消息
        nextev_message, obj = publish_msg('specific_event', event_type='power_swap_start',
                                          data={'chg_subsys_encoding': pack['nio_encoding']},
                                          sleep_time=2)

        # 校验mysql
        tables = ['vehicle_soc_history']
        checker.check_mysql_tables(obj, tables, sample_ts=obj['sample_ts'], event_name='power_swap_start')

        # 校验
        with allure.step('校验 {}'.format(kafka['topics']['power_swap'])):
            kafka_msg = None
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['power_swap'], timeout=60):
                logger.debug(f'consumed {data}')
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                logger.debug(f'consumed {data}')
                if kafka_msg['event_data']['sample_ts'] == obj['sample_ts'] and vid == kafka_msg['vehicle_id']:
                    is_found = True
                    break
            assert_equal(True, is_found)
            event_data = parse_nextev_message(nextev_message)['params']
            # 将上报的消息变为utf-8格式
            power_swap_event_in_message = {k: v for k, v in event_data.items()}
            power_swap_event_in_message['event_data'] = ast.literal_eval(power_swap_event_in_message['event_data'])
            power_swap_event_in_message['event_data']['bid'] = pack['bid']
            if 'marcopolo' in cmdopt:
                del (power_swap_event_in_message['event_data']['chg_subsys_encoding'])
            assert_equal(kafka_msg, power_swap_event_in_message)

    def test_power_swap_end_event(self, vid, publish_msg, kafka, mysql, cmdopt, checker):
        # kafka['comn'].set_offset_to_end(kafka['topics']['power_swap'])
        # 选取电池编码
        pack = mysql['battery_trace'].fetch_one('sys_battery_pack_entity', where_model={'status': 1},
                                                order_by='create_time desc')
        # 构造并上报消息
        nextev_message, obj = publish_msg('specific_event', event_type='power_swap_end',
                                          data={'chg_subsys_encoding': pack['nio_encoding']},
                                          sleep_time=2)

        # 校验mysql
        tables = ['vehicle_soc_history']
        checker.check_mysql_tables(obj, tables, sample_ts=obj['sample_ts'], event_name='power_swap_end')

        # 校验
        with allure.step('校验 {}'.format(kafka['topics']['power_swap'])):
            kafka_msg = None
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['power_swap'], timeout=60):
                logger.debug(f'consumed {data}')
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                logger.debug(f'consumed {data}')

                if kafka_msg['event_data']['sample_ts'] == obj['sample_ts'] and vid == kafka_msg['vehicle_id']:
                    is_found = True
                    break

            event_data = parse_nextev_message(nextev_message)['params']
            # 将上报的消息变为utf-8格式
            power_swap_event_in_message = {k: v for k, v in event_data.items()}
            power_swap_event_in_message['event_data'] = ast.literal_eval(power_swap_event_in_message['event_data'])
            assert_equal(True, is_found)
            power_swap_event_in_message['event_data']['bid'] = pack['bid']
            if 'marcopolo' in cmdopt:
                del (power_swap_event_in_message['event_data']['chg_subsys_encoding'])
            assert_equal(kafka_msg, power_swap_event_in_message)

    def test_power_swap_failure_event(self, vid, publish_msg, kafka, checker):
        kafka['comn'].set_offset_to_end(kafka['topics']['power_swap'])
        # 构造并上报消息
        nextev_message, obj = publish_msg('specific_event', event_type='power_swap_failure',
                                          data={'chg_subsys_encoding': 'P0000084AH130YY0012340001YFTY49'},
                                          sleep_time=2)

        # 校验mysql
        tables = ['vehicle_soc_history']
        checker.check_mysql_tables(obj, tables, sample_ts=obj['sample_ts'], event_name='power_swap_failure')

        # 校验
        with allure.step('校验 {}'.format(kafka['topics']['power_swap'])):
            kafka_msg = None
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['power_swap'], timeout=60):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                logger.debug(f'consumed {data}')
                if kafka_msg['event_data']['sample_ts'] == obj['sample_ts'] and vid == kafka_msg['vehicle_id']:
                    is_found = True
                    break
            assert_equal(True, is_found)
            event_data = parse_nextev_message(nextev_message)['params']
            # 将上报的消息变为utf-8格式
            power_swap_event_in_message = {k: v for k, v in event_data.items()}
            power_swap_event_in_message['event_data'] = ast.literal_eval(power_swap_event_in_message['event_data'])
            assert_equal(kafka_msg, power_swap_event_in_message)
