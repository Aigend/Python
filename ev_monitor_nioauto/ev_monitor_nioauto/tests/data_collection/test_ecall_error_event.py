""" 
@author:dun.yuan
@time: 2022/5/6 12:21 AM
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestEcallErrMsg(object):
    def test_ecall_error_event(self, vid, checker, publish_msg, kafka, env):
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])
        with allure.step("上报事件ecall_error_event"):
            nextev_message, ecall_error_obj = publish_msg('ecall_error_event')

        with allure.step("检查向下游kafka推送"):
            for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=60):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == ecall_error_obj['sample_ts'] and vid == msg['params']['account_id']:
                    break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            expect = parse_nextev_message(nextev_message)
            assert_equal(msg, expect)

        with allure.step("检查cassandra vehicle_data表更新"):
            tables = {'vehicle_data': ['vehicle_id',
                                       'sample_ts',
                                       'emgc_call_flr_sts']
                      }
            checker.check_cassandra_tables(ecall_error_obj, tables, event_name='ecall_error_event')