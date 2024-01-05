""" 
@author:dun.yuan
@time: 2022/5/5 7:09 PM
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestCPDWarnMsg(object):
    def test_cpd_warn_event(self, vid, checker, publish_msg, kafka, env):
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])
        with allure.step("上报事件cpd_warning_event"):
            nextev_message, cpd_warning_obj = publish_msg('cpd_warning_event',
                                                          account_id=env['vehicles']['normal']['account_id'])

        with allure.step("检查向下游kafka推送"):
            for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=60):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == cpd_warning_obj['sample_ts'] and vid == msg['params']['account_id']:
                    break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            expect = parse_nextev_message(nextev_message)
            assert_equal(msg, expect)

        with allure.step("检查cassandra vehicle_data表更新"):
            tables = {'vehicle_data': ['vehicle_id',
                                       'sample_ts',
                                       'door_status.door_locks.account_id as account_id',
                                       'cpd_sts']
                      }
            checker.check_cassandra_tables(cpd_warning_obj, tables, event_name='cpd_warning_event')
