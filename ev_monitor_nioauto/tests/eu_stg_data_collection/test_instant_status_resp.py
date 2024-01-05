""" 
@author:dun.yuan
@time: 2021/6/20 12:40 上午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import random
import pytest
import time
import allure
from nio_messages.nextev_msg import parse_nextev_message
from utils.assertions import assert_equal

list_situation = (False, True)
case = []
for i in list_situation:
    if i is True:
        srr = 'set_outside_sample_ts=' + str(i) + ', use outside sample_ts.'
        case.append(srr)
    if i is False:
        srr = 'set_outside_sample_ts=' + str(i) + ', use inside sample_ts.'
        case.append(srr)


@allure.feature('上报车辆的全量事件')
class TestInstantStatusMsg(object):
    @allure.story('车机处于离线状态，当恢复在线状态上报此事件，保证app显示为最新的车辆状态')
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        '''如果无初始化值就返回0'''
        sql_result = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])
        return {'original_mileage': sql_result[0]['mileage'] if sql_result else 0}

    @pytest.mark.parametrize("set_outside_sample_ts", list_situation, ids=case)
    def test_instant_status_resp(self, vid, kafka, prepare, checker, publish_msg, set_outside_sample_ts):
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['vehicle_data'])

        # 构造并上报消息
        mileage = prepare['original_mileage'] + 1
        if set_outside_sample_ts:
            nextev_message, instant_status_obj = publish_msg('instant_status_resp', sleep_time=30,
                                                             outside_sample_ts=int(round(time.time() * 1000)),
                                                             sample_point={
                                                                 "vehicle_status": {
                                                                     "mileage": mileage}
                                                             })
        else:
            nextev_message, instant_status_obj = publish_msg('instant_status_resp', sleep_time=30,
                                                             sample_point={
                                                                 "vehicle_status": {
                                                                     "mileage": mileage}
                                                             })

        # 校验cassandra
        if 'sample_ts' in instant_status_obj:
            cassandra_time = instant_status_obj['sample_ts']
        else:
            cassandra_time = instant_status_obj['sample_point']['sample_ts']

        tables = {'vehicle_data': ['vehicle_id',
                                      'charging_info',
                                      'soc_status',
                                      'trip_status',
                                      'body_status',
                                      'position_status',
                                      'vehicle_status',
                                      'bms_status',
                                      'driving_data',
                                      'driving_motor_status',
                                      'extremum_data',
                                      'occupant_status',
                                      'hvac_status',
                                      'tyre_status',
                                      'can_msg',
                                      'window_status',
                                      'light_status',
                                      'door_status',
                                      # 'btry_pak_info',
                                      # 're_alarm_data',
                                      'alarm_data',
                                      'evm_flag',
                                      'sample_ts']
                  }
        instant_status_obj['sample_point'].pop('battery_package_info')
        checker.check_cassandra_tables(instant_status_obj['sample_point'], tables,
                                       event_name='instant_status_resp',
                                       sample_ts=cassandra_time)

        # 校验kafka
        # publish_ts = instant_status_obj['sample_point']['sample_ts'] + 2000
        # msg = None
        # for data in kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=10):
        #     msg = parse_nextev_message(data)
        #     if msg['publish_ts'] == publish_ts and vid == msg['params']['account_id']:
        #         break
        #
        # with allure.step('校验 {}'.format(kafka['topics']['vehicle_data'])):
        #     # msg.pop('params') if msg else None
        #     nextev_obj = parse_nextev_message(nextev_message)
        #     msg['params'].pop('original_length')
        #     nextev_obj['params'].pop('original_length')
        #     msg['params']['vehicle_status']['sample_point'].pop('can_msg')
        #     nextev_obj['params']['vehicle_status']['sample_point'].pop('can_msg')
        #     assert_equal(msg, nextev_obj)

        # 校验mysql
        tables = ['status_position', 'status_vehicle', 'status_soc',
                  'status_btry_packs', 'status_occupant', 'status_driving_motor_data', 'status_driving_motor',
                  'status_extremum_data', 'status_driving_data', 'status_hvac',
                  'status_tyre', 'status_door', 'status_light', 'status_window']

        checker.check_mysql_tables(instant_status_obj['sample_point'], tables)