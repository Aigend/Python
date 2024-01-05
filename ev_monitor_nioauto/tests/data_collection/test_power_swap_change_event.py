""" 
@author:dun.yuan
@time: 2021/12/8 7:35 下午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import pytest
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestPowerSwapMsg(object):
    def test_power_swap_service_event(self, vid, checker, publish_msg, kafka):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        with allure.step("上报事件power_swap_service_event"):
            nextev_message, power_swap_obj = publish_msg('power_swap_service_event', protobuf_v=18)

        with allure.step("检验cassandra power_swap_status表更新"):
            tables = {'vehicle_data': ['vehicle_id',
                                       'window_status',
                                       'power_swap_status',
                                       'sample_ts']}
            checker.check_cassandra_tables(power_swap_obj, tables, event_name='power_swap_service_event')

        with allure.step("检验向下游kafka推送"):
            for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=60):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == power_swap_obj['sample_ts'] and vid == msg['params']['account_id']:
                    break
        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            expect = parse_nextev_message(nextev_message)
            assert_equal(msg, expect)

    @pytest.mark.test
    def test_power_swap_service_periodic(self, vid, checker, publish_msg, kafka, cassandra):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        with allure.step("上报事件power_swap_service_periodic"):
            nextev_message, power_swap_obj = publish_msg('power_swap_service_periodic', protobuf_v=18)

        with allure.step("检验cassandra power_swap_status表更新"):
            msg = cassandra['datacollection'].fetch('vehicle_data',
                                              {"vehicle_id": vid,
                                               "sample_ts": power_swap_obj['sample_ts'],
                                               "msg_type": 'power_swap_service_periodic'})
            assert msg is None or len(msg) == 0

        found = False
        with allure.step("检验向下游kafka推送"):
            for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=10):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == power_swap_obj['sample_ts'] and vid == msg['params']['account_id']:
                    found = True
                    break
        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            assert not found
