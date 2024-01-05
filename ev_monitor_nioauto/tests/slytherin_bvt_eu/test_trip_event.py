""" 
@author:dun.yuan
@time: 2021/6/7 11:22 上午
@contact: dun.yuan@nio.com
@description: 1.从protobuf版本18开始处理trip，proto msg版本和event中版本同时更新为18
2.trip按vehicle_id分表，存入rvs_data_test库中
3.proto版本小于18的处理逻辑不变；大于等于18的journeyevent不再存分表，只写主表用于统计；大于等于18的行程周期性事件，按"%s:trip_first:%s:%s"和"%s:trip_last:%s:%s"写周期性状态到redis;大于等于18的驾驶行为事件，数据更新到trip中
4.trip事件不做聚合，需存储tripstatus数据
5.新增trip事件补数据job
@showdoc：
"""
import json
import random
import time
import allure
import pytest

from utils.assertions import assert_equal


class TestTripEvent(object):
    @pytest.fixture(scope='function', autouse=False)
    def prepare(self, vid, checker):
        original_mileage_in_mysql = checker.mysql.fetch('status_vehicle', {"id": vid}, ['mileage'])

        return {'original_mileage': original_mileage_in_mysql[0]['mileage']}

    def test_trip_event_as_entire_trip(self, vid, publish_msg, checker, prepare):
        trip_id = str(round(time.time()))
        with allure.step("上报事件trip_start_event, protobuf版本18"):
            start_remaining_range = round(random.randint(500, 2000) * 0.5)
            nextev_message, trip_start_obj = publish_msg('trip_start_event', protobuf_v=18, sleep_time=4,
                                                         vehicle_status={'mileage': prepare['original_mileage']},
                                                         trip_status={'trip_id': trip_id},
                                                         soc_status={'remaining_range': start_remaining_range})  # rvs_data 表增加start_remaining_range字段

        with allure.step("检验mysql rvs_data数据库的存储"):
            trip_in_mysql = checker.mysql_rvs_data.fetch_one(f'vehicle_trip_history_{vid[:2]}', {'trip_id': trip_id},
                                                             ['start_soc', 'start_dump_energy', 'start_mileage', 'start_remaining_range'])
            assert trip_in_mysql['start_soc'] == trip_start_obj['soc_status']['soc']
            assert trip_in_mysql['start_dump_energy'] == round(trip_start_obj['soc_status']['dump_enrgy'], 1)
            assert trip_in_mysql['start_mileage'] == trip_start_obj['vehicle_status']['mileage']
            # trip_in_mysql存储的经纬度是longitude_gcj02和latitude_gcj02，在Cassandra
            # assert trip_in_mysql['start_longitude'] == trip_start_obj['position_status']['longitude']
            # assert trip_in_mysql['start_latitude'] == trip_start_obj['position_status']['latitude']
            assert trip_in_mysql['start_remaining_range'] == start_remaining_range

        with allure.step("上报周期行程事件"):
            nextev_message, journey_update_obj = publish_msg('periodical_journey_update', protobuf_v=18,
                                                             sample_points=[{
                                                                 'sample_ts': round(time.time() * 1000)+11000,
                                                                 'vehicle_status': {
                                                                     "mileage": prepare['original_mileage'] + 1},
                                                                 'trip_status': {'trip_id': trip_id, 'trip_state': 2}
                                                             }])
        '''
        with allure.step("检查redis trip first缓存数据"):
            remote_vehicle_key_front = redis_key_front['remote_vehicle']
            key_first = f'{remote_vehicle_key_front}:trip_first:{vid}:{trip_id}'
            trip_first = checker.redis.get(key_first)
            data = json.loads(trip_first)

            assert data['soc_status']['soc'] == journey_update_obj['sample_points'][0]['soc_status']['soc']
            assert data['vehicle_status']['mileage'] == journey_update_obj['sample_points'][0]['vehicle_status'][
                'mileage']
            assert round(data['position_status']['longitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['longitude'])
            assert round(data['position_status']['latitude']) == round(
                journey_update_obj['sample_points'][0]['position_status']['latitude'])
            assert data['sample_time'] == journey_update_obj['sample_points'][0]['sample_ts'] // 1000
            assert round(data['driving_data']['average_speed']) == round(
                journey_update_obj['sample_points'][0]['driving_data']['average_speed'])
            assert round(data['driving_data']['max_speed']) == round(
                journey_update_obj['sample_points'][0]['driving_data']['max_speed'])
            assert round(data['driving_data']['min_speed']) == round(
                journey_update_obj['sample_points'][0]['driving_data']['min_speed'])
            data['trip_status'].pop('sample_time')
            journey_update_obj['sample_points'][0]['trip_status'].pop('trip_id')
            assert_equal(data['trip_status'], journey_update_obj['sample_points'][0]['trip_status'])
        '''
        with allure.step("上报事件trip_end_event, protobuf版本18"):
            end_remaining_range = round(random.randint(0, 500) * 0.5)
            nextev_message, trip_end_obj = publish_msg('trip_end_event', protobuf_v=18,
                                                       sample_ts=round(time.time() * 1000) + 15000,
                                                       vehicle_status={'mileage': prepare['original_mileage'] + 3},
                                                       trip_status={'trip_id': trip_id, 'trip_state': 2},
                                                       soc_status={'remaining_range': end_remaining_range})  # rvs_data 表增加end_remaining_range字段

        with allure.step("检验mysql rvs_data数据库的存储"):
            trip_in_mysql = checker.mysql_rvs_data.fetch_one(f'vehicle_trip_history_{vid[:2]}', {'trip_id': trip_id},
                                                             ['end_soc', 'end_dump_energy', 'end_mileage',
                                                              'end_remaining_range', 'trip_odometer', 'trip_eng', 'avg_speed'],
                                                             suffix=' and `end_soc` is not NULL')

            assert trip_in_mysql['end_soc'] == trip_end_obj['soc_status']['soc']
            assert trip_in_mysql['end_dump_energy'] == round(trip_end_obj['soc_status']['dump_enrgy'], 1)
            assert trip_in_mysql['end_mileage'] == trip_end_obj['vehicle_status']['mileage']
            assert trip_in_mysql['trip_odometer'] == trip_end_obj['trip_status']['trip_odometer']
            assert trip_in_mysql['trip_eng'] == trip_end_obj['trip_status']['trip_eng']
            assert trip_in_mysql['end_remaining_range'] == end_remaining_range
            # 检查mysql 速度的更新
            period = (trip_end_obj['sample_ts'] - trip_start_obj['sample_ts']) // 1000
            assert trip_in_mysql['avg_speed'] == round(3600 * trip_in_mysql['trip_odometer'] / period, 1)
            # assert trip_in_mysql['max_speed'] == round(data['driving_data']['max_speed'], 1)
            # assert trip_in_mysql['min_speed'] == round(data['driving_data']['min_speed'], 1)
