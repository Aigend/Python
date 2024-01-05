""" 
@author:dun.yuan
@time: 2021/6/19 6:30 下午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
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

case = ['CGW sends connection status', 'CDC sends connection status', 'ADC sends connection status']


class TestConnectionStatus(object):
    @pytest.mark.parametrize("platform", ['CGW', 'CDC', 'ADC'], ids=case)
    def test_cassandra(self, checker, kafka, publish_msg, platform, vid, cassandra):
        """
        消费了connection status数据后，在存往cassandra时，会去redis cluster里取soc_status，position_status等实时信息落库。
        此处是data collection唯一一处和redis cluster的关联。
        如果redis cluster中值过期了的话，不会去mysql里取值。
        """
        with allure.step("先上报一个periodical_journey_update事件"):
            latest_msg_type = 'periodical_journey_update'
            nextev_message, last_obj = publish_msg(latest_msg_type)

        with allure.step("上报connection事件"):
            topic_map = {'CGW': kafka['topics']['cgw'],
                         'CDC': kafka['topics']['cdc'],
                         'ADC': kafka['topics']['adc']
                         }
            status_random = random.choice(['OFFLINE', 'ONLINE', 'CONNECTION_LOST'])
            ts = int(time.time() * 1000)

            msg = gen_nextev_message("connection_status_event", {"status": status_random}, publish_ts=ts, msg_type=4, account_id=vid)
            kafka['cvs'].produce(topic_map[platform], msg)
            dt = parse_nextev_message(msg)
            time.sleep(2)

        with allure.step("校验connection status信息与cassandra所存信息一致"):
            status_map = {'OFFLINE': 0, 'ONLINE': 1, 'CONNECTION_LOST': 2}
            platform_map = {'CGW': 0, 'CDC': 1, 'ADC': 2}

            # 校验
            tables = {
                'vehicle_data': ['vehicle_id',
                                 'soc_status',
                                 'position_status',
                                 'vehicle_status',
                                 'process_id',
                                 'msg_type',
                                 'connection_status',
                                 'sample_ts',
                                 ],

            }

            checker.check_cassandra_tables({'sample_ts': ts}, tables, event_name='ecu_connection_status',
                                           latest_msg_type=latest_msg_type,
                                           status=status_map[status_random],
                                           ecu_type=platform_map[platform],
                                           process_id=last_obj['journey_id'])

        with allure.step("取Cassandra中的数据，并变换到kafka的数据格式"):
            sample_date = datetime.datetime.fromtimestamp(dt['publish_ts'] / 1000.0).strftime('%Y-%m')
            msg_in_cassandra = cassandra['datacollection'].fetch('vehicle_data',
                                                                 where_model={'vehicle_id': vid,
                                                                              'sample_date': sample_date,
                                                                              'sample_ts': dt['publish_ts'],
                                                                              'msg_type': 'ecu_connection_status'},
                                                                 fields={'connection_status',
                                                                         'position_status',
                                                                         'soc_status',
                                                                         'vehicle_status',
                                                                         'process_id',
                                                                         'vehicle_id'})[0]
            msg_in_cassandra = checker._clear_none(msg_in_cassandra)
            kafka_formator = message_formator.MsgToKafkaFormator(vid, dt['publish_ts'])
            cassandra_to_kafka_data = kafka_formator.to_connection_status_event(dt, msg_in_cassandra)

        with allure.step("KAFKA校验swc-tsp-data_collection-${env}-vehicle_data与Cassandra一致"):
            for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=30):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == dt['publish_ts'] and msg['params']['account_id'] == dt['params']['account_id']:
                    msg['params']['vehicle_status'] = connection_status_event.parse_connection_status_message(
                        msg['params']['vehicle_status'])
                    break
            msg['params'].pop('original_length')
            assert_equal(msg, cassandra_to_kafka_data)
