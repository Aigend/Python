""" 
@author:dun.yuan
@time: 2022/5/5 2:31 PM
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestCDCErrMsg(object):
    def test_cdc_system_error_event(self, vid, checker, publish_msg, kafka):
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])
        with allure.step("上报事件cdc_err_msg"):
            nextev_message, cdc_err_obj = publish_msg('cdc_system_error_event')

        with allure.step("检查向下游kafka推送"):
            for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=60):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == cdc_err_obj['sample_ts'] and vid == msg['params']['account_id']:
                    break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            expect = parse_nextev_message(nextev_message)
            assert_equal(msg, expect)

        with allure.step("检查cassandra vehicle_data表更新"):
            tables = {'vehicle_data': ['vehicle_id',
                                       'sample_ts',
                                       'can_cdc_sys_err']
                      }
            checker.check_cassandra_tables(cdc_err_obj, tables, event_name='cdc_system_error_event')
