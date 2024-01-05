""" 
@author:dun.yuan
@time: 2022/3/15 6:21 PM
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestSaBattHealth(object):
    def test_sa_batt_status_event(self, vid, checker, publish_msg_by_kafka, kafka):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        with allure.step("上报事件sa_cellular_status_event"):
            nextev_message, sa_batt_health_obj = publish_msg_by_kafka('sa_cellular_status_event', protobuf_v=18, platform_type=1)

        with allure.step("检验cassandra sa_cellular_status_event表更新"):
            tables = {'vehicle_data': ['vehicle_id',
                                       'sa_cellular_status',
                                       'sample_ts']}
            checker.check_cassandra_tables(sa_batt_health_obj, tables, event_name='sa_cellular_status_event')

        with allure.step("检验向下游kafka推送"):
            for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=60):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == sa_batt_health_obj['sample_ts'] and vid == msg['params']['account_id']:
                    break
        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            expect = parse_nextev_message(nextev_message)
            assert_equal(msg, expect)
