""" 
@author:dun.yuan
@time: 2021/10/18 6:45 下午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""

import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestNbsAbortEvent(object):
    def test_nbs_abort_event(self, vid, checker, publish_msg, kafka):
        """
        vehicle_data kafka 加上发送未解析的can msg
        未解析的 msg_id 为原 msg_id 取负数，value为hexstring，即表示十六进制的字符串
        """
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])
        with allure.step("上报事件nbs_abort_event"):
            nextev_message, nbs_abort_obj = publish_msg('nbs_abort_event', protobuf_v=18)

        with allure.step("检查向下游kafka推送"):
            for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=60):
                msg = parse_nextev_message(data)
                if msg['publish_ts'] == nbs_abort_obj['sample_ts'] and vid == msg['params']['account_id']:
                    break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            expect = parse_nextev_message(nextev_message)
            msg['params'].pop('original_length')
            expect['params'].pop('original_length')
            msg['params'].pop('vehicle_status')
            expect['params'].pop('vehicle_status')
            assert_equal(msg, expect)

        with allure.step("检查cassandra vehicle_data表更新"):
            tables = {'vehicle_data': ['vehicle_id',
                                       'sample_ts',
                                       'vehicle_status.vehl_type_dbc',
                                       'can_msg_list']
                      }
            for item in nbs_abort_obj['can_msg']:
                item.pop('can_news')
            checker.check_cassandra_tables(nbs_abort_obj, tables, event_name='nbs_abort_event')