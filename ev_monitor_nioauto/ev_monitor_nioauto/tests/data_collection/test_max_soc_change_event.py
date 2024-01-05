""" 
@author:dun.yuan
@time: 2021/10/18 6:43 下午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestMaxSocChangeEvent(object):
    def test_max_soc_change_event(self, vid, checker, publish_msg, kafka):
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        with allure.step("上报事件max_soc_change_event"):
            nextev_message, max_soc_change_obj = publish_msg('max_soc_change_event', protobuf_v=18)

        with allure.step("检查向下游kafka推送"):
            for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=60):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == max_soc_change_obj['sample_ts'] and vid == msg['params']['account_id']:
                    break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            expect = parse_nextev_message(nextev_message)
            assert_equal(msg, expect)

        with allure.step("检查cassandra vehicle_data表更新"):
            tables = {'vehicle_data': ['vehicle_id',
                                       'sample_ts',
                                       'soc_status']
                      }
            checker.check_cassandra_tables(max_soc_change_obj, tables, event_name='max_soc_change_event')

        with allure.step("检验mysql status_trip表更新"):
            tables = ['status_soc']
            checker.check_mysql_tables(max_soc_change_obj, tables)