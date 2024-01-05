#!/usr/bin/env python
# coding=utf-8
"""
rvs server处理mysql的落库，data collection处理kafka和cassandra的落库
"""

import random
import time
import pytest

import allure
from nio_messages.nextev_msg import gen_nextev_message
from utils.assertions import assert_equal
from utils.time_parse import timestamp_to_utc_strtime

case = ['ADC NT2 sends connection status', 'CGW sends connection status', 'CDC sends connection status', 'ADC sends connection status']


class TestConnectionStatus(object):
    @pytest.fixture(scope="class", params=['ADC NT2', 'CGW', 'CDC', 'ADC'], ids=case)
    def prepare(self, request, vid, cmdopt, kafka):
        topic_map = {'CGW': kafka['topics']['cgw'],
                     'CDC': kafka['topics']['cdc'],
                     'ADC': kafka['topics']['adc'],
                     'ADC NT2': kafka['topics']['adc_nt2']
                     }

        platform = request.param

        status_random = random.choice(['OFFLINE', 'ONLINE', 'CONNECTION_LOST'])
        ts = int(time.time() * 1000)
        port = random.choice(['20083', '20084'])
        msg = gen_nextev_message("", {"status": status_random, "port": port}, publish_ts=ts, msg_type=4, account_id=vid, version=18)
        kafka['cvs'].produce(topic_map[platform], msg)
        time.sleep(1)

        yield {'vid': vid, 'platform': platform, 'ts': ts, 'status': status_random, 'port': port}

    def test_mysql(self, prepare, mysql):
        with allure.step("校验connection status信息与mysql connection_status所存信息一致"):
            status_map = {'OFFLINE': 0, 'ONLINE': 1, 'CONNECTION_LOST': 0}
            update_time = str(timestamp_to_utc_strtime(int(prepare['ts'])))

            if prepare['platform'] == 'CGW':
                data_in_mysql = mysql['rvs'].fetch('status_connection', {"id": prepare['vid']},
                                                   exclude_fields=['cdc_connected', 'cdc_update_time',
                                                                   'adc_connected', 'adc_update_time',
                                                                   'cdc_port', 'adc_port'])[0]

                data_in_message = {'id': prepare['vid'], 'cgw_connected': status_map[prepare['status']],
                                   'cgw_port': int(prepare['port']), 'update_time': update_time}
                assert_equal(data_in_mysql, data_in_message)

            if prepare['platform'] == 'CDC':
                data_in_mysql = mysql['rvs'].fetch('status_connection', {"id": prepare['vid']},
                                                   exclude_fields=['cgw_connected', 'update_time',
                                                                   'adc_connected', 'adc_update_time',
                                                                   'cgw_port', 'adc_port'])[0]

                data_in_message = {'id': prepare['vid'], 'cdc_connected': status_map[prepare['status']],
                                   'cdc_port': int(prepare['port']), 'cdc_update_time': update_time}
                assert_equal(data_in_mysql, data_in_message)

            if 'ADC' in prepare['platform']:
                data_in_mysql = mysql['rvs'].fetch('status_connection', {"id": prepare['vid']},
                                                   exclude_fields=['cgw_connected', 'update_time',
                                                                   'cdc_connected', 'cdc_update_time',
                                                                   'cdc_port', 'cgw_port'])[0]

                data_in_message = {'id': prepare['vid'], 'adc_connected': status_map[prepare['status']],
                                   'adc_port': int(prepare['port']), 'adc_update_time': update_time}
                assert_equal(data_in_mysql, data_in_message)
