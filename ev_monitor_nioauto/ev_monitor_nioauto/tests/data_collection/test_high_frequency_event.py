""" 
@author:dun.yuan
@time: 2022/5/7 1:12 AM
@contact: dun.yuan@nio.com
@description: 该事件只针对部分车辆，只有选定触发的车辆才会上报该事件，数据用于相关的分析
@showdoc：
"""
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestHighFrequencyEvent(object):
    def test_high_frequency_event(self, vid, checker, publish_msg, kafka, env):
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])
        with allure.step("上报事件high_frequency_event"):
            nextev_message, high_frequency_obj = publish_msg('high_frequency_event')

        with allure.step("检查向下游kafka推送"):
            for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=60):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == high_frequency_obj['sample_ts'] and vid == msg['params']['account_id']:
                    break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            expect = parse_nextev_message(nextev_message)
            assert_equal(msg, expect)

        with allure.step("检查cassandra vehicle_data表更新"):
            tables = {'vehicle_data': ['vehicle_id',
                                       'sample_ts',
                                       'can_msg',
                                       'position_status.attitude as attitude',
                                       'driving_data']
                      }
            for item in high_frequency_obj['high_fre_data']:
                item['can_msg'].pop('can_news')
                item['driving_data'] = item.pop('steerWhlag')
                sample_ts = item.pop('sample_time')
                checker.check_cassandra_tables(item, tables, event_name='high_frequency_event', sample_ts=sample_ts)
