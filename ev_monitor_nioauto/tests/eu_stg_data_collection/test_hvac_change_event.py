""" 
@author:dun.yuan
@time: 2021/6/20 12:26 上午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import pytest
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal

case = [
    'air_con_on=0 and ccu_cbn_pre_ac_ena_sts=1, result mysql air_con_on=1, hvac on',
    'air_con_on=1 and ccu_cbn_pre_ac_ena_sts=0, result mysql air_con_on=1, hvac on',
    'air_con_on=1 and ccu_cbn_pre_ac_ena_sts=1, result mysql air_con_on=1, hvac on',
    'air_con_on=0 and ccu_cbn_pre_ac_ena_sts=0, result mysql air_con_on=0, hvac off'
]


class TestHvacChangeMsg(object):
    @pytest.mark.parametrize("air_con_on,ccu_cbn_pre_ac_ena_sts", zip([0, 1, 1, 0], [1, 0, 1, 0]), ids=case)
    def test_hvac_change_event(self, air_con_on, ccu_cbn_pre_ac_ena_sts, publish_msg, checker, vid, kafka):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        nextev_message, hvac_change_obj = publish_msg('hvac_change_event', sleep_time=30,
                                                      hvac_status={"air_con_on": air_con_on,
                                                                   "ccu_cbn_pre_ac_ena_sts": ccu_cbn_pre_ac_ena_sts}
                                                      )

        # 校验cassandra
        tables ={'vehicle_data':['vehicle_id',
                                 'hvac_status',
                                 'sample_ts']
                 }
        checker.check_cassandra_tables(hvac_change_obj, tables, event_name='hvac_change_event')

        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=10):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == hvac_change_obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            assert_equal(msg, parse_nextev_message(nextev_message))

        # 校验mysql
        tables = ['status_hvac']
        checker.check_mysql_tables(hvac_change_obj, tables)