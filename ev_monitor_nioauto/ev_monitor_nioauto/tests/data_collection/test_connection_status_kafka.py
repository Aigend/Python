#!/usr/bin/env python
# coding=utf-8

"""
:file: test_connection_status_kafka.py
:author: yanmei.liu
:Date: Created on 2019/3/18
"""
import datetime
import random
import time
import pytest
import allure
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.nextev_msg import parse_nextev_message
from nio_messages import connection_status_event
from utils import message_formator
from utils.assertions import assert_equal


case = ['CGW sends connection status', 'CDC sends connection status', 'ADC sends connection status',
        'ADC NT2 sends connection status']


@pytest.mark.test
class TestConnectionStatus(object):
    @pytest.fixture(scope="function", params=['CGW', 'CDC', 'ADC', 'ADC NT2'], ids=case)
    def prepare(self, request, vid, cmdopt, kafka, publish_msg_by_kafka):
        with allure.step("先上报一个periodical_journey_update事件"):
            latest_msg_type = 'periodical_journey_update'
            publish_msg_by_kafka(latest_msg_type)
        with allure.step("上报connection事件"):
            topic_map = {'CGW': kafka['topics']['cgw'],
                         'CDC': kafka['topics']['cdc'],
                         'ADC': kafka['topics']['adc'],
                         'ADC NT2': kafka['topics']['adc_nt2']
                         }
            ecu_type = request.param
            status_random = random.choice(['OFFLINE', 'ONLINE', 'CONNECTION_LOST'])
            ts = int(time.time() * 1000)
            msg = gen_nextev_message("connection_status_event", {"status": status_random}, publish_ts=ts, msg_type=4, account_id=vid)
            kafka['cvs'].produce(topic_map[ecu_type], msg)
            time.sleep(1)
            data = parse_nextev_message(msg)
        return data, ecu_type

    def test_connection_status_kafka(self, vid, checker, prepare, kafka, cassandra, publish_msg_by_kafka, cmdopt):
        with allure.step("取Cassandra中的数据，并变换到kafka的数据格式"):
            sample_date = datetime.datetime.fromtimestamp(prepare[0]['publish_ts'] / 1000.0).strftime('%Y-%m')
            msg_in_cassandra = cassandra['datacollection'].fetch('vehicle_data',
                                                                 where_model={'vehicle_id': vid,
                                                                              'sample_date': sample_date,
                                                                              'sample_ts': prepare[0]['publish_ts'],
                                                                              'msg_type': 'ecu_connection_status'},
                                                                 fields={'connection_status',
                                                                         'position_status',
                                                                         'soc_status',
                                                                         'vehicle_status',
                                                                         'process_id',
                                                                         'vehicle_id'})[0]
            msg_in_cassandra = checker._clear_none(msg_in_cassandra)
            kafka_formator = message_formator.MsgToKafkaFormator(vid, prepare[0]['publish_ts'])
            cassandra_to_kafka_data = kafka_formator.to_connection_status_event(prepare[0], msg_in_cassandra)
            if 'marcopolo' in cmdopt:
                cassandra_to_kafka_data['params']['vehicle_status']['position_status']['longitude'] = None
                cassandra_to_kafka_data['params']['vehicle_status']['position_status']['latitude'] = None

        with allure.step("KAFKA校验swc-tsp-data_collection-${env}-vehicle_data与Cassandra一致"):
            for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=30):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == prepare[0]['publish_ts'] and msg['params']['account_id'] == prepare[0]['params']['account_id']:
                    msg['params']['vehicle_status'] = connection_status_event.parse_connection_status_message(msg['params']['vehicle_status'])
                    break
            msg['params'].pop('original_length')
            assert_equal(msg, cassandra_to_kafka_data)
