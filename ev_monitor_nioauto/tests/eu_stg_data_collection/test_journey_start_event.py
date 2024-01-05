""" 
@author:dun.yuan
@time: 2021/6/20 1:08 上午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import random
import pytest
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal


class TestJourneyStartMsg(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    def test_journey_start_event(self, publish_msg, checker, prepare, vid, kafka):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        mileage = prepare['original_mileage'] + 1
        nextev_message, journey_start_obj = publish_msg('journey_start_event', sleep_time=30,
                                                        vehicle_status={"mileage": mileage}
                                                        )

        # 校验mysql
        # tables =['status_position', 'status_vehicle', 'status_soc', 'status_btry_packs', 'status_hvac']
        # checker.check_mysql_tables(journey_start_obj, tables, event_name='journey_start_event')

        # 校验cassandra
        tables = {
            'vehicle_data': ['vehicle_id',
                             'soc_status',
                             'position_status',
                             'vehicle_status',
                             'hvac_status',
                             # 'btry_pak_info',
                             'icc_id',
                             'process_id as journey_id',
                             'sample_ts'],
            'driving_data': ['dump_enrgy',
                             'mileage',
                             'position',
                             'posng_valid_type',
                             'soc',
                             'speed',
                             'realtime_power_consumption',
                             'sample_ts']
        }
        journey_start_obj.pop('battery_package_info')
        checker.check_cassandra_tables(journey_start_obj, tables, event_name='journey_start_event')

        # 校验kafka
        msg = None
        for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=10):
            msg = parse_nextev_message(data)
            if msg['publish_ts'] == journey_start_obj['sample_ts'] and vid == msg['params']['account_id']:
                break

        # 新增bid字段，验证推送到大数据平台的消息里携带
        # assert 'bid' in msg['params']['vehicle_status']['battery_package_info']['btry_pak_encoding'][0]
        # msg['params']['vehicle_status']['battery_package_info']['btry_pak_encoding'][0].pop('bid')
        # msg['params']['original_length'] = str(int(msg['params']['original_length'])-34)

        with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
            assert_equal(msg, parse_nextev_message(nextev_message))

