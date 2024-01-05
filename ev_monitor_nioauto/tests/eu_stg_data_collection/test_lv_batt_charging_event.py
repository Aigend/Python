""" 
@author:dun.yuan
@time: 2021/6/20 4:03 下午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import allure

from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestLvBattChargingMsg(object):
    def test_lv_batt_charging_event(self, vid, kafka, publish_msg, checker):
        """
        vehicle_data kafka 加上发送未解析的can msg
        未解析的 msg_id 为原 msg_id 取负数，value为hexstring，即表示十六进制的字符串
        """
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, obj = publish_msg('lv_batt_charging_event', sleep_time=30,
                                          can_msg={
                                              'can_data': [
                                                  {
                                                      'msg_id': 850,
                                                      'value': '6800500000'
                                                  },
                                                  {
                                                      'msg_id': 852,
                                                      'value': '0000000000000000'
                                                  }
                                              ]
                                          })

        # 校验cassandra
        tables = {'vehicle_data': ['vehicle_id',
                                   'lv_batt_charging_status',
                                   'can_msg',
                                   'vehicle_status',
                                   'sample_ts']}

        checker.check_cassandra_tables(obj, tables, event_name='lv_batt_charging_event')

        # 校验kafka
        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=10):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            msg.pop('params') if msg else None
            nextev_obj = parse_nextev_message(nextev_message)
            nextev_obj.pop('params')
            assert_equal(msg, nextev_obj)

        # 校验mysql
        tables = ['history_lv_battery', 'status_lv_battery']
        checker.check_mysql_tables(obj, tables)