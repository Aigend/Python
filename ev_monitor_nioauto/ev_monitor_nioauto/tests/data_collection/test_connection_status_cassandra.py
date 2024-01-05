#!/usr/bin/env python
# coding=utf-8
import random
import time
import pytest
import allure
from nio_messages.nextev_msg import gen_nextev_message

case = ['CGW sends connection status', 'CDC sends connection status', 'ADC sends connection status',
        'ADC NT2 sends connection status']


class TestConnectionStatus(object):
    @pytest.mark.parametrize("platform", ['CGW', 'CDC', 'ADC', 'ADC NT2'], ids=case)
    def test_cassandra(self, checker, kafka, publish_msg_by_kafka, platform, vid):
        """
        消费了connection status数据后，在存往cassandra时，会去redis cluster里取soc_status，position_status等实时信息落库。
        此处是data collection唯一一处和redis cluster的关联。
        如果redis cluster中值过期了的话，不会去mysql里取值。
        """
        with allure.step("先上报一个periodical_journey_update事件"):
            latest_msg_type = 'periodical_journey_update'
            nextev_message, last_obj = publish_msg_by_kafka(latest_msg_type)

        with allure.step("上报connection事件"):
            topic_map = {'CGW': kafka['topics']['cgw'],
                         'CDC': kafka['topics']['cdc'],
                         'ADC': kafka['topics']['adc'],
                         'ADC NT2': kafka['topics']['adc_nt2']
                         }
            status_random = random.choice(['OFFLINE', 'ONLINE', 'CONNECTION_LOST'])
            ts = int(time.time() * 1000)

            msg = gen_nextev_message("", {"status": status_random}, publish_ts=ts, msg_type=4, account_id=vid)
            kafka['cvs'].produce(topic_map[platform], msg)
            time.sleep(2)

        with allure.step("校验connection status信息与cassandra所存信息一致"):
            status_map = {'OFFLINE': 0, 'ONLINE': 1, 'CONNECTION_LOST': 2}
            platform_map = {'CGW': 0, 'CDC': 1, 'ADC': 2, 'ADC NT2': 2}

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
